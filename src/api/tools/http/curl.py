import json
import shlex
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit

from httpx import Request, RequestNotRead

from utils.allure.redaction import REDACTED, is_sensitive_name, redact_nested_value

OMITTED_BODY = "<non-JSON body omitted>"


def _sanitize_url(url: str) -> str:
    parsed = urlsplit(url)
    query = urlencode([
        (key, REDACTED if is_sensitive_name(key) else value)
        for key, value in parse_qsl(parsed.query, keep_blank_values=True)
    ])
    return urlunsplit((parsed.scheme, parsed.netloc, parsed.path, query, parsed.fragment))


def _sanitize_body(body: bytes) -> str:
    try:
        payload = json.loads(body.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError):
        return OMITTED_BODY

    return json.dumps(redact_nested_value(payload), ensure_ascii=False, separators=(",", ":"))


def get_curl_from_request(request: Request) -> str:
    """
    Формирует безопасную cURL-команду для Allure-отчёта.

    Sensitive headers, query parameters and JSON fields are redacted. An
    unstructured request body is omitted because it cannot be sanitized
    reliably.
    """
    result = [
        f"curl -X {shlex.quote(request.method)} "
        f"{shlex.quote(_sanitize_url(str(request.url)))}"
    ]

    for header, value in request.headers.items():
        safe_value = REDACTED if is_sensitive_name(header) else value
        result.append(f"-H {shlex.quote(f'{header}: {safe_value}')}")

    try:
        if body := request.content:
            result.append(f"-d {shlex.quote(_sanitize_body(body))}")
    except RequestNotRead:
        pass

    return " \\\n  ".join(result)
