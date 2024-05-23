import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import urllib.parse
import logging
import pytz
import time

# Set up logging
logging.basic_config(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def scrape_news_titles(base_url, search_word, max_articles=5):
    logger.info(f"Scraping news titles for: {search_word}")

    # URL-encode the search query
    query = urllib.parse.quote(search_word)
    
    # Decode the query for checking titles and content
    decoded_query = search_word.lower()
    
    # Calculate the date 24 hours ago in UTC
    utc_now = datetime.now(pytz.utc)
    end_date = utc_now
    start_date = end_date - timedelta(days=1)
    
    # Format the dates in the required format (YYYY.MM.DD)
    start_date_str = start_date.strftime("%Y.%m.%d")
    end_date_str = end_date.strftime("%Y.%m.%d")
    
    # Log the start and end dates
    logger.info(f"Start Date (UTC): {start_date_str}, End Date (UTC): {end_date_str}")
    
    # Construct the full URL with dynamic date parameters
    url = f"{base_url}?where=news&query={query}&sm=tab_opt&sort=0&photo=0&field=0&pd=3&ds={start_date_str}&de={end_date_str}&docid=&related=0&mynews=0&office_type=0&office_section_code=0&news_office_checked=&nso=so%3Ar%2Cp%3Afrom{start_date_str.replace('.','')}to{end_date_str.replace('.','')}&is_sug_officeid=0&office_category=0&service_area=0"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    
    try:
        # Sending a request to the URL
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an exception for HTTP errors

        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find all elements with the class name 'news_tit', which contains the news titles and URLs
        news_items = soup.find_all('a', {'class': 'news_tit'})
        
        # Extract the text and URL from each news item and store in a list
        news_list = []
        for item in news_items:
            title = item.get('title')  # The actual title is stored in the 'title' attribute
            url = item.get('href')  # The URL is stored in the 'href' attribute

            # Check if the title contains the original search word
            if decoded_query in title.lower():
                news_list.append({'title': title, 'url': url})
                if len(news_list) >= max_articles:
                    break

            # Fetch the content of the article
            article_response = requests.get(url, headers=headers)
            article_soup = BeautifulSoup(article_response.text, 'html.parser')
            content = article_soup.get_text().lower()

            # Check if the content contains the original search word
            if decoded_query in content and {'title': title, 'url': url} not in news_list:
                news_list.append({'title': title, 'url': url})
                if len(news_list) >= max_articles:
                    break
        
        logger.info(f"Found {len(news_list)} articles for: {search_word}")
        return news_list
    
    except requests.RequestException as e:
        logger.error(f"Failed to retrieve the page. Error: {e}")
        return []

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

def job():
    # Base URL for the news search
    base_url = 'https://search.naver.com/search.naver'

    # Define the search words
    search_words = [
        "가이아나",
        "과테말라",
        "그레나다",
        "앤티가바부다",
        "니카라과",
        "에콰도르",
        "도미니카공화국",
        "엘살바도르",
        "도미니카연방",
        "온두라스",
        "우루과이",
        "바베이도스",
        "자메이카",
        "바하마",
        "칠레",
        "베네수엘라",
        "코스타리카",
        "벨리즈",
        "볼리비아",
        "트리니다드토바고",
        "세인트루시아",
        "파나마",
        "세인트빈센트 그레나딘",
        "파라과이",
        "세인트키츠네비스",
        "수리남",
        "페루",
        "브라질",
        "멕시코",
        "콜롬비아",
        "아르헨티나",
        "아이티",
        "쿠바"
    ]

    # Define your Telegram bot token and chat ID
    bot_token = 'INPUT YOUR TOKEN'  # Replace with your bot token
    chat_id = 'INPUT YOUR CHAT ID'  # Replace with your chat ID

    # Get today's date in the required format for the error message
    utc_now = datetime.now(pytz.utc)
    date_str = utc_now.strftime("%m월 %d일자")

    # Scrape and send the results to Telegram for each search word
    for search_word in search_words:
        news_titles = scrape_news_titles(base_url, search_word)
        
        if news_titles:
            for news in news_titles:
                message = f"<b>Title:</b> {news['title']}\n<b>URL:</b> {news['url']}\n"
                send_to_telegram(bot_token, chat_id, message)
        else:
            error_message = f"최근 {search_word} 관련 기사를 찾을 수 없습니다."
            send_to_telegram(bot_token, chat_id, error_message)
        
        # Introduce a delay of 5 seconds between each request
        time.sleep(5)

    logger.info("News titles have been sent to Telegram.")

if __name__ == "__main__":
    job()
