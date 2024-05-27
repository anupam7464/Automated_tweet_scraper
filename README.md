# Twitter Tweet Extractor

This repository contains a Python script that logs into Twitter, searches for specific tweets, and prints their content using Selenium and BeautifulSoup.

# Prerequisites

- Python 3.x
- Google Chrome
- ChromeDriver
  (note- google chrome and crome driver both must be same version)

# Installation

1. Clone the repository:

   git clone https://github.com/yourusername/Twitter-Tweet-Extractor.git
   cd Twitter-Tweet-Extractor
   

2. Install the required Python packages:
   
   pip install selenium beautifulsoup4

3. Download ChromeDriver:

   Download the ChromeDriver that matches your version of Chrome from [here](https://sites.google.com/a/chromium.org/chromedriver/downloads).

4. Update the script with your credentials and paths:

   Open the script file and update the following variables with your own information:

   
   twitter_username = 'enter your email'
   twitter_password = 'enter your password'
   twitter_username_2 = 'enter your username'
   
   driver_path = r'location of chrome driver'  # Use raw string
   chrome_options.binary_location = r'location of chrome application'  # Path to the Chrome executable

 #  Usage

1. Run the script:

   
   python script_name.py
   
   Replace `script_name.py` with the name of your script file.

2. Script Process:

   - The script will open the Twitter login page.
   - It will enter your email, username, and password to log in.
   - After logging in, it will navigate to the Twitter Explore page and search for tweets with the keyword .
   - It will click on the "Latest" tab to get the most recent tweets.
   - The script will scroll down to load more tweets and then extract and print the tweet text.

# Script Explanation

- Login to Twitter:

  The script uses Selenium to open the Twitter login page and input your credentials to log in.

- Search for Tweets:

  After logging in, the script navigates to the Twitter Explore page and searches for tweets containing the keyword 'politics'.

- Extract and Print Tweets:

  The script scrolls down to load more tweets, extracts the text of each tweet using BeautifulSoup, and prints the tweet content.

# Libraries Used

- Selenium: For automating the browser interactions.
- BeautifulSoup: For parsing the HTML content and extracting the tweet text.
- time and random: For adding human-like delays during interactions.
