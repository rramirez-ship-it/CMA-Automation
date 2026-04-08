
from datetime import datetime
import re

from playwright.sync_api import expect

import random

from staging.data_test.florida_addresses import FLORIDA_ADDRESSES



def test_create_CMA_Report_stg(page):
    page.goto('https://platform.stg.lwolf.com/product/select?a=cc')
    expect(page.locator('#product-select')).to_be_visible()
    page.get_by_role("link", name="Munoz Realty (STG)").click()
    page.get_by_role("link", name="CMA").click()
    
    #Create a new CMA Report
    page.locator("a:has-text('Create CMA Report')").click()
    version = datetime.now().strftime("%Y%m%d-%H%M%S")
    page.get_by_role("textbox", name="Title").fill(f"automation test v{version}")
    
    address = random.choice(FLORIDA_ADDRESSES)
    page.get_by_placeholder("Enter your property address").fill(address)
    
    first_suggestion = page.locator("[class*='address-auto-complete__InputContainer-sc-1cuppq9-2 efFhcU']").first
    first_suggestion.wait_for(state="visible", timeout=5000)
    first_suggestion.click()
    
    page.locator("form").filter(has_text="CriteriaListingsCustomizePublishFetch Listings").get_by_role("button").click()
    
    #Fetch Listings
    # count the total of checked boxes to comapre later
    
    stats = page.locator("div.sticky.listings-stats")
    stats_text = stats.inner_text()
    print(f"Stats text: {stats_text}")
    
    active_match = re.search(r"Active:\s*(\d+)", stats_text)
    sold_match = re.search(r"Sold:\s*(\d+)", stats_text)
    
    active_count = int(active_match.group(1)) if active_match else 0
    sold_count = int(sold_match.group(1)) if sold_match else 0

    total_listings = active_count + sold_count
    print(f"Active: {active_count} | Sold: {sold_count} | Total: {total_listings}")
    
    page.locator("form").get_by_role("link", name="Customize Report").click()

    # Customize Report

    expected_titles = ["Title page", "Cover letter"]


