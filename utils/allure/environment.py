import platform
from pathlib import Path

from config import settings


def create_allure_environment_file(output_directory: Path) -> None:
    """Сохраняет в Allure только безопасные технические параметры запуска."""

    viewport = settings.browser_viewport
    properties = {
        "browsers": ",".join(browser.value for browser in settings.browser),
        "headless": str(settings.headless).lower(),
        "viewport": (
            f"{viewport.width}x{viewport.height}"
            f"@{viewport.device_scale_factor}"
        ),
        "os": platform.platform(),
        "python_version": platform.python_version(),
    }
    content = "\n".join(f"{key}={value}" for key, value in properties.items())

    output_directory.mkdir(parents=True, exist_ok=True)
    output = output_directory.joinpath("environment.properties")
    output.write_text(content, encoding="utf-8")
