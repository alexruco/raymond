# main.py

import logging
from .tasks import extract_keywords_from_urls
from .utils import valid_url

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
    print("Columns in result_df:", result_df.columns)
    print("Contents of result_df:\n", result_df)

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
    # Ensure the DataFrame is properly formatted
    result_df.to_csv(output_csv, index=False)

    return result_df

# Example usage
if __name__ == "__main__":
    # Example URL
    url = 'https://example.com'
    keywords = get_keywords(url)
    print(f"Keywords for {url}: {keywords}")

    # Example file path
    #file_path = 'urls.txt'
    #result_df = get_keywords_from_file(file_path, output_csv='keywords.csv')
    #print(f"Keywords extracted and saved to keywords.csv")
