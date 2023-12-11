import requests
from bs4 import BeautifulSoup
import csv

base_url = "http://books.toscrape.com/"

# Scrape main page for categories
response = requests.get(base_url + "index.html")
soup = BeautifulSoup(response.content, 'html.parser')
categories = soup.find("div", class_="side_categories").find_all("a")[1:]

def sanitize_filename(filename):
    return "".join([c for c in filename if c.isalpha() or c.isdigit() or c==' ']).rstrip()

# Loop through each category
for category in categories:
    category_name = sanitize_filename(category.get_text().strip())
    filename = f'Phase_Three_{category_name}.csv'
    category_url = base_url + category["href"]
    books_in_category = 0  # Counter to track books in this category
    books_data = []  # Store scraped data for each category

    while category_url:
        response = requests.get(category_url)
        soup = BeautifulSoup(response.content, 'html.parser')

        # Scrape books in the current page
        books = soup.find_all("article", class_="product_pod")
        books_on_this_page = len(books)
        books_in_category += books_on_this_page
        for book in books:
            book_url = base_url + "catalogue/" + book.find("h3").find("a")["href"].replace("../../../", "")
            response_book = requests.get(book_url)
            soup_book = BeautifulSoup(response_book.content, 'html.parser')

            # Extract details and image URL
            image_url = base_url + soup_book.find("div", class_="item active").find("img")["src"].replace("../../..", "")
            description = soup_book.find("meta", {"name": "description"})["content"].strip()

            rating_element = soup_book.find('p', class_='star-rating')
            if rating_element:
                rating_classes = [cls for cls in rating_element['class'] if cls != 'star-rating']
                rating = rating_classes[0] if rating_classes else 'No rating'
                review_rating = {
                    'One': '1/5',
                    'Two': '2/5',
                    'Three': '3/5',
                    'Four': '4/5',
                    'Five': '5/5'
                }.get(rating, '0/5')
            else:
                review_rating = 'No rating/5'

            table = soup_book.find("table", class_="table table-striped")
            details = {row.th.get_text().strip(): row.td.get_text().strip() for row in table.findAll('tr')}

            book_details = {
                "URL": book_url,
                "UPC": details["UPC"],
                "Title": soup_book.h1.get_text(),
                "Price (incl. tax)": details["Price (incl. tax)"],
                "Price (excl. tax)": details["Price (excl. tax)"],
                "Availability": details["Availability"],
                "Product Description": description,
                "Category": category_name,
                "Review Rating" : review_rating,
                "Image URL": image_url
            }

            books_data.append(book_details)

        print(f"Scraped {books_on_this_page} books from page {category_url}")

        # Check for the next page
        next_link = soup.find("li", class_="next")
        if next_link:
            category_url = category_url.rsplit('/', 1)[0] + '/' + next_link.find("a")["href"]
        else:
            category_url = None

    print(f"Completed scraping books from category: {category_name}")
    print("-" * 50)  # separator for clarity

    # Save data to CSV
    filename = f'Phase_Three_{category_name}.csv'
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ["URL", "UPC", "Title", "Price (incl. tax)", "Price (excl. tax)", "Availability", "Product Description", "Category", "Image URL", "Review Rating"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for book in books_data:
            writer.writerow(book)

    print(f"Data saved to {filename}!")
    print("-" * 50)  # separator for clarity

# Updated print statement for accuracy
print("Data saved to CSV files!")