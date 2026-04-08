# save_auth.py
from playwright.sync_api import expect, sync_playwright

AUTH_FILE = "staging/tests/auth.json"
USER_DATA_DIR = "./browser-profile"

with sync_playwright() as p:
    # Persistent context guarda la sesión en browser-profile/ directamente
    # sin necesitar storage_state como argumento
    context = p.chromium.launch_persistent_context(
        user_data_dir=USER_DATA_DIR,
        headless=False,
        viewport={"width": 1280, "height": 720},
    )

    page = context.new_page()
    page.goto('https://staging.cloudcma.com/real-estate-agents')
    page.get_by_role('link', name='Sign In').click()
    page.get_by_role('link', name='Sign in with Lone Wolf Account').click()
    page.get_by_role("textbox", name="Email address").fill("rramirez@lwolf.com")
    page.get_by_role("button", name="Continue").click()
    page.get_by_role("textbox", name="Enter the password for").fill("Trajes208112")
    page.get_by_role("button", name="Sign in").click()

    # page.wait_for_url("**/product/select**", timeout=120000)
    expect(page.locator('#product-select', timeout=120000)).to_be_visible()#EWWW

    # Guardar también en auth.json como respaldo
    context.storage_state(path=AUTH_FILE)
    print("✅ Sesión guardada en browser-profile/ y auth.json")

    context.close()