import os
import csv
import time
import logging
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException, TimeoutException, WebDriverException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# Setup logging for debugging
logging.basicConfig(level=logging.INFO)

def get_instagram_links(username, password):
    # Initialize the WebDriver
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)

    try:
        # Navigate to Instagram
        driver.get("https://www.instagram.com/accounts/login/")
        
        # Wait for the login form to load
        wait = WebDriverWait(driver, 10)
        wait.until(EC.presence_of_element_located((By.NAME, "username")))

        # Find username and password fields and fill them
        driver.find_element(By.NAME, "username").send_keys(username)
        driver.find_element(By.NAME, "password").send_keys(password)

        # Find the login button and click it
        driver.find_element(By.XPATH, '//*[@id="loginForm"]/div/div[3]/button').click()

        # Wait for the main page to load
        wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="react-root"]/section/main')))
        logging.info("Logged in successfully")

        # Handle "Not Now" pop-ups
        try:
            wait.until(EC.presence_of_element_located((By.CLASS_NAME, "x1i10hfl"))).click()
            wait.until(EC.presence_of_element_located((By.CLASS_NAME, "_a9_1"))).click()
        except TimeoutException:
            logging.info("No 'Not Now' pop-up appeared")

        # Locate and click the search box
        search_box = driver.find_element(By.XPATH, "//input[@placeholder='Search']")
        search_box.send_keys('Link in bio', Keys.ENTER)

        # Wait for search results to load
        wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "x4k7w5x")))

        results = driver.find_elements(By.CLASS_NAME, "x4k7w5x")
        usernames = [result.text.strip() for result in results if ' ' not in result.text.strip()]

        urls = set()
        for username in usernames:
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
        csv_directory = "D:\\Python Projects\\Gothams Project"  # Adjust this to your desired location
        if not os.path.exists(csv_directory):
            os.makedirs(csv_directory)  # Create the directory if it doesn't exist
        
        # CSV file path
        csv_file = os.path.join(csv_directory, "urls.csv")

        # Writing URLs to the CSV file
        with open(csv_file, 'w', newline='', encoding="utf-8") as file:
            writer = csv.writer(file)
            for url in urls:
                writer.writerow([url])

    except (TimeoutException, WebDriverException, Exception) as e:
        logging.error(f"An error occurred: {e}")

    finally:
        # Ensure the driver is closed at the end
        driver.quit()

if __name__ == "__main__":
    user_username = input("Enter your Instagram username: ")
    user_password = input("Enter your Instagram password: ")
    get_instagram_links(user_username, user_password)
