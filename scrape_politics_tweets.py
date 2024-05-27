from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
import random

twitter_username = 'enter your email'
twitter_password = 'enter your password'
twitter_username_2 = 'enter your username'

driver_path = r'location of chrome driver'

chrome_options = webdriver.ChromeOptions()
chrome_options.binary_location = r'location of chrome application'

service = Service(driver_path)
try:
    driver = webdriver.Chrome(service=service, options=chrome_options)
except Exception as e:
    raise Exception(f"Failed to initialize WebDriver: {e}")

def human_delay(min_seconds=1, max_seconds=3):
    time.sleep(random.uniform(min_seconds, max_seconds))

try:
    driver.get('https://twitter.com/login')
    wait = WebDriverWait(driver, 20)
    email_input = wait.until(EC.presence_of_element_located((By.NAME, 'text')))
    human_delay(2, 4)
    email_input.send_keys(twitter_username)
    human_delay(14, 16)
    script = """
    var nextButton = document.querySelector('div[data-testid="LoginForm_Login_Button"]');
    if (nextButton) {
        nextButton.click();
    }
    """
    driver.execute_script(script)
    username_input = wait.until(EC.presence_of_element_located((By.NAME, 'text')))
    human_delay(2, 4)
    username_input.send_keys(twitter_username_2)
    username_input.send_keys(Keys.RETURN)
    password_input = wait.until(EC.presence_of_element_located((By.NAME, 'password')))
    human_delay(2, 4)
    password_input.send_keys(twitter_password)
    password_input.send_keys(Keys.RETURN)
    wait.until(EC.presence_of_element_located((By.XPATH, '//input[@aria-label="Search query"]')))
    human_delay(2, 4)
    driver.get('https://twitter.com/explore')
    search_box = wait.until(EC.presence_of_element_located((By.XPATH, '//input[@aria-label="Search query"]')))
    human_delay(2, 4)
    search_box.send_keys('politics')
    search_box.send_keys(Keys.RETURN)
    human_delay(2, 4)
    latest_tab = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, 'Latest')))
    human_delay(2, 4)
    latest_tab.click()
    human_delay(2, 4)
    for _ in range(5):
        driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
        human_delay(2, 4)
    page_source = driver.page_source
    soup = BeautifulSoup(page_source, 'html.parser')
    tweets = soup.find_all('div', {'data-testid': 'tweet'})
    for tweet in tweets:
        try:
            tweet_text = tweet.find('div', {'lang': True}).text
            print(tweet_text)
            human_delay(1, 3)
        except Exception as e:
            print(f'Error extracting tweet text: {e}')
finally:
    driver.quit()
