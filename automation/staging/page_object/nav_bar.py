from playwright.sync_api import Page, expect
import re


class NavigationMenu:
    def __init__(self, page: Page):
        self.page = page
        self.nav = page.locator("nav")
        
    def verify_nav_bar_menu(self, failures: list):
        expected_items = [
            "Home", 
            "CMA", 
            re.compile(r"^(Tour|Buyer Tour)$"),
            "Property", 
            "Presentation", 
            "Flyer", 
            "Homebeat"
        ]
        for item in expected_items:
            try:
                if isinstance(item, re.Pattern):
                    expect(self.page.get_by_role("link", name=item)).to_be_visible()
                else:
                    expect(self.page.get_by_role("link", name=item, exact=True)).to_be_visible()
            except AssertionError:
                failures.append(f"FAILED: Nav item '{item.pattern if isinstance(item, re.Pattern) else item}' it's not visible")
            
    def go_to(self, menu_item: str):
        self.nav.get_by_role("link", name=menu_item, exact=True).click()