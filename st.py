import os
import json
import time
import requests
from pathlib import Path
from bs4 import BeautifulSoup
import cv2
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st
from PIL import Image
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def extract_images_and_captions(html_file, output_dir):
    """
    Extracts images and their captions from an HTML file.
    Saves images to a specified output directory and returns a list of tuples (image_path, caption).

    Args:
        html_file: File object for the HTML file.
        output_dir: Directory to save extracted images.

    Returns:
        A list of tuples (image_path, caption).
    """

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    pairs = []
    
    try:
        content = html_file.read().decode('utf-8')
    except Exception as e:
        st.error(f"Failed to read the HTML file: {e}")
        return pairs
    
    soup = BeautifulSoup(content, 'html.parser')
    image_paragraphs = soup.find_all('p')
    
    images = []
    captions = []
    
    found_first_image = False
    
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
    
    for idx, img_src in enumerate(images, start=1):
        caption = None
        if idx > 1 and (idx-2) < len(captions):
            caption = captions[idx-2]
        
        try:
            abs_image_path = None
            image_data = None
            
            if img_src.startswith('http://') or img_src.startswith('https://'):
                response = requests.get(img_src)
                response.raise_for_status()
                image_data = response.content
            else:
                abs_image_path = os.path.abspath(os.path.join(os.path.dirname(html_file.name), img_src))
                if not os.path.exists(abs_image_path):
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
                st.error(f"Failed to process image: {img_src}")
        except Exception as e:
            st.error(f"Error processing image {img_src}: {e}")
    
    return pairs

def create_captions_mapping(pairs):
    """Create a dictionary mapping image filenames to captions."""
    captions = {}
    for image_path, caption in pairs:
        filename = os.path.basename(image_path)
        captions[filename] = caption
    return captions

def preprocess_image(image_path, size=(300, 300)):
    """Load and preprocess the image for matching."""
    image = cv2.imread(image_path)
    if image is None:
        st.error(f"Error reading image: {image_path}")
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
        st.error(f"No images found in folder1: {folder1}")
    if not images_folder2:
        st.error(f"No images found in folder2: {folder2}")
    
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
        st.warning("No matches found.")
        return
    
    for img1_path, img2_path, match_count, caption in matches:
        img1 = cv2.imread(str(img1_path))
        img2 = cv2.imread(str(img2_path))
        
        if img1 is None or img2 is None:
            st.error(f"Error loading images: {img1_path} or {img2_path}")
            continue
        
        img1_rgb = cv2.cvtColor(img1, cv2.COLOR_BGR2RGB)
        img2_rgb = cv2.cvtColor(img2, cv2.COLOR_BGR2RGB)
        
        img1_rgb_resized, img2_rgb_resized = resize_to_common_height(img1_rgb, img2_rgb)
        
        combined_img = np.hstack((img1_rgb_resized, img2_rgb_resized))
        
        st.image(combined_img, caption=f"Match Count: {match_count}\nCaption: {caption if caption else 'No caption'}", use_column_width=True)

def create_mapping_from_matches(matches):
    """Create a dictionary mapping image filenames to captions based on matched images."""
    mapping = {}
    for img1_path, img2_path, score, caption in matches:
        img2_filename = os.path.basename(img2_path)
        mapping[img2_filename] = caption if caption else "No caption"
    return mapping

def init_driver():
    chrome_options = Options()
    driver_service = Service(CHROME_DRIVER_PATH)
    driver = webdriver.Chrome(service=driver_service, options=chrome_options)
    return driver

def login_to_wordpress(driver, username, password):
    driver.get("https://wp.thecollector.com/wp-login.php")
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'user_login'))).send_keys(username)
    driver.find_element(By.ID, 'user_pass').send_keys(password)
    driver.find_element(By.ID, 'wp-submit').click()
    WebDriverWait(driver, 10).until(EC.title_contains("Dashboard"))

def navigate_to_media_library(driver):
    driver.get("https://wp.thecollector.com/wp-admin/upload.php?mode=list")
    WebDriverWait(driver, 10).until(EC.title_contains("Media Library"))

def upload_image(driver, image_path):
    driver.get("https://wp.thecollector.com/wp-admin/media-new.php?browser-uploader")
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//input[starts-with(@id,'html5_')]"))
    ).send_keys(image_path)
    time.sleep(10)

def add_caption(driver, caption_text):
    if caption_text == "No caption":
        return
    
    try:
        navigate_to_media_library(driver)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".wp-list-table")))
        image_link = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".wp-list-table .title a"))
        )
        image_link.click()
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'attachment_caption')))
        caption_input = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, 'attachment_caption'))
        )
        caption_input.clear()
        caption_input.send_keys(caption_text)
        update_button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, 'publish'))
        )
        driver.execute_script("arguments[0].scrollIntoView(true);", update_button)
        WebDriverWait(driver, 10).until_not(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".loading-overlay"))
        )
        driver.execute_script("arguments[0].click();", update_button)
    except Exception as e:
        st.error(f"An error occurred while adding caption: {e}")

# Streamlit interface
st.title("Image Extraction and Captioning Tool")

uploaded_html = st.file_uploader("Upload HTML file", type=["html"])
if uploaded_html:
    output_directory = "extracted_images"
    pairs = extract_images_and_captions(uploaded_html, output_directory)
    
    if pairs:
        st.write(f"Extracted {len(pairs)} images and captions.")
        for image_path, caption in pairs:
            st.image(image_path, caption=f"Caption: {caption if caption else 'No caption'}")
    else:
        st.warning("No images or captions were extracted.")
    
    folder2 = st.text_input("Enter the path to the Folder with high res images", "")
    
    if folder2:
        captions = create_captions_mapping(pairs)
        matched_images = match_images_with_captions(output_directory, folder2, captions)
        visualize_matches_with_captions(matched_images)
    
    if st.button("Start WordPress Upload"):
        CHROME_DRIVER_PATH = st.text_input("Enter the path to your ChromeDriver executable", "")
        username = st.text_input("Enter your WordPress username", "")
        password = st.text_input("Enter your WordPress password", "")
        
        if CHROME_DRIVER_PATH and username and password:
            driver = init_driver()
            try:
                login_to_wordpress(driver, username, password)
                for image_filename in os.listdir(folder2):
                    image_path = os.path.join(folder2, image_filename)
                    caption_text = captions.get(image_filename, "No caption")
                    upload_image(driver, image_path)
                    time.sleep(10)
                    add_caption(driver, caption_text)
            finally:
                driver.quit()
            st.success("Upload and captioning completed.")
else:
    st.warning("Please upload an HTML file.")
