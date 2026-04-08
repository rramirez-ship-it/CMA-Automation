from playwright.sync_api import expect
from staging.page_object.nav_menu import ClientSwitcher
from staging.tests.conftest import page

def soft_expect_visible(locator, label, failures):
    try:
        expect(locator).to_be_visible()
    except AssertionError:
        failures.append(f"FAILED: '{label}' it's not visible")
        
def test_client_switcher(page):
    failures = []
    
    page.goto('https://platform.stg.lwolf.com/product/select?a=cc')
    expect(page.locator('#product-select')).to_be_visible()
    page.get_by_role("link", name="Munoz Realty (STG)").click()
    page.wait_for_load_state("networkidle")  # espera que la app termine de cargar

    # Dump del HTML completo para inspeccionar
    with open("debug_dom.html", "w") as f:
        f.write(page.content())

    page.screenshot(path="debug_screenshot.png", full_page=True)
    
    switcher = ClientSwitcher(page)
    

    #Verify in CMA page
    switcher.page.get_by_role("link", name="CMA").click()
    soft_expect_visible(page.get_by_role("heading", name="CMA Reports"), "Heading CMA Reports", failures)
    switcher.verify_all_links(failures)
    
    # Verify in Tours page
    switcher.page.get_by_role("link", name="Tour").click()
    soft_expect_visible(page.get_by_role("heading", name="Buyer Tours"), "Heading Buyer Tours", failures)
    switcher.verify_all_links(failures)
    
    # Verify in Property page
    switcher.page.get_by_role("link", name="Property").click()
    soft_expect_visible(page.get_by_role("heading", name="Property Reports"), "Heading Property Reports", failures)
    switcher.verify_all_links(failures)
    
    # Verify in Presentation page
    switcher.page.get_by_role("link", name="Presentation").click()
    soft_expect_visible(page.get_by_role("heading", name="Presentations"), "Heading Presentations", failures)
    switcher.verify_all_links(failures)
    
    # Verify in Flyer page
    switcher.page.get_by_role("link", name="Flyer").click()
    soft_expect_visible(page.get_by_role("heading", name="Flyers"), "Heading Flyers", failures)
    switcher.verify_all_links(failures)
    
    # Verify in Homebeats page
    switcher.page.get_by_role("link", name="Homebeat", exact=True).click
    soft_expect_visible(page.get_by_role("heading", name="Homebeats"), "Heading Homebeats", failures)
    switcher.verify_all_links(failures)
    
    
    # final report
    assert not failures, "\n" + "\n".join(failures)
