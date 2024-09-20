# main.py

import logging
from tasks import extract_keywords_from_urls
from utils import valid_url
import people_also_ask
from typing import Set

def get_keywords(url, top_n=10):
    """ 
    Extracts keywords from a single URL and returns them as a list.
    """
    # Validate the URL
    try:
        valid_url(url)
    except ValueError as e:
        raise ValueError(f"Invalid URL provided: {e}")

    # Extract keywords
    result_df = extract_keywords_from_urls(
        urls=[url],
        top_n=top_n
    )

    # Debugging: Print the columns and DataFrame
    # Uncomment the following lines if you need to debug
    # print("Columns in result_df:", result_df.columns)
    # print("Contents of result_df:\n", result_df)

    # Collect keywords from 'keyword_1' to 'keyword_n' columns
    keyword_columns = [col for col in result_df.columns if col.startswith('keyword_')]
    if not keyword_columns:
        raise KeyError("The DataFrame does not contain keyword columns.")

    # Extract the keywords from the row corresponding to the URL
    keywords_row = result_df.iloc[0][keyword_columns]

    # Remove any None or NaN values
    keywords = keywords_row.dropna().tolist()

    return keywords

def get_keywords_from_file(file_path, top_n=10, output_csv='output.csv'):
    """
    Reads URLs from a text file, extracts keywords from each, and saves the results to a CSV.
    Returns the DataFrame containing the results.
    """
    # Read URLs from file
    try:
        with open(file_path, 'r') as f:
            urls = [line.strip() for line in f if line.strip()]
    except Exception as e:
        logging.error(f"Failed to read URLs from file {file_path}: {e}")
        raise

    if not urls:
        logging.error("No URLs found in the file.")
        raise ValueError("No URLs found in the file.")

    # Validate URLs
    valid_urls = []
    for url in urls:
        try:
            valid_url(url)
            valid_urls.append(url)
        except ValueError as e:
            logging.warning(f"{e}")

    if not valid_urls:
        logging.error("No valid URLs to process after validation.")
        raise ValueError("No valid URLs to process after validation.")

    # Extract keywords
    result_df = extract_keywords_from_urls(
        urls=valid_urls,
        top_n=top_n
    )

    # Save the results to CSV
    result_df.to_csv(output_csv, index=False)

    return result_df

def get_people_also_ask_questions(central_keyword: str, url: str, top_n: int = 10, max_questions: int = 10) -> Set[str]:
    """
    Extracts keywords from the URL, combines them with the central keyword,
    and retrieves 'People Also Ask' questions for each combined query.

    Args:
        central_keyword (str): The central keyword to combine with extracted keywords.
        url (str): The URL to extract keywords from.
        top_n (int): Number of top keywords to extract from the URL.
        max_questions (int): Maximum number of questions to retrieve per combined query.

    Returns:
        Set[str]: A set of unique 'People Also Ask' questions.
    """
    # Validate the URL
    try:
        valid_url(url)
    except ValueError as e:
        raise ValueError(f"Invalid URL provided: {e}")

    # Get keywords from the URL
    keywords = get_keywords(url, top_n=top_n)
    logging.info(f"Extracted keywords: {keywords}")

    # Combine each keyword with the central keyword
    combined_queries = [f"'{central_keyword}' {keyword}" for keyword in keywords]
    logging.info(f"Combined queries: {combined_queries}")

    # Collect unique questions
    all_questions = set()

    for query in combined_queries:
        try:
            # Get 'People Also Ask' questions for the combined query
            questions = people_also_ask.get_related_questions(query)
            # Limit the number of questions per query
            questions = questions[:max_questions]
            logging.info(f"Questions for '{query}': {questions}")
            all_questions.update(questions)
        except Exception as e:
            logging.error(f"Error getting questions for query '{query}': {e}")

    return all_questions


def get_keywords_from_file(file_path, top_n=10, output_csv='output.csv'):
    """
    Reads URLs from a text file, extracts keywords from each, and saves the results to a CSV.
    Returns the DataFrame containing the results.
    """
    # Read URLs from file
    try:
        with open(file_path, 'r') as f:
            urls = [line.strip() for line in f if line.strip()]
    except Exception as e:
        logging.error(f"Failed to read URLs from file {file_path}: {e}")
        raise

    if not urls:
        logging.error("No URLs found in the file.")
        raise ValueError("No URLs found in the file.")

    # Validate URLs
    valid_urls = []
    for url in urls:
        try:
            valid_url(url)
            valid_urls.append(url)
        except ValueError as e:
            logging.warning(f"{e}")

    if not valid_urls:
        logging.error("No valid URLs to process after validation.")
        raise ValueError("No valid URLs to process after validation.")

    # Extract keywords
    result_df = extract_keywords_from_urls(
        urls=valid_urls,
        top_n=top_n
    )

    # Save the results to CSV
    result_df.to_csv(output_csv, index=False)

    return result_df


# Example usage
if __name__ == "__main__":
    # Configure logging to output to the console
    logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

    # Example central keyword and URL
    central_keyword = 'machine learning'
    url = 'https://en.wikipedia.org/wiki/Artificial_intelligence'

    # Get 'People Also Ask' questions
    try:
        questions = get_people_also_ask_questions(central_keyword, url, top_n=5, max_questions=5)
        print(f"People Also Ask questions for URL '{url}' with central keyword '{central_keyword}':")
        for question in questions:
            print(f"- {question}")
    except Exception as e:
        logging.error(f"An error occurred: {e}")
