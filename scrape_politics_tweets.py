from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
import random

# Twitter account credentials
twitter_username = 'arnavsam2@gmail.com'
twitter_password = 'Arnav&Kundan@123'
twitter_username_2 = '@arnav_sam13389'

# Verify ChromeDriver path
driver_path = r'C:\Users\anupa\Downloads\chromedriver-win64 (1)\chromedriver-win64\chromedriver.exe'  # Use raw string

# Set up Chrome options
chrome_options = webdriver.ChromeOptions()
chrome_options.binary_location = r'C:\Users\anupa\Downloads\chrome-win64\chrome-win64\chrome.exe'  # Path to the Chrome executable

# Initialize the WebDriver with Service
service = Service(driver_path)
try:
    driver = webdriver.Chrome(service=service, options=chrome_options)
except Exception as e:
    raise Exception(f"Failed to initialize WebDriver: {e}")

def human_delay(min_seconds=1, max_seconds=3):
    time.sleep(random.uniform(min_seconds, max_seconds))

try:
    # Open Twitter login page
    driver.get('https://twitter.com/login')
    
    # Wait for the page to load
    wait = WebDriverWait(driver, 20)
    
    # Locate the email input field and enter email
    email_input = wait.until(EC.presence_of_element_located((By.NAME, 'text')))
    human_delay(2, 4)
    email_input.send_keys(twitter_username)
    
    # Delay for 15 seconds to mimic human thinking time
    human_delay(14, 16)
    
    # Use JavaScript to detect and click the "Next" button
    script = """
    var nextButton = document.querySelector('div[data-testid="LoginForm_Login_Button"]');
    if (nextButton) {
        nextButton.click();
    }
    """
    driver.execute_script(script)
    
    # Wait for the username input field to be present
    username_input = wait.until(EC.presence_of_element_located((By.NAME, 'text')))
    human_delay(2, 4)
    username_input.send_keys(twitter_username_2)
    username_input.send_keys(Keys.RETURN)
    
    # Wait for the password field to be present
    password_input = wait.until(EC.presence_of_element_located((By.NAME, 'password')))
    human_delay(2, 4)
    password_input.send_keys(twitter_password)
    password_input.send_keys(Keys.RETURN)
    
    # Wait for the home page to load after login
    wait.until(EC.presence_of_element_located((By.XPATH, '//input[@aria-label="Search query"]')))
    
    # Open Twitter Explore page
    human_delay(2, 4)
    driver.get('https://twitter.com/explore')
    
    # Wait for the search box to be present
    search_box = wait.until(EC.presence_of_element_located((By.XPATH, '//input[@aria-label="Search query"]')))
    
    # Enter the search query
    human_delay(2, 4)
    search_box.send_keys('politics')  # Search query set to 'politics'
    search_box.send_keys(Keys.RETURN)
    
    # Wait for search results to load
    human_delay(2, 4)
    
    # Click on the "Latest" tab to get the most recent tweets
    latest_tab = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, 'Latest')))
    human_delay(2, 4)
    latest_tab.click()
    
    # Wait for the "Latest" tab to load
    human_delay(2, 4)
    
    # Scroll down to load more tweets
    for _ in range(5):  # Adjust the range to scroll more or less
        driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
        human_delay(2, 4)
    
    # Get page source and parse with BeautifulSoup
    page_source = driver.page_source
    soup = BeautifulSoup(page_source, 'html.parser')
    
    # Find tweet elements
    tweets = soup.find_all('div', {'data-testid': 'tweet'})
    
    for tweet in tweets:
        try:
            # Extract and print the tweet text
            tweet_text = tweet.find('div', {'lang': True}).text
            print(tweet_text)
            # Random delay between printing tweets
            human_delay(1, 3)
        except Exception as e:
            print(f'Error extracting tweet text: {e}')
finally:
    # Close the WebDriver
    driver.quit()
