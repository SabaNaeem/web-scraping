import json

from playwright.sync_api import sync_playwright


def fetch_content(page, url):
    titles = []
    descriptions = []

    try:
        page.goto(url, timeout=60000000)

        page.wait_for_selector('div.kt-accordion-inner-wrap')
        divs = page.query_selector_all('div.wp-block-kadence-pane')

        for div in divs:
            title = div.query_selector('span.kt-blocks-accordion-title').text_content()
            description = div.query_selector('div.kt-accordion-panel-inner').text_content()
            titles.append(title)
            descriptions.append(description)
            print(title)
            print(description)

        return titles, descriptions
    except Exception as err:
        print(f"An error occurred while parsing HTML: {err}")
        return None, None


def create_json(data):
    try:
        with open("jobs_hiram.json", 'w') as file:
            json.dump(data, file, indent=4)
        print(f"Data has been written to file")
    except Exception as e:
        print(f"An error occurred while writing to the JSON file: {e}")


def main():
    url = 'https://www.hiram.edu/about-hiram-college/human-resources/careers-at-hiram/'
    descriptions = []
    data = []
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        titles, descriptions = fetch_content(page, url)

        for title, description in zip(titles, descriptions):
            data.append({
                "title": title,
                "description": description
            })
        browser.close()
        create_json(data)


if __name__ == '__main__':
    main()
