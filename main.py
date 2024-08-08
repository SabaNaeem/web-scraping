import requests
import csv
from bs4 import BeautifulSoup


def fetch_content(content):
    try:
        soup = BeautifulSoup(content, 'html.parser')
        titles = soup.find_all('div', attrs={'class': 'product-card__title'})
        prices = soup.find_all('span', attrs={'class': 'price-item--regular'})
        if not titles or not prices:
            raise ValueError("Could not find the expected HTML elements (titles or prices)")
        data = []
        for title, price in zip(titles, prices):
            print(title.text)
            price = price.text.replace(" ", "").replace("\n", "")
            print(price)
            data.append([title.text, price])
        return data
    except Exception as err:
        print(f"An error occurred while parsing HTML: {err}")
        return None


def fetch_url(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.content
    except Exception as err:
        print(f"An error occurred: {err}")
        return None


def create_csv(all_data):
    try:
        filename = input("Enter the name of the CSV file: ")
        if filename.endswith(".csv"):
            with open(filename, mode='w', newline='') as file:
                writer = csv.writer(file)

                writer.writerow(['Title', 'Price'])

                for data in all_data:
                    i = 0
                    while i < len(data):
                        writer.writerow([data[i][0], data[i][1]])
                        i += 1

            print("Data has been written to products.csv")
        else:
            print("File type not supported")
    except Exception as err:
        print(f"An error occurred: {err}")


def main():
    pages = 2
    all_data = []
    # https://booksforless.ph/collections/best-sellers-1
    url = input("Enter URL: ")
    for page in range(1, pages + 1):
        update_url = f"{url}?page={page}"  # Adjust URL pattern if needed
        print(f"Fetching page {page} from {update_url}")

        content = fetch_url(update_url)
        if content:
            if isinstance(content, bytes):
                content = content.decode('utf-8')

        data = fetch_content(content)
        if data:
            all_data.append(data)

    create_csv(all_data)


if __name__ == '__main__':
    main()
