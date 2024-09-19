# tasks.py

import pandas as pd
import requests
from bs4 import BeautifulSoup
import nltk
from tqdm import tqdm
import logging
import time
from keyword_extractor import extract_keywords
from requests_html import HTMLSession


nltk.download('stopwords', quiet=True)


def fetch_url_content(url):
    """
    Fetches the content of a URL and returns the text.
    """
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) ' +
                          'AppleWebKit/537.36 (KHTML, like Gecko) ' +
                          'Chrome/58.0.3029.110 Safari/537.3'}
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        text = soup.get_text(separator=' ', strip=True)
        
        # Save fetched content to a file for inspection
        with open('fetched_content.txt', 'w', encoding='utf-8') as f:
            f.write(text)
        
        logging.debug(f"Fetched content length for {url}: {len(text)}")
        return text
    except Exception as e:
        logging.error(f"Error fetching {url}: {e}")
        return None

def extract_keywords_from_urls(urls, top_n=5, max_words=5, delay=0.1):
    """
    Extracts top N keywords from each URL.
    """
    results = []
    for url in tqdm(urls, desc="Processing URLs"):
        logging.info(f"Processing URL: {url}")
        text = fetch_url_content(url)
        if text and len(text) > 100:  # Check for minimum content length
            logging.debug(f"Fetched text length: {len(text)} characters")
            keywords = extract_keywords(text, top_n=top_n)
            if not keywords:
                logging.warning(f"No keywords extracted for {url}")
            # Process keywords
            processed_keywords = [
                ' '.join(keyword.replace(',', ';').split()[:max_words]) if keyword else None
                for keyword in keywords
            ]
            # Pad with None if fewer keywords are found
            while len(processed_keywords) < top_n:
                processed_keywords.append(None)
            # Create a dictionary for the current URL and its keywords
            keyword_dict = {'url': url}
            for i, keyword in enumerate(processed_keywords, 1):
                keyword_dict[f'keyword_{i}'] = keyword
            keyword_dict['error'] = None  # No error
            results.append(keyword_dict)
        else:
            # In case of failure to fetch content or content too short
            logging.warning(f"Insufficient content fetched from {url}")
            keyword_dict = {'url': url, 'error': "Insufficient content"}
            for i in range(1, top_n + 1):
                keyword_dict[f'keyword_{i}'] = None
            results.append(keyword_dict)
        time.sleep(delay)  # Delay to respect rate limits
    return pd.DataFrame(results)
