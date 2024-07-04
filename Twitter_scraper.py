import tweepy
import yaml
import time
import random
import logging
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from datetime import datetime

# Load configuration
with open('config.yaml', 'r') as file:
    config = yaml.safe_load(file)

# Twitter account credentials
twitter_username = config['credentials']['username']
twitter_password = config['credentials']['password']
consumer_key = config['credentials']['consumer_key']
consumer_secret = config['credentials']['consumer_secret']
access_token = config['credentials']['access_token']
access_token_secret = config['credentials']['access_token_secret']

# Keywords to search for
keywords = config['keywords']

# Selenium WebDriver setup
driver_path = r'C:\Users\anupa\Downloads\chromedriver-win64 (1)\chromedriver-win64\chromedriver.exe'
chrome_options = webdriver.ChromeOptions()
chrome_options.binary_location = r'C:\Users\anupa\Downloads\chrome-win64\chrome-win64\chrome.exe'
chrome_options.add_argument('--disable-blink-features=AutomationControlled')
chrome_options.add_argument('--start-maximized')
service = Service(driver_path)

logging.basicConfig(level=logging.INFO)

def human_delay(min_seconds=1, max_seconds=3):
    time.sleep(random.uniform(min_seconds, max_seconds))

def find_element_with_retry(by, value, retries=5):
    for i in range(retries):
        try:
            element = WebDriverWait(driver, 30).until(EC.presence_of_element_located((by, value)))
            return element
        except Exception as e:
            if i < retries - 1:
                human_delay(1, 3)
            else:
                raise e

def login_to_twitter():
    driver.get('https://twitter.com/login')
    human_delay(2, 4)
    username_input = find_element_with_retry(By.NAME, 'text')
    username_input.send_keys(twitter_username)
    human_delay(2, 4)
    username_input.send_keys(Keys.RETURN)
    password_input = find_element_with_retry(By.NAME, 'password')
    human_delay(2, 4)
    password_input.send_keys(twitter_password)
    human_delay(2, 4)
    password_input.send_keys(Keys.RETURN)
    explore_button = find_element_with_retry(By.XPATH, '//a[@href="/explore"]')
    human_delay(2, 4)
    explore_button.click()
    human_delay(2, 4)
    search_box = find_element_with_retry(By.XPATH, '//input[@aria-label="Search query"]')
    human_delay(2, 4)
    search_box.click()
    human_delay(2, 4)
    search_box.send_keys(keywords[0])
    human_delay(2, 4)
    search_box.send_keys(Keys.RETURN)
    human_delay(2, 4)

def scrape_top_tweets(keyword):
    scroll_attempts = 0
    max_scroll_attempts = 10
    tweet_count = 0
    while tweet_count < 10 and scroll_attempts < max_scroll_attempts:
        tweets = driver.find_elements(By.XPATH, '//article[@data-testid="tweet"]')
        for tweet in tweets:
            if tweet_count >= 10:
                break
            tweet_html = tweet.get_attribute('outerHTML')
            soup = BeautifulSoup(tweet_html, 'html.parser')
            try:
                username = soup.find('div', {'dir': 'ltr'}).text
                content = soup.find('div', {'lang': True}).text
                tweet_data = {
                    'Username': username,
                    'Content': content,
                    'Datetime': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                }
                filename = f"{keyword}_tweet_{tweet_count + 1}.csv"
                df = pd.DataFrame([tweet_data])
                df.to_csv(filename, index=False)
                tweet_count += 1
                human_delay(2, 4)
            except Exception as e:
                logging.error(f"Error processing tweet: {e}")
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        human_delay(2, 4)
        scroll_attempts += 1

try:
    driver = webdriver.Chrome(service=service, options=chrome_options)
    login_to_twitter()
    scrape_top_tweets(keywords[0])
finally:
    driver.quit()
