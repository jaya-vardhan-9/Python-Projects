from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time

# Prompt the user for their Instagram username and password
user_username = input("Enter your Instagram username: ")
user_password = input("Enter your Instagram password: ")

# Set up the WebDriver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

try:
    # Open Instagram login page
    driver.get("https://www.instagram.com/accounts/login/")

    # Wait for the login form to load
    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_element_located((By.NAME, "username")))

    # Find username and password fields and fill them
    username = driver.find_element(By.NAME, "username")
    password = driver.find_element(By.NAME, "password")

    username.send_keys(user_username)
    password.send_keys(user_password)

    # Find the login button and click it
    login_button = driver.find_element(By.XPATH, '//*[@id="loginForm"]/div/div[3]/button')
    login_button.click()

    # Wait for some time to ensure login is processed
    wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="react-root"]/section/main')))
    print("Logged in successfully")

    # Indefinite wait to keep the browser open
    input("Press Enter to close the browser...")

finally:
    # Close the browser
    driver.quit()
