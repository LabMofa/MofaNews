import requests
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# URL of the MOFA RSS feed
URL_MOFA_RSS = "http://www.mofa.go.kr/www/brd/rss.do?brdId=234"

def scrape_latest_items(url, max_items=5):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    
    # Send a GET request to the RSS feed with headers
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an exception for HTTP errors
        logger.info(f"Successfully retrieved the page from {url}")
    except requests.RequestException as e:
        logger.error(f"Failed to retrieve the page. Error: {e}")
        return []

    # Parse the XML content
    try:
        root = ET.fromstring(response.content)
        logger.info("Successfully parsed the XML content")
    except ET.ParseError as e:
        logger.error(f"Failed to parse XML content. Error: {e}")
        return []

    # Find the items in the RSS feed
    items = root.findall('./channel/item')

    # Log the number of items found
    logger.info(f"Number of items found: {len(items)}")

    # Calculate the time 24 hours ago
    time_24_hours_ago = datetime.now() - timedelta(days=1)

    # Extract title, URL, and publication date from each item
    latest_items = []
    for item in items:
        title_element = item.find('title')
        link_element = item.find('link')
        pub_date_element = item.find('pubDate')

        if title_element is not None and link_element is not None and pub_date_element is not None:
            title = title_element.text.strip()
            url = link_element.text.strip()
            pub_date_str = pub_date_element.text.strip()
            pub_date = datetime.strptime(pub_date_str, '%a, %d %b %Y %H:%M:%S %Z')
            
            if pub_date > time_24_hours_ago:
                latest_items.append({
                    'title': title,
                    'url': url,
                    'pub_date': pub_date
                })

            if len(latest_items) >= max_items:
                break

    return latest_items

def send_to_telegram(bot_token, chat_id, message):
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {
        'chat_id': chat_id,
        'text': message,
        'parse_mode': 'HTML'
    }
    try:
        response = requests.post(url, data=payload)
        response.raise_for_status()  # Raise an exception for HTTP errors
        logger.info(f"Message sent to Telegram: {message}")
        return response
    except requests.RequestException as e:
        logger.error(f"Failed to send message. Error: {e}")
        return None

# Scrape and log the latest items
latest_items = scrape_latest_items(URL_MOFA_RSS)

# Define your Telegram bot token and chat ID
bot_token = 'INPUT YOUR TOKEN'  # Replace with your bot token
chat_id = 'INPUT YOUR CHAT ID'  # Replace with your chat ID

# Send the results to Telegram
if latest_items:
    for item in latest_items:
        message = f"<b>Title:</b> {item['title']}\n<b>URL:</b> {item['url']}\n<b>Published Date:</b> {item['pub_date']}\n"
        logger.info(f"News: {message}")
        send_to_telegram(bot_token, chat_id, message)
else:
    error_message = "No items found or failed to retrieve the page."
    logger.info(error_message)
    send_to_telegram(bot_token, chat_id, error_message)

logger.info("News titles have been sent to Telegram.")
