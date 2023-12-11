import requests
from bs4 import BeautifulSoup
import csv

scrape_url = 'http://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html'
webpage_response = requests.get(scrape_url)

if webpage_response.status_code == 200:
    soup = BeautifulSoup(webpage_response.content, 'html.parser')

    title_element = soup.find('h1')
    book_title = title_element.get_text().strip()  # Changed from book_title_class

    product_info_table = soup.find('table', class_='table table-striped')

    upc = product_info_table.find('th', string='UPC').find_next('td').get_text().strip()

    price_incl_tax = product_info_table.find('th', string='Price (incl. tax)').find_next('td').get_text().strip()

    price_excl_tax = product_info_table.find('th', string='Price (excl. tax)').find_next('td').get_text().strip()

    quantity_available = product_info_table.find('th', string="Availability").find_next('td').get_text().strip()

    product_description_element = soup.find('div', id='product_description')
    product_description = product_description_element.find_next('p').get_text().strip() if product_description_element else 'No description'

    img_url_element = soup.find('div', id='product_gallery').find('img')
    img_url = 'http://books.toscrape.com/' + img_url_element['src'].lstrip('/') if img_url_element else 'No image URL'

    rating_element = soup.find('p', class_='star-rating')
    if rating_element:
        rating_classes = [class_ for class_ in rating_element['class'] if class_ != 'star-rating']
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

    with open('Phase_One.csv', 'w', newline='') as csvfile:
        fieldnames = ['URL', 'Title', 'UPC', 'Price (incl. tax)', 'Price (excl. tax)', 'Quantity Available', 'Product Description', 'Category', 'Review Rating', 'Image URL']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        writer.writerow({
            'URL': scrape_url,
            'Title': book_title,  # Use book_title
            'UPC': upc, 
            'Price (incl. tax)': price_incl_tax, 
            'Price (excl. tax)': price_excl_tax, 
            'Quantity Available': quantity_available, 
            'Product Description': product_description, 
            'Category': 'Poetry',
            'Review Rating': review_rating, 
            'Image URL': img_url
        })

else:
    print("Failed to fetch the webpage")
