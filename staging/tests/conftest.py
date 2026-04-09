# conftest.py
import os
import re
import allure
import pytest
from pathlib import Path
from playwright.sync_api import sync_playwright

AUTH_FILE     = "auth.json"
USER_DATA_DIR = "./browser-profile"

# Patrón de archivos que genera Playwright con --screenshot only-on-failure
SCREENSHOT_NAME_PATTERN = re.compile(r"^test-failed-\d+\.png$")


# ──────────────────────────────────────────────
# CLI option:  pytest --browser-name firefox
# ──────────────────────────────────────────────
def pytest_addoption(parser):
    parser.addoption(
        "--browser-name",
        action="store",
        default="chromium",
        choices=["chromium", "firefox", "webkit"],
        help="Browser a usar: chromium | firefox | webkit",
    )


@pytest.fixture(scope="session")
def browser_name(request):
    return (
        request.config.getoption("--browser", default=None)
        or request.config.getoption("--browser-name", default="chromium")
    )


# ──────────────────────────────────────────────
# Browser context  (Chromium SSO persistente /
# Firefox + WebKit con storage_state)
# ──────────────────────────────────────────────
@pytest.fixture(scope="session")
def browser_context(browser_name):
    with sync_playwright() as p:
        browser_type = getattr(p, browser_name)

        if browser_name == "chromium":
            if not os.path.exists(USER_DATA_DIR):
                if os.path.exists(AUTH_FILE):
                    temp = p.chromium.launch(headless=True)
                    ctx  = temp.new_context(storage_state=AUTH_FILE)
                    ctx.storage_state(path=AUTH_FILE)
                    ctx.close()
                    temp.close()
                else:
                    raise FileNotFoundError(
                        "No se encontró 'auth.json' ni 'browser-profile/'.\n"
                        " Ejecuta primero: python save_auth.py"
                    )

            context = p.chromium.launch_persistent_context(
                user_data_dir=USER_DATA_DIR,
                headless=False,
                viewport={"width": 1280, "height": 720},
                user_agent=(
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/122.0.0.0 Safari/537.36"
                ),
            )

        else:
            if not os.path.exists(AUTH_FILE):
                raise FileNotFoundError(
                    f"Para {browser_name} se requiere 'auth.json'.\n"
                    "   Ejecuta primero: python save_auth.py"
                )

            user_agents = {
                "firefox": (
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:124.0) "
                    "Gecko/20100101 Firefox/124.0"
                ),
                "webkit": (
                    "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_4) "
                    "AppleWebKit/605.1.15 (KHTML, like Gecko) "
                    "Version/17.4 Safari/605.1.15"
                ),
            }

            browser = browser_type.launch(headless=False)
            context = browser.new_context(
                storage_state=AUTH_FILE,
                viewport={"width": 1280, "height": 720},
                user_agent=user_agents[browser_name],
            )

        yield context

        try:
            context.storage_state(path=AUTH_FILE)
        except Exception:
            pass
        context.close()


@pytest.fixture(scope="session")
def page(browser_context):
    page = browser_context.new_page()
    yield page
    page.close()


# ──────────────────────────────────────────────
# Hook 1: screenshot en memoria → adjunto Allure
# Se activa cuando cualquier test falla en "call"
# Método en memoria = más confiable que leer
# desde disco (evita caché de SO según doc oficial)
# ──────────────────────────────────────────────
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report  = outcome.get_result()

    if report.when == "call" and report.failed:
        page = item.funcargs.get("page")
        if page is None:
            return

        browser_name = item.config.getoption("--browser-name", default="chromium")

        try:
            screenshot_bytes = page.screenshot(full_page=True)
            allure.attach(
                screenshot_bytes,
                name=f"Screenshot – {item.name} [{browser_name}]",
                attachment_type=allure.attachment_type.PNG,
            )
        except Exception as e:
            print(f"\n[allure] Error capturando screenshot: {e}")


# ──────────────────────────────────────────────
# Hook 2: recolecta screenshots que Playwright
# guardó automáticamente vía:
#   --screenshot only-on-failure  (pyproject.toml)
# Complementario al hook anterior
# ──────────────────────────────────────────────
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_teardown(item, nextitem):
    yield

    try:
        artifacts_dir = item.funcargs.get("output_path")
        if artifacts_dir:
            artifacts_dir_path = Path(artifacts_dir)
            if artifacts_dir_path.is_dir():
                for file in sorted(artifacts_dir_path.iterdir()):
                    if file.is_file() and SCREENSHOT_NAME_PATTERN.match(file.name):
                        allure.attach.file(
                            str(file),
                            name=file.name,
                            attachment_type=allure.attachment_type.PNG,
                        )
    except Exception as e:
        print(f"\n[allure teardown] Error adjuntando screenshot: {e}")
