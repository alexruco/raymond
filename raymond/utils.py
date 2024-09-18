import argparse
import re
import logging
import sys


def valid_url(url):
    """
    Validates the provided URL using a regular expression.
    Raises a ValueError if the URL is invalid.
    """
    regex = re.compile(
        r'^(?:http|ftp)s?://'  # http:// or https:// or ftp:// or ftps://
        r'(?:\S+(?::\S*)?@)?'  # user:pass@
        r'(?:'
        r'(?:(?:[A-Za-z0-9-]+\.)+[A-Za-z]{2,6})'  # domain...
        r'|'
        r'localhost'  # localhost...
        r'|'
        r'\d{1,3}(?:\.\d{1,3}){3}'  # ...or ipv4
        r')'
        r'(?::\d+)?'  # optional port
        r'(?:/\S*)?$', re.IGNORECASE)
    if re.match(regex, url):
        return url
    else:
        raise ValueError(f"Invalid URL: {url}")

def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Extract top N keywords from a collection of URLs using YAKE."
    )
    parser.add_argument(
        '--file',
        type=str,
        help='Path to a file containing URLs to process (one URL per line)'
    )
    parser.add_argument(
        '--top',
        type=int,
        default=5,
        help='Number of top keywords to extract per URL (default is 5)'
    )
    parser.add_argument(
        '--output',
        type=str,
        default='keywords.csv',
        help='Path to save the output CSV file (default is keywords.csv)'
    )
    parser.add_argument(
        '--verbose',
        action='store_true',
        help='Enable verbose output'
    )
    parser.add_argument(
        'urls',
        metavar='U',
        type=str,
        nargs='*',
        help='List of valid URLs to extract keywords from'
    )
    return parser.parse_args()

def setup_logging(verbose=False):
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        filename='keyword_extraction.log',
        filemode='w',
        format='%(asctime)s - %(levelname)s - %(message)s'
    )

def save_to_csv(df, output_path):
    try:
        df.to_csv(output_path, index=False, quoting=1)
        logging.info(f"Results successfully saved to {output_path}")
    except Exception as e:
        logging.error(f"Failed to save results to {output_path}: {e}")
        sys.exit(1)
