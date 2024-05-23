import requests
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup
from collections import Counter
import nltk
from nltk.corpus import stopwords
import string

# Download stopwords
nltk.download('stopwords')

# URL of the RSS feed to scrape
URL_SECRETARY_RSS = "https://www.state.gov/rss-feed/secretarys-remarks/feed/"

def scrape_speech_urls(url, max_items=5):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    
    # Send a GET request to the RSS feed with headers
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an exception for HTTP errors
    except requests.RequestException as e:
        print(f"Failed to retrieve the page. Error: {e}")
        return []

    # Parse the XML content
    root = ET.fromstring(response.content)

    # Find the items in the RSS feed
    items = root.findall('./channel/item')

    # Debugging information
    print(f"Number of items found: {len(items)}")

    # Extract title and URL from each item
    speech_urls = []
    for item in items[:max_items]:  # Limit to the latest 5 items
        title_element = item.find('title')
        link_element = item.find('link')
        
        if title_element is not None and link_element is not None:
            title = title_element.text.strip()
            url = link_element.text.strip()
            speech_urls.append({
                'title': title,
                'url': url
            })

    return speech_urls

def fetch_speech_text(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an exception for HTTP errors

        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find the speech text (adjust the selector as needed based on the actual HTML structure)
        speech_text = soup.find('div', class_='entry-content').get_text(separator='\n', strip=True)
        return speech_text

    except requests.RequestException as e:
        print(f"Failed to retrieve the page. Error: {e}")
        return None

def analyze_text(text):
    # Define stopwords and punctuation
    stop_words = set(stopwords.words('english'))
    punctuations = set(string.punctuation)

    # Tokenize the text
    words = nltk.word_tokenize(text.lower())

    # Filter out stopwords and punctuation
    filtered_words = [word for word in words if word not in stop_words and word not in punctuations]

    # Count word frequencies
    word_freq = Counter(filtered_words)

    return word_freq.most_common(10)

# Scrape and print the latest speech URLs
speech_urls = scrape_speech_urls(URL_SECRETARY_RSS)

# Fetch and analyze the full text of each speech
all_speech_texts = ""
for speech in speech_urls:
    print(f"Title: {speech['title']}")
    print(f"URL: {speech['url']}")
    speech_text = fetch_speech_text(speech['url'])
    if speech_text:
        all_speech_texts += speech_text + " "
    else:
        print("Failed to fetch the speech text.")
    print("\n" + "="*80 + "\n")

# Analyze the combined text of all speeches
if all_speech_texts:
    most_common_words = analyze_text(all_speech_texts)
    print("Most Frequently Used Words:")
    for word, freq in most_common_words:
        print(f"{word}: {freq}")
else:
    print("No speech texts available for analysis.")
