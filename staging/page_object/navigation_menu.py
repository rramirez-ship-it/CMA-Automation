from playwright.sync_api import Page, expect


class NavigationMenu:
    def __init__(self, page: Page):
        self.page = page

        # Locators
        self.nav_bar = page.locator("nav:visible")
        self.client_switcher_button = page.locator(
            "button.ClientSwitcher-module_client-picker__button__2e80Y"
        )
        self.home_menu_item = page.locator("li:has-text('Home')")
        self.contacts_link = page.get_by_label("Contacts")
        self.relationships_link = page.get_by_label("Relationships")
        self.cloud_attract_item = page.get_by_role(
            "menuitem", name="Cloud Attract - 1 instances available"
        )
        self.cloud_mlx_item = page.get_by_role(
            "menuitem", name="Cloud MLX - 1 instances available"
        )
        self.cloud_cma_item = page.get_by_role(
            "menuitem", name="Cloud CMA - 1 instances available"
        )
        self.cloud_streams_item = page.get_by_role(
            "menuitem", name="Cloud Streams - 1 instances available"
        )
        self.liondesk_item = page.get_by_role(
            "menuitem", name="LionDesk - 1 instances available"
        )
        self.spacio_item = page.get_by_role(
            "menuitem", name="Spacio - 1 instances available"
        )

    # --- Assertions ---

    def verify_nav_bar_items(self):
        """Verifies all expected text labels are present in the nav bar."""
        expected_items = ["Home", "CMA", "Tour", "Property", "Presentation", "Flyer", "Homebeat"]
        for item in expected_items:
            expect(self.nav_bar.locator(f"text={item}")).to_be_visible()

    def verify_client_switcher_is_enabled(self):
        expect(self.client_switcher_button).to_be_visible()
        expect(self.client_switcher_button).to_be_enabled()

    def verify_home_item_is_visible(self):
        expect(self.home_menu_item).to_be_visible()

    def verify_contacts_is_visible(self):
        expect(self.contacts_link).to_be_visible()

    def verify_relationships_is_visible(self):
        expect(self.relationships_link).to_be_visible()

    def verify_all_menu_items_visible(self):
        """Verifies all product menu items are visible and enabled."""
        items = [
            self.cloud_attract_item,
            self.cloud_mlx_item,
            self.cloud_cma_item,
            self.cloud_streams_item,
            self.liondesk_item,
            self.spacio_item,
        ]
        for item in items:
            expect(item).to_be_visible()
            expect(item).to_be_enabled()

    def verify_full_navigation_bar(self):
        """
        Orchestrator method: runs all nav bar verifications in sequence.
        Call this from your test instead of calling each method individually.
        """
        self.verify_nav_bar_items()
        self.verify_client_switcher_is_enabled()
        self.verify_home_item_is_visible()
        self.verify_contacts_is_visible()
        self.verify_relationships_is_visible()
        self.verify_all_menu_items_visible()       
        
    