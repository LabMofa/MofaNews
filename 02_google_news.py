from gnews import GNews
from datetime import datetime
import requests

def get_todays_top_news(search_word, max_articles=5):
    google_news = GNews()
    google_news.period = '1d'  # Set period to '1d' to get news from the past day
    news = google_news.get_news(search_word)
    return news[:max_articles]  # Limit the number of articles

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
        print(f"Message sent to Telegram: {message}")
        return response
    except requests.RequestException as e:
        print(f"Failed to send message. Error: {e}")
        return None

# Define the search words
search_words = ["Cuba", "Haiti", "Multinational Security Support"]

# Define your Telegram bot token and chat ID
bot_token = 'INPUT YOUR TOKEN'  # Replace with your bot token
chat_id = 'INPUT YOUR CHAT ID'  # Replace with your chat ID

# Get today's date in the required format for the error message
today = datetime.now()
date_str = today.strftime("%m월 %d일자")

# Iterate over each search word, get the top news, and send to Telegram
for search_word in search_words:
    print(f"Fetching news for: {search_word}")
    news_articles = get_todays_top_news(search_word)
    if news_articles:
        for news in news_articles:
            message = f"<b>Title:</b> {news['title']}\n<b>URL:</b> {news['url']}\n<b>Published Date:</b> {news['published date']}\n"
            print(f"News: {message}")  # Print the news message to the terminal
            send_to_telegram(bot_token, chat_id, message)
    else:
        error_message = f"{date_str} {search_word} 관련 기사를 찾을 수 없습니다."
        print(error_message)  # Print the error message to the terminal
        send_to_telegram(bot_token, chat_id, error_message)

print("News titles have been sent to Telegram.")

