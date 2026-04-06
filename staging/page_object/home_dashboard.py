

class homePage:
    def __init__(self, page):
        self.page = page
        
    def go_to_home_dashboard(self):
        self.page.goto('https://platform.stg.lwolf.com/product/select?a=cc')
        