# conftest.py
import os
import base64
from datetime import datetime
import pytest
import pytest_html
from playwright.sync_api import sync_playwright

AUTH_FILE = "auth.json"
USER_DATA_DIR = "./browser-profile"
REPORTS_DIR = "reports"
SCREENSHOTS_DIR = os.path.join(REPORTS_DIR, "screenshots")


# ── CLI option: pytest --browser-name firefox
def pytest_addoption(parser):
    parser.addoption(
        "--browser-name",
        action="store",
        default="chromium",
        choices=["chromium", "firefox", "webkit"],
        help="Browser a usar: chromium | firefox | webkit",
    )


# ── Título del reporte
def pytest_html_report_title(report):
    report.title = "QA Automation Report – LWolf Platform"


# ── Info de entorno en el reporte
def pytest_configure(config):
    config._metadata = getattr(config, "_metadata", {})
    config._metadata["Project"] = "LWolf Staging Platform"
    config._metadata["Environment"] = "Staging"
    config._metadata["Base URL"] = "https://platform.stg.lwolf.com"


# ── Columna "Description" con el docstring del test
def pytest_html_results_table_header(cells):
    cells.insert(2, "<th>Description</th>")


def pytest_html_results_table_row(report, cells):
    cells.insert(2, f"<td>{getattr(report, 'description', '')}</td>")


@pytest.fixture(scope="session")
def browser_name(request):
    return (
        request.config.getoption("--browser", default=None)
        or request.config.getoption("--browser-name", default="chromium")
    )


@pytest.fixture(scope="session")
def browser_context(browser_name):
    with sync_playwright() as p:
        browser_type = getattr(p, browser_name)

        # ── Chromium: persistent context para preservar sesión SSO
        if browser_name == "chromium":
            if not os.path.exists(USER_DATA_DIR):
                if os.path.exists(AUTH_FILE):
                    temp = p.chromium.launch(headless=False)
                    ctx = temp.new_context(storage_state=AUTH_FILE)
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

        # ── Firefox / WebKit
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


# ── Hook principal: screenshot embebido en el reporte HTML
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    # Guardar descripción (docstring) para la columna extra
    report.description = str(item.function.__doc__ or "")

    # ── Solo en fase "call" y solo si falló
    if report.when == "call" and report.failed:
        page = item.funcargs.get("page")
        if page is None:
            return

        browser_name = item.config.getoption("--browser-name", default="chromium")
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        # 1. Guardar screenshot en disco
        os.makedirs(SCREENSHOTS_DIR, exist_ok=True)
        screenshot_path = os.path.join(
            SCREENSHOTS_DIR, f"{item.name}_{browser_name}_{timestamp}.png"
        )

        try:
            page.screenshot(path=screenshot_path, full_page=True)
        except Exception as e:
            print(f"\n[screenshot] Error capturando: {e}")
            return

        # 2. Leer bytes y convertir a base64
        try:
            with open(screenshot_path, "rb") as f:
                png_bytes = f.read()
            b64 = base64.b64encode(png_bytes).decode("utf-8")
        except Exception as e:
            print(f"\n[screenshot] Error leyendo archivo: {e}")
            return

        # 3. Adjuntar al reporte — API oficial pytest-html:
        #    · import pytest_html  (no "from pytest_html import extras")
        #    · report.extras       (plural ← este era el bug)
        #    · pytest_html.extras.png(b64_string)  para imagen embebida
        extras = getattr(report, "extras", [])
        extras.append(
            pytest_html.extras.png(b64, name=f"Screenshot – {browser_name}")
        )
        extras.append(
            pytest_html.extras.text(
                f"Guardado en: {screenshot_path}",
                name="Ruta del archivo",
            )
        )
        report.extras = extras  # ← plural, este era el bug principal
