from playwright.sync_api import expect

class ClientSwitcher: 
    def __init__(self, page):
        self.page = page
        self.switcher_button = page.locator("ClientSwitcher-module_client-picker__button__2e80Y")
        self.nav = page.locator("ClientSwitcher-module_client-picker__button__2e80Y")
        
    def verify_client_switcher(self, failures: list):
        expected_items = [
            "Home",
            "Contacts",
            "Relationships",
            "Cloud Attract",
            "Cloud CMA",
            "Cloud MLX",
            "Cloud Streams",
            "LionDesk",
            "Spacio"
        ]
        
    def open(self):
        self.switcher_button.click()
        self.nav.wait_for(state="visible")
        
    def verify_all_links(self, failures: list): 
        self.open()
        for item in self.expected_items:
            locator = self.nav.get_by_role("link", name=item, exact=True)
            try: 
                expect(locator).to_be_visible()
            except AssertionError as e:
                failures.append(f"FAILED: The following product '{item}' it's not visible")
                
    def go_to(self, product_name: str):
        self.open()
        self.nav.get_by_role("link", name=product_name, exact=True).click()