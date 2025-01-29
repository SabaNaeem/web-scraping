import time
import json
import re
from seleniumbase import Driver

def main():

    urls = {
        'bedspread': 'https://mesaky.com/ar/category/POGlWK', #31
        'mattresses': '',
        'mattress-pad': 'https://mesaky.com/ar/category/WPrdxV', # 41
        'side-table': 'https://mesaky.com/ar/category/VaNmVv', # 49
        'console': 'https://mesaky.com/ar/category/ADyKYb',  # 31
        'dressing-table': 'https://mesaky.com/ar/category/vZGQQA',  # 15
        'comforter': '',
        'tv-table': 'https://mesaky.com/ar/category/KzWEEb', #18
        # 'dining-table': '',
        'storage-box': 'https://mesaky.com/ar/category/vAeOby', # 9
        'flower-pot-and-plant': 'https://mesaky.com/ar/category/YzWxrq',  # 70
        'statue-and-antique': 'https://mesaky.com/ar/category/yKeRnz', # 41
        'laundry-basket': 'https://mesaky.com/ar/category/KRgrqD', # 2
        'candle': 'https://mesaky.com/ar/category/PDYKeG',  # 24
        # 'candlestick': '',
        'vase': 'https://mesaky.com/ar/category/lvxEqd', # 45
        # 'plant': '',
        'flower': 'https://mesaky.com/ar/category/GqvpGb', # 76
        'wall-clock': 'https://mesaky.com/ar/category/qGZEgm', #36
        'shelve': 'https://mesaky.com/ar/category/PDYKam',  #63
        # 'decorative-hanger': '',
        'lighting': 'https://mesaky.com/ar/category/xQnoDK', #269
        'lampshade': 'https://mesaky.com/ar/category/nxXVdz', #105
        'floor-stand': 'https://mesaky.com/ar/category/WPrEZg', #50
        'wall-lighting': 'https://mesaky.com/ar/category/ZPdNxY', # 505
        'outdoor-lighting': 'https://mesaky.com/ar/category/PlgNvQ', #148
        'chandelier': 'https://mesaky.com/ar/category/lZzVVr',
        'pendant-lighting': 'https://mesaky.com/ar/category/GXrBBO', # 521
        'coffee-maker': 'https://mesaky.com/ar/category/WzQQXw', #114
        'cooking-appliance': 'https://mesaky.com/ar/category/vAeexE', #129
        'food-processor': 'https://mesaky.com/ar/category/bwDDPN', # 58
        'cooking-pot': 'https://mesaky.com/ar/category/DpwmVB', #165
        'serving-utensil-and-tray': 'https://mesaky.com/ar/category/qGZybV', #207
        'cup': 'https://mesaky.com/ar/category/KzdGxG',
        'plate': 'https://mesaky.com/ar/category/zoYGeq', #735
        'others': ''
    }
    failed = []
    for key, url in urls.items():
        # Initialize the driver
        driver = Driver(uc=True)
        driver.uc_open_with_reconnect(url, reconnect_time=10)
        driver.uc_gui_click_captcha()
        # Scroll to the bottom of the page to load all content
        last_height = driver.execute_script("return document.body.scrollHeight;")
        time.sleep(5)
        while True:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(10)  # Allow time for content to load
            new_height = driver.execute_script("return document.body.scrollHeight;")
            if new_height == last_height:
                break
            last_height = new_height

        time.sleep(3)

        # Define the XPath for the product links
        product_links_xpath = "//h3[contains(@class,'s-product-card-content-title')]/a"

        # Find all product links on the page
        product_links = []
        try:
            elements = driver.find_elements("xpath", product_links_xpath)
            for element in elements:
                href = element.get_attribute("href")
                if href:
                    product_links.append(href)
        except Exception as e:
            print(f"Error extracting product links: {e}")
        print("Total products found: ", len(product_links))
        # List to store extracted data
        scraped_data = []
        # Visit each product link and scrape details
        for index, product_url in enumerate(product_links):
            try:
                # Open the product page
                driver.get(product_url)
                driver.uc_open_with_reconnect(product_url, reconnect_time=4)
                print(f"Scraping product {index + 1} of {len(product_links)}")
                time.sleep(1)  # Wait for the page to load

                # Extract product title
                product_title_xpath = "//h1"
                product_title_element = driver.find_element("xpath", product_title_xpath)
                product_title = product_title_element.text if product_title_element else ""

                # Extract product image URL
                product_image_xpath = "//salla-slider/div[2]/div[1]/a[1]/img"
                product_image_element = driver.find_element("xpath", product_image_xpath)
                product_image_url = product_image_element.get_attribute("src") if product_image_element else ""

                # Extract product price
                product_price_xpath = "//div[@class='price my-1']/div//h2[contains(@class,'total-price font-bold da-tm text-xl')]"
                product_price_element = driver.find_element("xpath", product_price_xpath)

                if product_price_element:
                    # Clean up the extracted price text
                    price_split = product_price_element.text.split()  # Split into price and currency
                else:
                    price_split = []

                # Extract price and currency
                product_price = price_split[0]
                product_currency = price_split[1]

                # Extract product description
                product_description_xpath = "//div[contains(@class,'tabs')]//div[@id='product-tabs-details']/div[contains(@class,'product__description')]"
                product_description_elements = driver.find_elements("xpath", product_description_xpath)

                if product_description_elements:
                    product_description_div = product_description_elements[0].get_attribute("innerHTML")
                    product_description = re.sub(r"<[^>]+>", "",
                                                 product_description_div).strip() if product_description_div else ""
                else:
                    product_description = ""

                # Append the data to the list
                scraped_data.append({
                    "product_url": product_url,
                    "product_category": "bedspreads",
                    "product_title": product_title,
                    "product_image_url": product_image_url,
                    "product_price": product_price,
                    "product_description": product_description,
                    "product_currency": product_currency
                })

                print(f"Title: {product_title}")
                print(f"Image URL: {product_image_url}")
                print(f"Price: {product_price}")
                print(f"Description: {product_description}")
                print(f"Currency: {product_currency}")
                print("-" * 50)

            except Exception as e:
                failed.append(product_url)
                print(f"Error scraping product at {product_url}: {e}")

        # Save the scraped data to a JSON file
        output_file = "scraped_products.json"
        # Load existing data if the file exists
        try:
            with open(output_file, "r", encoding="utf-8") as file:
                existing_data = json.load(file)
        except FileNotFoundError:
            existing_data = []

            # Append the new data to the existing data
            existing_data.extend(scraped_data)

            # Save the updated data to the file
            with open(output_file, "w", encoding="utf-8") as file:
                json.dump(existing_data, file, ensure_ascii=False, indent=4)

            print(f"Data saved to {output_file}")
            print(f"Failed URLs: {failed}")
            # Close the driver
            driver.quit()

if __name__ == "__main__":
    main()

