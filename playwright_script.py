import os
import requests
from playwright.sync_api import sync_playwright
import csv

def scrape_products(url):

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()

        # Navigate to the Pinterest page
        print("Loading page...")
        page.goto(url)
        csv_file = open("products.csv", "a", newline='')
        csv_write = csv.writer(csv_file)

        # Write header if file is new
        if csv_file.tell() == 0:
            csv_write.writerow(['Image URL', 'Model Colors', 'Price'])

        products = page.locator("xpath=//li[@class='product-card']").all()

        # Iterate over products and extract model colors and price
        for product in products:
            img_url = product.locator("xpath=.//img").first
            model_colors = product.locator("xpath=.//div[@class='product-card-title']/h4").first
            price = product.locator("xpath=.//span[@class='current-price']").first

            if model_colors and price and img_url:
                model_colors_text = model_colors.text_content()
                price_text = price.text_content()
                img = img_url.get_attribute("src")

                # Write to CSV file
                csv_write.writerow([img, model_colors_text, price_text])

        csv_file.close()

        browser.close()



# Define the Pinterest URL and output folder
page_url = "https://www.customwheeloffset.com/store/wheels"

# Run the scraper
scrape_products(page_url)
