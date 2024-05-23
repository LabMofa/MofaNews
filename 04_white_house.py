import requests
from bs4 import BeautifulSoup
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# URL of the webpage to scrape
URL_WHITEHOUSE = "https://www.whitehouse.gov/briefing-room/"

def scrape_latest_items(url, max_items=5):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    
    # Send a GET request to the webpage with headers
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an exception for HTTP errors
        logger.info(f"Successfully retrieved the page from {url}")
    except requests.RequestException as e:
        logger.error(f"Failed to retrieve the page. Error: {e}")
        return []

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find the items in the briefing room section
    items = soup.select('article a')

    # Log the number of items found
    logger.info(f"Number of items found: {len(items)}")

    # Extract title and URL from each item
    latest_items = []
    for item in items[:max_items]:  # Limit to the latest 5 items
        title = item.get_text(strip=True)
        url = item['href']
        latest_items.append({
            'title': title,
            'url': url
        })

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
latest_items = scrape_latest_items(URL_WHITEHOUSE)

# Define your Telegram bot token and chat ID
bot_token = 'INPUT YOUR TOKEN'  # Replace with your bot token
chat_id = 'INPUT YOUR CHAT ID'  # Replace with your chat ID

# Send the results to Telegram
if latest_items:
    for item in latest_items:
        message = f"<b>Title:</b> {item['title']}\n<b>URL:</b> {item['url']}\n"
        logger.info(f"News: {message}")
        send_to_telegram(bot_token, chat_id, message)
else:
    error_message = "No items found or failed to retrieve the page."
    logger.info(error_message)
    send_to_telegram(bot_token, chat_id, error_message)

logger.info("News titles have been sent to Telegram.")

