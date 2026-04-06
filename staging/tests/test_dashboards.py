from playwright.sync_api import expect
from staging.page_object.nav_bar import NavigationMenu


def soft_expect_visible(locator, label, failures):
    try:
        expect(locator).to_be_visible()
    except AssertionError:
        failures.append(f"FAILED: '{label}' it's not visible")


def test_dashboard_navigation(page):
    failures = []
    
    page.goto('https://platform.stg.lwolf.com/product/select?a=cc')
    expect(page.locator('#product-select')).to_be_visible()
    page.get_by_role("link", name="Munoz Realty (STG)").click()
    
    nav = NavigationMenu(page)

    # Verify navigation menu CMA
    nav.page.get_by_role("link", name="CMA").click()
    soft_expect_visible(page.get_by_role("heading", name="CMA Reports"), "Heading CMA Reports", failures)
    soft_expect_visible(page.get_by_role("link", name="Create CMA Report"), "Link Create CMA Report", failures)
    nav.verify_nav_bar_menu(failures)

    # Verify navigation menu Tours
    nav.page.get_by_role("link", name="Tour").click()
    soft_expect_visible(page.get_by_role("heading", name="Buyer Tours"), "Heading Buyer Tours", failures)
    soft_expect_visible(page.get_by_role("link", name="Create Buyer Tour"), "Link Create Buyer Tour", failures)
    nav.verify_nav_bar_menu(failures)

    # Verify navigation menu Property
    nav.page.get_by_role("link", name="Property").click()
    soft_expect_visible(page.get_by_role("heading", name="Property Reports"), "Heading Property Reports", failures)
    soft_expect_visible(page.get_by_role("link", name="Create Property Report"), "Link Create Property Report", failures)
    nav.verify_nav_bar_menu(failures)

    # Verify navigation menu Presentation
    nav.page.get_by_role("link", name="Presentation").click()
    soft_expect_visible(page.get_by_role("heading", name="Presentations"), "Heading Presentations", failures)
    soft_expect_visible(page.get_by_role("link", name="Create Presentation"), "Link Create Presentation", failures)
    nav.verify_nav_bar_menu(failures)

    # Verify navigation menu Flyer
    nav.page.get_by_role("link", name="Flyer").click()
    soft_expect_visible(page.get_by_role("heading", name="Flyers"), "Heading Flyers", failures)
    soft_expect_visible(page.get_by_role("link", name="Create Flyer"), "Link Create Flyer", failures)
    nav.verify_nav_bar_menu(failures)

    # Verify navigation menu Homebeats
    nav.page.get_by_role("link", name="Homebeat", exact=True).click()
    soft_expect_visible(page.get_by_role("heading", name="Homebeats"), "Heading Homebeats", failures)
    nav.verify_nav_bar_menu(failures)

    # final report
    assert not failures, "\n" + "\n".join(failures)