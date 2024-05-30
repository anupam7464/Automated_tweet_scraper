import tweepy
import pandas as pd
import yaml
import os
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
import random

with open('config.yaml', 'r') as file:
    config = yaml.safe_load(file)

twitter_username = config['credentials']['username']
twitter_password = config['credentials']['password']
consumer_key = config['credentials']['consumer_key']
consumer_secret = config['credentials']['consumer_secret']
access_token = config['credentials']['access_token']
access_token_secret = config['credentials']['access_token_secret']

keywords = config['keywords']

def create_twitter_api():
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth, wait_on_rate_limit=True)
    return api

api = create_twitter_api()

driver_path = r'C:\Users\anupa\Downloads\chromedriver-win64 (1)\chromedriver-win64\chromedriver.exe'
chrome_options = webdriver.ChromeOptions()
chrome_options.binary_location = r'C:\Users\anupa\Downloads\chrome-win64\chrome-win64\chrome.exe'
chrome_options.add_argument('--disable-blink-features=AutomationControlled')
chrome_options.add_argument('--start-maximized')
service = Service(driver_path)
driver = webdriver.Chrome(service=service, options=chrome_options)

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
    find_element_with_retry(By.XPATH, '//input[@aria-label="Search query"]')
    human_delay(2, 4)

def search_tweets(keyword):
    driver.get('https://twitter.com/explore')
    search_box = find_element_with_retry(By.XPATH, '//input[@aria-label="Search query"]')
    human_delay(2, 4)
    search_box.send_keys(keyword)
    search_box.send_keys(Keys.RETURN)
    human_delay(2, 4)
    latest_tab = find_element_with_retry(By.LINK_TEXT, 'Latest')
    human_delay(2, 4)
    latest_tab.click()
    human_delay(2, 4)
    for _ in range(5):
        driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
        human_delay(2, 4)
    page_source = driver.page_source
    soup = BeautifulSoup(page_source, 'html.parser')
    tweets = soup.find_all('div', {'data-testid': 'tweet'})
    tweet_list = []
    for tweet in tweets:
        try:
            tweet_text = tweet.find('div', {'lang': True}).text
            tweet_list.append({
                'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'keyword': keyword,
                'tweet': tweet_text,
                'username': twitter_username
            })
        except Exception as e:
            print(f'Error extracting tweet text: {e}')
    return tweet_list

def save_tweets_to_csv(tweets):
    tweets_df = pd.DataFrame(tweets)
    csv_file = 'tweets.csv'
    try:
        existing_df = pd.read_csv(csv_file)
        combined_df = pd.concat([existing_df, tweets_df], ignore_index=True)
    except FileNotFoundError:
        combined_df = tweets_df
    combined_df.to_csv(csv_file, index=False)

def get_todays_tweet():
    csv_file = 'tweets.csv'
    df = pd.read_csv(csv_file)
    today = datetime.now().strftime('%Y-%m-%d')
    today_tweet = df[df['date'].str.contains(today)]
    if not today_tweet.empty:
        return today_tweet.iloc[0]['tweet']
    else:
        return None

def send_to_chatgpt(text):
    return f"Generate an image for the following tweet: {text}"

def create_image_from_prompt(prompt):
    print(f"Creating image for prompt: {prompt}")

try:
    login_to_twitter()
    all_tweets = []
    for keyword in keywords:
        tweets = search_tweets(keyword)
        all_tweets.extend(tweets)
    save_tweets_to_csv(all_tweets)
finally:
    driver.quit()

todays_tweet = get_todays_tweet()
if todays_tweet:
    image_prompt = send_to_chatgpt(todays_tweet)
    create_image_from_prompt(image_prompt)
else:
    print("No tweet found for today.")
