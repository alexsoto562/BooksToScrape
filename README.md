# BooksToScrape
!!!FOR DEMO PURPOSES ONLY, ALL CONTENT ON THIS PAGE IS MADE UP AND HAS NO REAL VALUE!!!

Phase One: Book Data Scraper This script scrapes details for a specific book from books.toscrape.com.

Features:

Fetches book details using a specified URL. Extracts title, UPC, price, quantity, product description, and image URL. Outputs data to book_data.csv. Prerequisites:

Python 3.x Libraries: requests, BeautifulSoup, csv Usage:

bash Copy code pip install requests beautifulsoup4 python <script_name>.py Notes:

Targets: http://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html. Data saved to book_data.csv in script's directory. Error message: "Failed to fetch the webpage". Limitations:

Designed for books.toscrape.com. Always respect robots.txt and terms of service. Phase Two: History Books Data Scraper This script scrapes book details from the History category on books.toscrape.com.

Features:

Fetches a list of books from the History category. Extracts URL, UPC, title, price, quantity, description, and image URL. Outputs data to book_phase_two.csv. Prerequisites:

Python 3.x Libraries: requests, BeautifulSoup, csv Usage:

bash Copy code pip install requests beautifulsoup4 python <script_name>.py Notes:

Targets History category. Data saved to book_phase_two.csv in script's directory. Provides feedback on scraping progress. Converts relative URLs to full URLs. Limitations:

Designed for books.toscrape.com. Always respect robots.txt and terms of service. Phase Three: Comprehensive Book Data Scraper This script scrapes book details from all categories on books.toscrape.com.

Features:

Iterates through every category. Extracts URL, UPC, title, price, quantity, description, category name, and image URL. Outputs data to phase_three_test_five.csv. Prerequisites:

Python 3.x Libraries: requests, BeautifulSoup, csv Usage:

bash Copy code pip install requests beautifulsoup4 python <script_name>.py Notes:

Fetches details for every book in each category. Handles pagination. Provides feedback on scraping progress. Data saved to phase_three_test_five.csv in script's directory. Limitations:

Designed for books.toscrape.com. Always respect robots.txt and terms of service. Phase Four: Book Image Downloader This script uses data from phase_three_test_five.csv to download book images.

Features:

Processes CSV to identify image URLs. Downloads images to phase_four_downloaded_images directory. Sanitizes book titles for filenames. Provides feedback on download progress. Prerequisites:

Python 3.x Libraries: requests, os, csv phase_three_test_five.csv file in the same directory. Usage:

bash Copy code pip install requests python <script_name>.py Notes:

Images saved to phase_four_downloaded_images directory. Images named after sanitized book titles. Requires phase_three_test_five.csv from the previous phase. Limitations:

Assumes PNG image format. Stable network connection required. Adjustments may be needed if CSV structure/content changes.
