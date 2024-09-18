# __init__.py for the _RAYMOND package

# Exposing only the main functions
from .main import get_keywords, get_keywords_from_file

# Versioning
__version__ = "1.0.0"

# Defining the public API (only the main module's functions are exposed)
__all__ = [
    'get_keywords',
    'get_keywords_from_file',
]
