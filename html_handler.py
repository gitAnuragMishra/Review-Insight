from bs4 import BeautifulSoup #type: ignore
from datetime import datetime
import os
import yaml #type: ignore


with open('config.yaml', 'r') as file:
    config = yaml.safe_load(file)


def save_uploaded_file(uploaded_files, save_folder):
    # Create the folder if it doesn't exist
    if not os.path.exists(save_folder):
        os.makedirs(save_folder)

    saved_file_paths = []
    
    # Save each uploaded file
    for uploaded_file in uploaded_files:
        file_path = os.path.join(save_folder, uploaded_file.name)
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        saved_file_paths.append(file_path)

    return saved_file_paths


def extract_product_name(uploaded_html_files):
    product_names = []
    for file in uploaded_html_files:
        product_names.append(file.name.replace('.html', ' ').replace('_ Amazon.in_', '')) # file.name is a string #learnt a new thing, we can chain .replace() wow!!
    return product_names

def extract_reviews_from_files(folder_path) -> list:
    all_reviews = []

    # Get a list of all HTML files in the folder
    file_paths = [os.path.join(folder_path, file) for file in os.listdir(folder_path) if file.endswith('.html')]

    for file_path in file_paths:
        with open(file_path, 'r', encoding='utf-8') as file:
            file_content = file.read()

        soup = BeautifulSoup(file_content, 'html.parser')

        # reviews = soup.find_all('span', {'data-hook': 'review-body'})
        # all_reviews.extend([review.get_text(strip=True) for review in reviews])
        review_elements = soup.find_all('div', {'data-hook': 'review'})
        for review in review_elements:
            title_element = review.find('a', {'data-hook': 'review-title'})
            body_element = review.find('span', {'data-hook': 'review-body'})
            
            if title_element and body_element:
                title = title_element.get_text(strip=True)
                body = body_element.get_text(strip=True)
                all_reviews.append(f"{title}. {body}")


    return all_reviews


def extract_product_descriptions_from_folder(folder_path) -> list:
    product_descriptions = []

    # Loop through all HTML files in the folder
    for filename in os.listdir(folder_path):
        if filename.endswith(".html"):
            file_path = os.path.join(folder_path, filename)
            with open(file_path, 'r', encoding='utf-8') as file:
                html_content = file.read()

            # Parse the HTML content
            soup = BeautifulSoup(html_content, 'html.parser')

            # Extract the product description
            product_description = soup.find('div', {'id': 'feature-bullets'})
            if product_description:
                description_text = product_description.get_text(separator=" ", strip=True)
                product_descriptions.append(description_text)
            else:
                product_descriptions.append("Product description not found.")

    return product_descriptions

