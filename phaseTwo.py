import requests
import csv
import pathlib
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from phaseOne import scan_page, details

data_path = pathlib.Path('/Users/grazimarinoni/Desktop/OpenClassroom/Projects/Project-2/data')

headings = ["category",
            "book_title",
            "product_page_url",
            "universal_product_code (upc)",
            "price_incl_tax",
            "price_excl_tax",
            "qnt_available",
            "product_description",
            "review_rating",
            "image_url"]


def phase_two(category_url):
    cat_page = scan_page(category_url)
    # To collect a list of the div tags that have the books URLs
    bookURL_list = cat_page.find_all("div", class_="image_container")

    # To collect a list of the div tags that have the books URLs
    for books in bookURL_list:
        bookURL = books.find("a")["href"].replace("../../../","http://books.toscrape.com/catalogue/")
        details(bookURL)
    return

def process_pages(url):
    cat_page = scan_page(url)
    category_name = cat_page.find("strong").get_text()
    # To collect a list of the div tags that have the books URLs
    csv_path = (data_path / f"{category_name}").with_suffix('.csv')
    with csv_path.open(mode='w') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        writer.writerow(headings)
    phase_two(url)

    while True:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "lxml")
        # Pagination
        next_page_element = soup.select_one('li.next > a')
        if next_page_element:
            next_page_url = next_page_element.get('href')
            url = urljoin(url, next_page_url)
            phase_two(url)

        else:
            break


# if __name__ == '__main__':
