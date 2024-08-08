# web-scraping
# Web Scraping Task: Book Information from a Bookstore

## Objective
Create a Python script that scrapes book information from a fictional online bookstore's bestsellers page using BeautifulSoup4.

## Requirements
1. Use Python 3.x
2. Use the `requests` library to fetch the web page
3. Use BeautifulSoup4 for parsing HTML
4. Extract the following information for each book:
   - Title
   - Author
   - Price
   - Rating (out of 5 stars)
5. Store the extracted data in a structured format (e.g., list of dictionaries)
6. Write the data to a CSV file

## Steps
1. Install required libraries:
   ```
   pip install requests beautifulsoup4
   ```

2. Import necessary modules:
   ```python
   import requests
   from bs4 import BeautifulSoup
   import csv
   ```

3. Send a GET request to the target URL:
   ```python
   url = "http://books.toscrape.com/index.html"
   response = requests.get(url)
   ```

4. Create a BeautifulSoup object to parse the HTML:
   ```python
   soup = BeautifulSoup(response.content, 'html.parser')
   ```

5. Find and extract the required information for each book:
   ```python
   books = soup.find_all('article', class_='product_pod')
   book_data = []
   for book in books:
       # Extract title, author, price, and rating
       # Append to book_data list
   ```

6. Write the extracted data to a CSV file:
   ```python
   with open('bestsellers.csv', 'w', newline='', encoding='utf-8') as csvfile:
       # Use csv.DictWriter to write the data
   ```

## Bonus Tasks
1. Implement error handling for network requests and HTML parsing
2. Add command-line arguments to specify the URL and output file name
3. Extend the script to scrape multiple pages of bestsellers

## Evaluation Criteria
- Correct implementation of BeautifulSoup4 for HTML parsing
- Accurate extraction of required book information
- Proper error handling and edge case management
- Code organization and readability
- Documentation and comments

## Resources
- BeautifulSoup4 Documentation: https://www.crummy.com/software/BeautifulSoup/bs4/doc/
- Requests Library Documentation: https://docs.python-requests.org/en/latest/
- Python CSV Module Documentation: https://docs.python.org/3/library/csv.html

Good luck with your web scraping task!
