# src/raymond/keyword_extractor.py

import logging
from typing import List

from langdetect import detect
import yake


def extract_keywords(text: str, top_n: int = 4) -> List[str]:
    """
    Extracts the top N keywords from the provided text using YAKE (Yet Another Keyword Extractor).

    Args:
        text (str): The text to extract keywords from.
        top_n (int, optional): Number of top keywords to extract. Defaults to 4.

    Returns:
        List[str]: A list of extracted keywords.

    Notes:
        - If language detection fails or the detected language is not supported by YAKE,
          the function defaults to using English ('en').
        - Supported languages include major languages like English, Spanish, French, etc.
    """
    try:
        language = detect(text)
        logging.debug(f"Detected language: {language}")
    except Exception as e:
        language = 'en'
        logging.warning(f"Language detection failed: {e}. Defaulting to English.")

    supported_languages = [
        'ar', 'bg', 'cs', 'da', 'de', 'el', 'en', 'es', 'fa', 'fi', 'fr', 'hr',
        'hu', 'it', 'ja', 'ko', 'nl', 'no', 'pl', 'pt', 'ro', 'ru', 'sk', 'sl',
        'sv', 'tr', 'zh'
    ]

    if language not in supported_languages:
        logging.warning(
            f"Unsupported language '{language}' detected. Defaulting to English."
        )
        language = 'en'

    # Initialize YAKE keyword extractor
    custom_kw_extractor = yake.KeywordExtractor(
        lan=language,
        n=1,
        dedupLim=0.9,
        top=top_n,
        features=None
    )

    keywords = custom_kw_extractor.extract_keywords(text)
    logging.debug(f"Extracted keywords: {keywords}")

    # Return only the keyword strings
    return [kw[0] for kw in keywords]
