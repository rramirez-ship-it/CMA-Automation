# conftest.py
import os
import pytest
from playwright.sync_api import sync_playwright

AUTH_FILE = "auth.json"
USER_DATA_DIR = "./browser-profile"

@pytest.fixture(scope="session")
def browser_context():
    with sync_playwright() as p:

        # Si NO existe el perfil pero SÍ existe auth.json,
        # lanzar contexto normal una vez para poblar el perfil
        if not os.path.exists(USER_DATA_DIR) and os.path.exists(AUTH_FILE):
            temp_browser = p.chromium.launch(headless=False)
            temp_context = temp_browser.new_context(storage_state=AUTH_FILE)
            temp_context.storage_state(path=AUTH_FILE)  # refrescar
            temp_context.close()
            temp_browser.close()

        if not os.path.exists(AUTH_FILE) and not os.path.exists(USER_DATA_DIR):
            raise FileNotFoundError(
                "❌ No se encontró 'auth.json' ni 'browser-profile/'.\n"
                "   Ejecuta primero: python save_auth.py"
            )

        context = p.chromium.launch_persistent_context(
            user_data_dir=USER_DATA_DIR,
            headless=False,
            viewport={"width": 1280, "height": 720},
        )

        yield context

        context.storage_state(path=AUTH_FILE)
        context.close()


@pytest.fixture(scope="session")
def page(browser_context):
    page = browser_context.new_page()
    yield page
    page.close()


# ── Screenshots automáticos en fallos ──────────────────────────────────────
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    if report.failed and call.when == "call":
        page = item.funcargs.get("page")
        if page:
            os.makedirs("reports/screenshots", exist_ok=True)
            screenshot_path = f"reports/screenshots/{item.name}.png"
            page.screenshot(path=screenshot_path, full_page=True)

            # Adjunta el screenshot al reporte HTML
            try:
                from pytest_html import extras
                report.extra = getattr(report, "extra", [])
                report.extra.append(extras.image(screenshot_path))
            except ImportError:
                pass  # Si pytest-html no está instalado, no rompe nada