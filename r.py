import streamlit as st

# Title of the app
st.title('Simple Web App')

# Input from the user
name = st.text_input("Enter your name:")

# Button to submit
if st.button("Submit"):
    st.write(f"Hello, {name}!")



# Extracting Captions with Images - doesn't work well!!!

# import os
# from bs4 import BeautifulSoup
# import requests

# def extract_images_and_captions(html_path, output_dir):
#     """
#     Extracts images and their captions from an HTML file.
#     Saves images to a specified output directory and returns a list of tuples (image_path, caption).

#     Args:
#         html_path: Path to the HTML file.
#         output_dir: Directory to save extracted images.

#     Returns:
#         A list of tuples (image_path, caption).
#     """

#     if not os.path.exists(output_dir):
#         os.makedirs(output_dir)
#     print(f"Output directory created or already exists: {output_dir}")

#     pairs = []

#     try:
#         with open(html_path, 'r', encoding='utf-8') as f:
#             content = f.read()
#         print(f"Successfully read HTML file: {html_path}")
#     except Exception as e:
#         print(f"Failed to read the HTML file: {e}")
#         return pairs

#     soup = BeautifulSoup(content, 'html.parser')

#     images = soup.find_all('img')
#     image_paragraphs = soup.find_all('p')

#     captions = []
#     found_first_image = False

#     for paragraph in image_paragraphs:
#         img_tag = paragraph.find('img')
        
#         if img_tag:
#             span_tags = paragraph.find_all('span')
#             if len(span_tags) > 1:
#                 if found_first_image:
#                     caption_text = ' '.join(span.get_text(strip=True) for span in span_tags)
#                     if caption_text:
#                         captions.append(caption_text)
#                 else:
#                     found_first_image = True
#             else:
#                 if found_first_image:
#                     next_p = paragraph.find_next_sibling('p')
#                     if next_p:
#                         caption_text = next_p.get_text(strip=True)
#                         captions.append(caption_text)
#                 else:
#                     found_first_image = True

#     # Start processing from the second image
#     for idx, img in enumerate(images, start=1):
#         img_src = img.get('src', None)
#         if not img_src:
#             print(f"Image {idx} has no 'src' attribute.")
#             continue

#         # Skip caption for the first image
#         caption = None
#         if idx > 1 and (idx-2) < len(captions):
#             caption = captions[idx-2]
        
#         print(f"Processing image {idx}: {img_src} with caption {caption}")

#         try:
#             abs_image_path = None
#             image_data = None

#             if img_src.startswith('http://') or img_src.startswith('https://'):
#                 response = requests.get(img_src)
#                 response.raise_for_status()
#                 image_data = response.content
#             else:
#                 abs_image_path = os.path.abspath(os.path.join(os.path.dirname(html_path), img_src))
#                 if not os.path.exists(abs_image_path):
#                     print(f"File not found: {abs_image_path}")
#                     continue
#                 with open(abs_image_path, 'rb') as img_file:
#                     image_data = img_file.read()

#             if image_data:
#                 image_name = f'image_{idx}.jpg'
#                 image_path = os.path.join(output_dir, image_name)
#                 with open(image_path, 'wb') as f:
#                     f.write(image_data)
#                 pairs.append((image_path, caption))
#             else:
#                 print(f"Failed to process image: {img_src}")
#         except Exception as e:
#             print(f"Error processing image {img_src}: {e}")

#     return pairs

# def get_output_directory(html_path):
#     """
#     Given the path to an HTML file, return the path to the output directory.
    
#     Args:
#         html_path (str): The path to the HTML file.
    
#     Returns:
#         str: The path to the output directory.
#     """
#     if not os.path.isfile(html_path):
#         raise ValueError("The provided HTML file path is not valid.")
    
#     # Generate the output directory path based on the HTML file path
#     output_directory = os.path.join(os.path.dirname(html_path), 'extracted_images')
#     return output_directory



# # Example usage with corrected paths
# html_path = input("Enter the path to the HTML: ").strip().strip('"')
# output_directory = get_output_directory(html_path)

# pairs = extract_images_and_captions(html_path, output_directory)
# if pairs:
#     for image_path, caption in pairs:
#         print(f"Image: {image_path}, Caption: {caption}")
# else:
#     print("No images or captions were processed.")

# Extracting Captions with Images - Works but with 1st condition only!!!

# import os
# from bs4 import BeautifulSoup
# import requests

# def extract_images_and_captions(html_path, output_dir):
#     """
#     Extracts images and their captions from an HTML file.
#     Saves images to a specified output directory and returns a list of tuples (image_path, caption).

#     Args:
#         html_path: Path to the HTML file.
#         output_dir: Directory to save extracted images.

#     Returns:
#         A list of tuples (image_path, caption).
#     """

#     if not os.path.exists(output_dir):
#         os.makedirs(output_dir)
#     print(f"Output directory created or already exists: {output_dir}")

#     pairs = []

#     try:
#         with open(html_path, 'r', encoding='utf-8') as f:
#             content = f.read()
#         print(f"Successfully read HTML file: {html_path}")
#     except Exception as e:
#         print(f"Failed to read the HTML file: {e}")
#         return pairs

#     soup = BeautifulSoup(content, 'html.parser')

#     images = soup.find_all('img')
#     image_paragraphs = soup.find_all('p')

#     captions = []
#     found_first_image = False

#     for paragraph in image_paragraphs:
#         img_tag = paragraph.find('img')
        
#         if img_tag:
#             if found_first_image:
#                 next_p = paragraph.find_next_sibling('p')
#                 if next_p:
#                     caption_text = next_p.get_text(strip=True)
#                     captions.append(caption_text)
#             else:
#                 found_first_image = True

#     # Process images and associate captions
#     for idx, img in enumerate(images, start=1):
#         img_src = img.get('src', None)
#         if not img_src:
#             print(f"Image {idx} has no 'src' attribute.")
#             continue

#         # Skip caption for the first image
#         caption = None
#         if idx > 1 and (idx-2) < len(captions):
#             caption = captions[idx-2]
        
#         print(f"Processing image {idx}: {img_src} with caption {caption}")

#         try:
#             abs_image_path = None
#             image_data = None

#             if img_src.startswith('http://') or img_src.startswith('https://'):
#                 response = requests.get(img_src)
#                 response.raise_for_status()
#                 image_data = response.content
#             else:
#                 abs_image_path = os.path.abspath(os.path.join(os.path.dirname(html_path), img_src))
#                 if not os.path.exists(abs_image_path):
#                     print(f"File not found: {abs_image_path}")
#                     continue
#                 with open(abs_image_path, 'rb') as img_file:
#                     image_data = img_file.read()

#             if image_data:
#                 image_name = f'image_{idx}.jpg'
#                 image_path = os.path.join(output_dir, image_name)
#                 with open(image_path, 'wb') as f:
#                     f.write(image_data)
#                 pairs.append((image_path, caption))
#             else:
#                 print(f"Failed to process image: {img_src}")
#         except Exception as e:
#             print(f"Error processing image {img_src}: {e}")

#     return pairs


# def get_output_directory(html_path):
#     """
#     Given the path to an HTML file, return the path to the output directory.
    
#     Args:
#         html_path (str): The path to the HTML file.
    
#     Returns:
#         str: The path to the output directory.
#     """
#     if not os.path.isfile(html_path):
#         raise ValueError("The provided HTML file path is not valid.")
    
#     # Generate the output directory path based on the HTML file path
#     output_directory = os.path.join(os.path.dirname(html_path), 'extracted_images')
#     return output_directory



# # Example usage with corrected paths
# html_path = input("Enter the path to the HTML: ").strip().strip('"')
# output_directory = get_output_directory(html_path)

# pairs = extract_images_and_captions(html_path, output_directory)
# if pairs:
#     for image_path, caption in pairs:
#         print(f"Image: {image_path}, Caption: {caption}")
# else:
#     print("No images or captions were processed.")

    
    
    

# Trying to Add Spaces where there are multiple Span Tags

import os
from bs4 import BeautifulSoup
import requests

def extract_images_and_captions(html_path, output_dir):
    """
    Extracts images and their captions from an HTML file.
    Saves images to a specified output directory and returns a list of tuples (image_path, caption).

    Args:
        html_path: Path to the HTML file.
        output_dir: Directory to save extracted images.

    Returns:
        A list of tuples (image_path, caption).
    """

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    print(f"Output directory created or already exists: {output_dir}")

    pairs = []

    try:
        with open(html_path, 'r', encoding='utf-8') as f:
            content = f.read()
        print(f"Successfully read HTML file: {html_path}")
    except Exception as e:
        print(f"Failed to read the HTML file: {e}")
        return pairs

    soup = BeautifulSoup(content, 'html.parser')

    # Find all <p> tags
    image_paragraphs = soup.find_all('p')

    # Initialize lists
    images = []
    captions = []

    found_first_image = False

    # Extract captions and images
    for paragraph in image_paragraphs:
        img_tag = paragraph.find('img')
        if img_tag:
            img_src = img_tag.get('src', None)
            if img_src:
                images.append(img_src)
            if found_first_image:
                next_p = paragraph.find_next_sibling('p')
                if next_p:
                    caption_text = ''.join([
                        segment if segment.endswith(' ') else segment + ' '
                        for segment in next_p.stripped_strings
                    ]).strip()
                    captions.append(caption_text)
            else:
                found_first_image = True

    # Process images and associate captions
    for idx, img_src in enumerate(images, start=1):
        caption = None
        if idx > 1 and (idx-2) < len(captions):
            caption = captions[idx-2]

        print(f"Processing image {idx}: {img_src} with caption '{caption}'")

        try:
            abs_image_path = None
            image_data = None

            if img_src.startswith('http://') or img_src.startswith('https://'):
                response = requests.get(img_src)
                response.raise_for_status()
                image_data = response.content
            else:
                abs_image_path = os.path.abspath(os.path.join(os.path.dirname(html_path), img_src))
                if not os.path.exists(abs_image_path):
                    print(f"File not found: {abs_image_path}")
                    continue
                with open(abs_image_path, 'rb') as img_file:
                    image_data = img_file.read()

            if image_data:
                image_name = f'image_{idx}.jpg'
                image_path = os.path.join(output_dir, image_name)
                with open(image_path, 'wb') as f:
                    f.write(image_data)
                pairs.append((image_path, caption))
            else:
                print(f"Failed to process image: {img_src}")
        except Exception as e:
            print(f"Error processing image {img_src}: {e}")

    return pairs

def get_output_directory(html_path):
    """
    Given the path to an HTML file, return the path to the output directory.
    
    Args:
        html_path (str): The path to the HTML file.
    
    Returns:
        str: The path to the output directory.
    """
    if not os.path.isfile(html_path):
        raise ValueError("The provided HTML file path is not valid.")
    
    # Generate the output directory path based on the HTML file path
    output_directory = os.path.join(os.path.dirname(html_path), 'extracted_images')
    return output_directory

# Example usage with user input
html_path = input("Enter the path to the HTML: ").strip().strip('"')
output_directory = get_output_directory(html_path)

pairs = extract_images_and_captions(html_path, output_directory)
if pairs:
    for image_path, caption in pairs:
        print(f"Image: {image_path}, Caption: {caption}")
else:
    print("No images or captions were processed.")


# With JSON and ORB - My old Workflow

import os
from pathlib import Path
import cv2
import numpy as np
import matplotlib.pyplot as plt

def preprocess_image(image_path, size=(300, 300)):
    """Load and preprocess the image for matching."""
    image = cv2.imread(image_path)
    if image is None:
        print(f"Error reading image: {image_path}")
        return None
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    resized_image = cv2.resize(gray_image, size)
    return resized_image

def compute_orb_matches(image1, image2):
    """Compute the ORB matches between two images."""
    orb = cv2.ORB_create()
    kp1, des1 = orb.detectAndCompute(image1, None)
    kp2, des2 = orb.detectAndCompute(image2, None)
    bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
    matches = bf.match(des1, des2)
    matches = sorted(matches, key=lambda x: x.distance)
    return matches

def match_images_with_captions(folder1, folder2, captions):
    """Match images between two folders using ORB and associate captions."""
    images_folder1 = list(Path(folder1).glob('*.*'))
    images_folder2 = list(Path(folder2).glob('*.*'))
    
    if not images_folder1:
        print(f"No images found in folder1: {folder1}")
    if not images_folder2:
        print(f"No images found in folder2: {folder2}")
    
    matches = []
    for img1_path in images_folder1:
        img1_preprocessed = preprocess_image(str(img1_path))
        if img1_preprocessed is None:
            continue
        
        best_match = None
        best_match_count = -1
        
        for img2_path in images_folder2:
            img2_preprocessed = preprocess_image(str(img2_path))
            if img2_preprocessed is None:
                continue
            
            orb_matches = compute_orb_matches(img1_preprocessed, img2_preprocessed)
            match_count = len(orb_matches)
            
            if match_count > best_match_count:
                best_match_count = match_count
                best_match = img2_path
        
        if best_match:
            img1_filename = os.path.basename(img1_path)
            caption = captions.get(img1_filename, None)
            matches.append((img1_path, best_match, best_match_count, caption))
    
    return matches

def create_captions_mapping(pairs):
    """Create a dictionary mapping image filenames to captions."""
    captions = {}
    for image_path, caption in pairs:
        filename = os.path.basename(image_path)
        captions[filename] = caption
    return captions

def resize_to_common_height(img1, img2):
    """Resize images to have the same height."""
    height1, width1 = img1.shape[:2]
    height2, width2 = img2.shape[:2]
    
    common_height = min(height1, height2)
    new_width1 = int((common_height / height1) * width1)
    new_width2 = int((common_height / height2) * width2)
    
    img1_resized = cv2.resize(img1, (new_width1, common_height))
    img2_resized = cv2.resize(img2, (new_width2, common_height))
    
    return img1_resized, img2_resized

def visualize_matches_with_captions(matches):
    """Visualize the matched images with captions side by side."""
    if not matches:
        print("No matches found.")
        return
    
    for img1_path, img2_path, match_count, caption in matches:
        img1 = cv2.imread(str(img1_path))
        img2 = cv2.imread(str(img2_path))
        
        if img1 is None or img2 is None:
            print(f"Error loading images: {img1_path} or {img2_path}")
            continue
        
        img1_rgb = cv2.cvtColor(img1, cv2.COLOR_BGR2RGB)
        img2_rgb = cv2.cvtColor(img2, cv2.COLOR_BGR2RGB)
        
        img1_rgb_resized, img2_rgb_resized = resize_to_common_height(img1_rgb, img2_rgb)
        
        combined_img = np.hstack((img1_rgb_resized, img2_rgb_resized))
        
        plt.figure(figsize=(12, 6))
        plt.title(f"Match Count: {match_count}\nCaption: {caption if caption else 'No caption'}")
        plt.imshow(combined_img)
        plt.axis('off')
        plt.show()

# Example usage
folder1 = output_directory
folder2 = input("Enter the path to the Folder with high res images: ").strip().strip('"')


pairs = extract_images_and_captions(html_path, output_directory)
captions = create_captions_mapping(pairs)

matched_images = match_images_with_captions(output_directory, folder2, captions)
visualize_matches_with_captions(matched_images)


def create_mapping_from_matches(matches):
    """Create a dictionary mapping image filenames to captions based on matched images."""
    mapping = {}
    for img1_path, img2_path, score, caption in matches:
        # Use the filename from the Moula folder (img2_path)
        img2_filename = os.path.basename(img2_path)
        mapping[img2_filename] = caption if caption else "No caption"
    return mapping

# Example usage
# Assuming `matched_images` contains the matched results with captions
mapping_from_matches = create_mapping_from_matches(matched_images)

# Print or use the mapping as needed
for filename, caption in mapping_from_matches.items():
    print(f"{filename}: {caption}")

# Optional: Save the mapping to a file for later use
import json
mapping_file_path = r"C:\Users\User\Desktop\mapping_from_matches.json"
with open(mapping_file_path, 'w') as file:
    json.dump(mapping_from_matches, file, indent=4)


from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os
import json

# Path to your ChromeDriver executable
CHROME_DRIVER_PATH = r'C:\Users\User\Desktop\iRonhack\Final Project\chromedriver-win64\chromedriver.exe'

# Load the captions mapping from a JSON file
mapping_file_path = r"C:\Users\User\Desktop\mapping_from_matches.json"
with open(mapping_file_path, 'r') as file:
    captions_dict = json.load(file)

def init_driver():
    chrome_options = Options()
    driver_service = Service(CHROME_DRIVER_PATH)
    driver = webdriver.Chrome(service=driver_service, options=chrome_options)
    return driver

def login_to_wordpress(driver):
    print("Prompting for WordPress username and password...")  # Debugging line
    username = input("Enter your WordPress username: ")
    password = input("Enter your WordPress password: ")

    print("Attempting to login to WordPress...")  # Debugging line
    driver.get("https://wp.thecollector.com/wp-login.php")
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'user_login'))).send_keys(username)
    driver.find_element(By.ID, 'user_pass').send_keys(password)
    driver.find_element(By.ID, 'wp-submit').click()
    WebDriverWait(driver, 10).until(EC.title_contains("Dashboard"))
    print("Login successful")

def navigate_to_media_library(driver):
    driver.get("https://wp.thecollector.com/wp-admin/upload.php?mode=list")
    WebDriverWait(driver, 10).until(EC.title_contains("Media Library"))
    print("Navigated to media library in list mode")

def upload_image(driver, image_path):
    driver.get("https://wp.thecollector.com/wp-admin/media-new.php?browser-uploader")
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//input[starts-with(@id,'html5_')]"))
    ).send_keys(image_path)
    time.sleep(10)  # Adjust based on file size and network speed
    print(f"Uploaded image: {image_path}")




def add_caption(driver, caption_text):
    if caption_text == "No caption":
        print("No caption available for this image.")
        return  # Skip captioning if there's no caption
    
    try:
        navigate_to_media_library(driver)
        
        # Wait for the list of images to be visible
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".wp-list-table")))
        
        # Wait for and click the most recent image (first row's image link)
        image_link = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".wp-list-table .title a"))
        )
        image_link.click()
        
        # Wait for the edit page to load and the caption field to be interactable
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'attachment_caption')))
        caption_input = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, 'attachment_caption'))
        )
        
        caption_input.clear()
        caption_input.send_keys(caption_text)
        
        # Scroll to the "Update" button to ensure it's in view
        update_button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, 'publish'))
        )
        driver.execute_script("arguments[0].scrollIntoView(true);", update_button)
        
        # Wait for any potential loading overlays to disappear
        WebDriverWait(driver, 10).until_not(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".loading-overlay"))
        )
        
        # Click the "Update" button using JavaScript if normal clicking fails
        driver.execute_script("arguments[0].click();", update_button)
        
        print(f"Added caption: {caption_text}")
    except Exception as e:
        print(f"An error occurred while adding caption: {e}")

def main():
    driver = init_driver()
    try:
        login_to_wordpress(driver)
        
       # image_folder = folder2 #es shevcvale me
        
        for image_filename in os.listdir(folder2):          # ak image_foder shevcvale
            image_path = os.path.join(folder2, image_filename)          # akac
            
            # Extract the caption from the dictionary, if it exists
            caption_text = captions_dict.get(image_filename, "No caption")
            
            upload_image(driver, image_path)
            time.sleep(10)  # Ensure the image is fully uploaded
            
            add_caption(driver, caption_text)
            
    finally:
        driver.quit()

if __name__ == "__main__":
    main()




