import sys
import os

# Ensure the 'raymond' package can be found
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from raymond.main import get_keywords, get_keywords_from_file

def test_get_keywords():
    # Example test for get_keywords function
    url = 'https://example.com'
    keywords = get_keywords(url, top_n=3)
    assert isinstance(keywords, list)
    assert len(keywords) == 3

def test_get_keywords_from_file(tmp_path):
    # Create a temporary file with test URLs
    d = tmp_path / "sub"
    d.mkdir()
    p = d / "test_urls.txt"
    p.write_text("https://example.com\n")

    # Test get_keywords_from_file function
    result_df = get_keywords_from_file(str(p), top_n=3)
    assert not result_df.empty
