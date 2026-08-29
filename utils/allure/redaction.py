import json
import re
from collections.abc import Iterable, MutableMapping
from pathlib import Path
from typing import Any


REDACTED = "<redacted>"
SENSITIVE_NAME_PARTS = (
    "password",
    "passwd",
    "token",
    "secret",
    "authorization",
    "cookie",
    "apikey",
)
SENSITIVE_ASSIGNMENT = re.compile(
    r"(?P<prefix>['\"]?[\w-]*(?:password|passwd|token|secret|authorization|cookie|api[_-]?key)"
    r"[\w-]*['\"]?\s*[:=]\s*)"
    r"(?P<value>Bearer\s+[A-Za-z0-9._~+/=-]+|'[^']*'|\"[^\"]*\"|[^,\s})]+)",
    flags=re.IGNORECASE,
)


def is_sensitive_name(name: str) -> bool:
    normalized = "".join(character for character in name.casefold() if character.isalnum())
    return any(part in normalized for part in SENSITIVE_NAME_PARTS)


def redact_nested_value(value: Any) -> Any:
    if isinstance(value, dict):
        return {
            key: REDACTED if is_sensitive_name(str(key)) else redact_nested_value(item)
            for key, item in value.items()
        }

    if isinstance(value, list):
        return [redact_nested_value(item) for item in value]

    return value


def redact_text(value: str, secret_values: Iterable[str] = ()) -> str:
    redacted = SENSITIVE_ASSIGNMENT.sub(
        lambda match: f"{match.group('prefix')}'{REDACTED}'",
        value,
    )
    for secret in {secret for secret in secret_values if secret}:
        redacted = redacted.replace(secret, REDACTED)
    return redacted


def _sanitize_json_value(value: Any, secret_values: Iterable[str]) -> Any:
    if isinstance(value, dict):
        return {
            key: REDACTED
            if is_sensitive_name(str(key))
            else _sanitize_json_value(item, secret_values)
            for key, item in value.items()
        }

    if isinstance(value, list):
        return [_sanitize_json_value(item, secret_values) for item in value]

    if isinstance(value, str):
        return redact_text(value, secret_values)

    return value


def redact_parameters(
        parameters: MutableMapping[str, str],
        secret_values: Iterable[str] = (),
        ) -> None:
    """Маскирует sensitive values в параметрах Allure step in place."""

    sensitive_indicator = any(
        name in {"field_name", "name", "parameter"}
        and is_sensitive_name(value.strip("'\" "))
        for name, value in parameters.items()
    )

    for name, value in parameters.items():
        if is_sensitive_name(name):
            parameters[name] = REDACTED
        elif sensitive_indicator and name in {"actual", "expected", "input", "value"}:
            parameters[name] = REDACTED
        else:
            parameters[name] = redact_text(value, secret_values)


def sanitize_allure_results(
        results_directory: Path,
        secret_values: Iterable[str] = (),
        ) -> None:
    """Маскирует sensitive text в созданных Allure result files."""

    if not results_directory.exists():
        return

    for artifact in results_directory.rglob("*"):
        if not artifact.is_file() or artifact.suffix not in {".json", ".txt", ".properties"}:
            continue

        content = artifact.read_text(encoding="utf-8", errors="replace")
        if artifact.suffix == ".json":
            try:
                payload = json.loads(content)
            except json.JSONDecodeError:
                sanitized = redact_text(content, secret_values)
            else:
                sanitized = json.dumps(
                    _sanitize_json_value(payload, secret_values),
                    ensure_ascii=False,
                    separators=(",", ":"),
                )
        else:
            sanitized = redact_text(content, secret_values)

        if sanitized != content:
            artifact.write_text(sanitized, encoding="utf-8")
