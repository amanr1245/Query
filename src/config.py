"""
Configuration module for loading environment variables and constants.
"""
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '..', '.env'))

# SerpAPI configuration
SERPAPI_KEY = os.getenv('SERPAPI_KEY')

# Elasticsearch configuration
ELASTIC_URL = os.getenv('ELASTIC_URL', 'http://localhost:9200')
ELASTIC_INDEX = 'search_results'

# Search configuration
RESULTS_PER_PAGE = 10
MAX_PAGES = 5

# Validate required environment variables
def validate_config():
    """Validate that required environment variables are set."""
    missing_vars = []

    if not SERPAPI_KEY:
        missing_vars.append('SERPAPI_KEY')

    if missing_vars:
        raise ValueError(f"Missing required environment variables: {', '.join(missing_vars)}")

    return True
