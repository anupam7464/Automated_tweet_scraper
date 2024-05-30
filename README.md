# Twitter Tweet Extractor

This repository contains a Python script that logs into Twitter, searches for specific tweets, and prints their content using Selenium and BeautifulSoup.

## Prerequisites

- Python 3.x
- Google Chrome
- ChromeDriver
  (note: Google Chrome and ChromeDriver must both be the same version)

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/Twitter-Tweet-Extractor.git
   cd Twitter-Tweet-Extractor
   ```

2. Install the required Python packages:
   ```bash
   pip install selenium beautifulsoup4 pyyaml tweepy pandas
   ```

3. Download ChromeDriver:
   Download the ChromeDriver that matches your version of Chrome from [here](https://sites.google.com/a/chromium.org/chromedriver/downloads).

4. Create and update the `config.yaml` file with your credentials and paths:
   
   ```yaml
   credentials:
     username: your_username
     password: your_password
     consumer_key: your_consumer_key
     consumer_secret: your_consumer_secret
     access_token: your_access_token
     access_token_secret: your_access_token_secret

   keywords:
     - keyword1
     - keyword2
     - keyword3
   ```

   - Replace `your_username` with your Twitter username.
   - Replace `your_password` with your Twitter password.
   - Replace `your_consumer_key`, `your_consumer_secret`, `your_access_token`, `your_access_token_secret` with your Twitter API credentials.
   - Replace `keyword1`, `keyword2`, `keyword3` with the keywords you want to search for.

5. Update the script with the path to ChromeDriver and the Chrome application:
   
   ```python
   driver_path = r'path_to_chromedriver'  # Use raw string
   chrome_options.binary_location = r'path_to_chrome_application'  # Path to the Chrome executable
   ```

## Usage

1. Run the script:
   ```bash
   python script_name.py
   ```
   Replace `script_name.py` with the name of your script file.

2. Script Process:
   - The script will open the Twitter login page.
   - It will enter your username and password to log in.
   - After logging in, it will navigate to the Twitter Explore page and search for tweets with the specified keywords.
   - It will click on the "Latest" tab to get the most recent tweets.
   - The script will scroll down to load more tweets and then extract and print the tweet text.

## Script Explanation

### Login to Twitter

The script uses Selenium to open the Twitter login page and input your credentials to log in.

### Search for Tweets

After logging in, the script navigates to the Twitter Explore page and searches for tweets containing the specified keywords.

### Extract and Print Tweets

The script scrolls down to load more tweets, extracts the text of each tweet using BeautifulSoup, and prints the tweet content.

## Libraries Used

- **Selenium**: For automating the browser interactions.
- **BeautifulSoup**: For parsing the HTML content and extracting the tweet text.
- **Tweepy**: For interacting with the Twitter API.
- **Pandas**: For handling CSV operations.
- **time and random**: For adding human-like delays during interactions.
