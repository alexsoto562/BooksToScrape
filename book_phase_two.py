import requests
from bs4 import BeautifulSoup
import csv

# Initial request to fetch the list of books
response = requests.get("http://books.toscrape.com/catalogue/category/books/history_32/index.html")

# Check if our request was successful
if response.status_code == 200:
    print("Successfully fetched the web page!")
else:
    print("Failed to retrieve the page.")
    exit()

soup = BeautifulSoup(response.content, 'html.parser')

# Base URL for constructing full book URLs
base_url = "http://books.toscrape.com/catalogue/"

# Create or overwrite a CSV file to save the data
with open("Phase_Two.csv", "w", newline="") as csvfile:
    fieldnames = ["URL", "UPC", "Book Title", "Price (incl. tax)", "Price (excl. tax)", "Quantity Available", "Product Description", "Category" , "Review Rating", "Image URL"]

    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()  # Write the headers

    # Loop through each book
    for book in soup.find_all("article", class_="product_pod"):
        # Retrieve book URL and title
        book_url_fragment = book.find("h3").find("a")["href"]
        full_book_url = base_url + book_url_fragment.replace("../../../", "")
        book_title = book.find("h3").find("a")["title"]

        # Fetch details of the book using the constructed URL
        response_book = requests.get(full_book_url)
        if response_book.status_code != 200:
            print(f"Failed to retrieve details for book: {book_title}")
            continue

        soup_book = BeautifulSoup(response_book.content, 'html.parser')
        img_url = base_url + soup_book.find("div", class_="item active").find("img")["src"].replace("../../", "")
        description = soup_book.find("meta", attrs={"name": "description"})["content"].strip()

        availability_paragraph = soup_book.find("p", class_="instock availability")
        availability_text = availability_paragraph.get_text(strip=True)  # This fetches "In stock"

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

        # Create a dictionary to store details for this book
        book_details = {
            "URL": full_book_url,
            "Book Title": book_title,
            "Quantity Available" : availability_text,
            "Product Description": description,
            "Category" : "History",
            "Review Rating" : review_rating,
            "Image URL": img_url
        }

        # Extract details from the table
        table = soup_book.find("table", class_="table table-striped")
        for row in table.find_all("tr"):
            header = row.find("th").get_text().strip()
            value = row.find("td").get_text().strip()
            # Map the headers to our desired CSV column headers
            if header == "UPC":
                book_details["UPC"] = value
            elif header == "Price (incl. tax)":
                book_details["Price (incl. tax)"] = value
            elif header == "Price (excl. tax)":
                book_details["Price (excl. tax)"] = value

        # Write the book's details to the CSV
        writer.writerow(book_details)

print("Book details have been saved to Phase_Two.csv!")
