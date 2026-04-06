
class user_menu:
    def __init__(self, page):
        self.page = page

    def click_user_menu(self):
        self.page.get_by_role("button", name="User menu").click()