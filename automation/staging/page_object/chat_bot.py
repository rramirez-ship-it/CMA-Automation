

class chat_bot:
    def __init__(self, page):
        self.page = page
        
    def chat_bot_homepage(self):
        self.page.goto("https://staging.cloudcma.com/")
        self.page.locator("#embeddedMessagingIconChat").to_be_visible()
        self.page.locator("#embeddedMessagingIconChat").to_be_clickable()
        self.page.get_by_text("Have questions? Let’s chat").to_be_visible()
            
        
    def chat_bot_cma(self):
        self.page.goto('https://staging.cloudcma.com/cmas')
        self.page.locator("#embeddedMessagingIconChat").to_be_visible()
        self.page.locator("#embeddedMessagingIconChat").to_be_clickable()
        self.page.get_by_text("Have questions? Let’s chat").to_be_visible()
        
    def chat_bot_tour(self):
        self.page.goto('https://staging.cloudcma.com/tours')
        self.page.locator("#embeddedMessagingIconChat").to_be_visible()
        self.page.locator("#embeddedMessagingIconChat").to_be_clickable()
        self.page.get_by_text("Have questions? Let’s chat").to_be_visible()
        
    def chat_bot_property(self):
        self.page.goto('https://staging.cloudcma.com/properties')
        self.page.locator("#embeddedMessagingIconChat").to_be_visible()
        self.page.locator("#embeddedMessagingIconChat").to_be_clickable()
        self.page.get_by_text("Have questions? Let’s chat").to_be_visible()
        
    def chat_bot_presentation(self):
        self.page.goto('https://staging.cloudcma.com/presentations')
        self.page.locator("#embeddedMessagingIconChat").to_be_visible()
        self.page.locator("#embeddedMessagingIconChat").to_be_clickable()
        self.page.get_by_text("Have questions? Let’s chat").to_be_visible()
    
    def chat_bot_flyer(self):
        self.page.goto('https://staging.cloudcma.com/flyers')
        self.page.locator("#embeddedMessagingIconChat").to_be_visible()
        self.page.locator("#embeddedMessagingIconChat").to_be_clickable()
        self.page.get_by_text("Have questions? Let’s chat").to_be_visible()
        
    def chat_bot_homebeat(self):
        self.page.goto('https://staging.cloudcma.com/homebeat')
        self.page.locator("#embeddedMessagingIconChat").not_to_be_visible()
        self.page.get_by_text("Have questions? Let’s chat").not_to_be_visible()