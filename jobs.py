import json

from playwright.sync_api import sync_playwright


def fetch_content(page, url):
    titles = []
    links = []

    try:
        page.goto(url, timeout=60000000)

        page.wait_for_selector('div.columns')
        cols = page.query_selector_all('div.col4')

        for col in cols:
            content = col.query_selector_all('a.btn-link')
            for c in content:
                titles.append(c.inner_text())
                links.append(c.get_attribute('href'))

        return titles, links
    except Exception as err:
        print(f"An error occurred while parsing HTML: {err}")
        return None, None


def fetch_description(page, url):
    try:
        page.goto(url)

        page.wait_for_selector('div.wysiwyg-content.row')
        description = page.query_selector('div.wysiwyg-content.row').inner_text()
        return description
    except Exception as err:
        print(f"An error occurred while parsing HTML: {err}")
        return None


def create_json(data):
    try:
        with open("jobs.json", 'w') as file:
            json.dump(data, file, indent=4)
        print(f"Data has been written to file")
    except Exception as e:
        print(f"An error occurred while writing to the JSON file: {e}")


def main():
    url = 'https://www.concordia.edu/resources/human-resources/adjunct-faculty-positions/'
    all_descriptions = []
    data = []
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        # page.goto('https://www.concordia.edu/resources/human-resources/adjunct-faculty-positions/', timeout=6000)
        titles, links = fetch_content(page, url)
        if titles and links:
            for link in links:
                full_url = f"https://www.concordia.edu{link}"
                description = fetch_description(page, full_url)
                if description:
                    all_descriptions.append(description)

        for title, link, description in zip(titles, links, all_descriptions):
            data.append({
                "title": title,
                "link": link,
                "description": description
            })
        browser.close()
        create_json(data)


if __name__ == '__main__':
    main()
