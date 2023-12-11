import csv
import requests
import os

# Helper function to sanitize the title for use as a filename
def sanitize_filename(filename):
    # Remove characters that are invalid for filenames
    sanitized = ''.join(c for c in filename if c.isalnum() or c in (' ', '.', '_')).rstrip()
    return sanitized

# Create a directory to store the images if it doesn't exist
if not os.path.exists('phase_four_downloaded_images'):
    os.makedirs('phase_four_downloaded_images')

# Load data from CSV
with open('phase_three_test_five.csv', 'r', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    books_data = [row for row in reader]

# Initialize an empty string for category tracking
prev_category = ""

# Loop through the books data to download images
for book in books_data:
    image_url = book["Image URL"]
    response_image = requests.get(image_url, stream=True)
    
    # Check if the request was successful
    if response_image.status_code == 200:
        sanitized_title = sanitize_filename(book["Title"])
        image_filename = os.path.join('phase_four_downloaded_images', sanitized_title + ".png")
        
        # Save the image
        with open(image_filename, 'wb') as img_file:
            for chunk in response_image.iter_content(1024):
                img_file.write(chunk)
                
    # Check if we've moved on to a new category
    if prev_category != book["Category"]:
        if prev_category:  # if prev_category is not an empty string
            print(f"Finished downloading images for category: {prev_category}")
        prev_category = book["Category"]

# Print for the last category after exiting the loop
print(f"Finished downloading images for category: {prev_category}")

print("All images downloaded!")
