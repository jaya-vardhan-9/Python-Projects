import os
import csv
import time
import logging
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Setup logging for debugging
logging.basicConfig(level=logging.INFO)

# Initialize the WebDriver
service = Service(executable_path="C:\\Users\\jaiva\\Downloads\\Compressed\\chromedriver-win64\\chromedriver-win64\\chromedriver.exe")  # Adjust the path to your chromedriver
driver = webdriver.Chrome(service=service)

# Instagram login URL
instagram_url = "https://www.instagram.com"

# Use environment variables or a config file to store credentials securely
USERNAME = os.getenv("INSTAGRAM_USERNAME", "alsotamarina")
PASSWORD = os.getenv("INSTAGRAM_PASSWORD", "Jaya@1404")

try:
    # Navigate to Instagram
    driver.get(instagram_url)
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "username")))

    # Login process
    username = driver.find_element(By.NAME, "username")
    password = driver.find_element(By.NAME, "password")

    username.clear()
    password.clear()

    username.send_keys(USERNAME)
    password.send_keys(PASSWORD)

    login_button = driver.find_element(By.XPATH, '//*[@id="loginForm"]/div/div[3]')
    login_button.click()

    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "x1i10hfl")))

    # Handling pop-ups
    not_now = driver.find_element(By.CLASS_NAME, "x1i10hfl")
    not_now.click()

    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "_a9_1")))
    not_now = driver.find_element(By.CLASS_NAME, "_a9_1")
    not_now.click()

    # Locate and click the search box
    search_box = driver.find_element(By.XPATH, "//input[@placeholder='Search']")
    search_box.send_keys('Link in bio', Keys.ENTER)

    # Wait for search results to load
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "x4k7w5x")))

    results = driver.find_elements(By.CLASS_NAME, "x4k7w5x")
    usernames = [result.text.strip() for result in results]

    urls = set()
    for username in usernames:
        if ' ' not in username:
            profile_url = f"https://www.instagram.com/{username}/"
            driver.get(profile_url)
            time.sleep(2)

            try:
                # Find the link in bio
                bio_link = driver.find_element(By.XPATH, "//section/main/div/header/section/div[3]/div[3]/div/a/span/span")
                link_text = bio_link.text
                if link_text.startswith("t.") or link_text.startswith("telegram."):
                    urls.add(link_text)
                    logging.info(f"URL found: {link_text} (from {username})")
            except NoSuchElementException:
                logging.warning(f"No link found in the bio for {username}")

            if len(urls) >= 15:
                break

    # Create the path where the CSV file should be saved
    csv_directory = "C:\\Users\\jaiva\\Downloads"  # Adjust this to your desired location
    if not os.path.exists(csv_directory):
        os.makedirs(csv_directory)  # Create the directory if it doesn't exist
    
    # CSV file path
    csv_file = os.path.join(csv_directory, "urls.csv")

    # Writing URLs to the CSV file
    with open(csv_file, 'w', newline='', encoding="utf-8") as file:
        writer = csv.writer(file)
        for url in urls:
            writer.writerow([url])

except Exception as e:
    logging.error(f"An error occurred: {e}")

finally:
    # Ensure the driver is closed at the end
    driver.quit()