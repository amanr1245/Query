#!/usr/bin/env python3
"""
Command-line interface for running search queries and indexing results.
"""
import sys
import argparse
from typing import List, Dict, Any

from config import validate_config
from google_client.search_client import fetch_google_results
from parsers.result_parser import categorize_results, ResultParser
from elasticsearch_client.es_client import index_to_elastic


def process_query(query: str, num_pages: int = 5) -> bool:
    """
    Process a search query through the complete pipeline.
    
    Args:
        query: Search query string
        num_pages: Number of pages to fetch from Google
        
    Returns:
        True if processing successful, False otherwise
    """
    try:
        print(f"Processing query: '{query}'")
        print("=" * 50)
        
        # Step 1: Fetch results from Google via SerpAPI
        print("Step 1: Fetching results from Google via SerpAPI...")
        raw_results = fetch_google_results(query, num_pages)
        
        # Step 2: Categorize results into videos and articles
        print("Step 2: Categorizing results...")
        categorized_results = categorize_results(raw_results)
        
        videos = categorized_results['videos']
        articles = categorized_results['articles']
        
        print(f"Found {len(videos)} videos and {len(articles)} articles")
        
        # Step 3: Structure results into clean JSON documents
        print("Step 3: Structuring results into JSON documents...")
        structured_docs = []
        
        parser = ResultParser()
        
        # Process videos
        for i, video in enumerate(videos):
            doc = parser.structure_json_document(
                video, query, 'video', i + 1
            )
            structured_docs.append(doc)
        
        # Process articles
        for i, article in enumerate(articles):
            doc = parser.structure_json_document(
                article, query, 'article', i + 1
            )
            structured_docs.append(doc)
        
        print(f"Created {len(structured_docs)} structured documents")
        
        # Step 4: Index documents to Elasticsearch
        print("Step 4: Indexing documents to Elasticsearch...")
        success = index_to_elastic(structured_docs)
        
        if success:
            print("=" * 50)
            print("Pipeline completed successfully!")
            print(f"Indexed {len(structured_docs)} documents:")
            print(f"   - {len(videos)} videos")
            print(f"   - {len(articles)} articles")
            return True
        else:
            print("Failed to index documents to Elasticsearch")
            return False
            
    except Exception as e:
        print(f"Error processing query: {e}")
        return False


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Search Google and index results to Elasticsearch"
    )
    parser.add_argument(
        "query", 
        help="Search query string"
    )
    parser.add_argument(
        "--pages", 
        type=int, 
        default=5,
        help="Number of pages to fetch from Google (default: 5)"
    )
    parser.add_argument(
        "--validate-config",
        action="store_true",
        help="Validate configuration and exit"
    )
    
    args = parser.parse_args()
    
    try:
        # Validate configuration
        print("Validating configuration...")
        validate_config()
        print("Configuration is valid")
        
        if args.validate_config:
            return 0
        
        # Process the query
        success = process_query(args.query, args.pages)
        return 0 if success else 1
        
    except ValueError as e:
        print(f"Configuration error: {e}")
        print("\nPlease ensure you have a .env file with the required variables:")
        print("  SERPAPI_KEY=your_serpapi_key")
        print("  ELASTIC_URL=http://localhost:9200  # optional")
        return 1
    except KeyboardInterrupt:
        print("\n\nProcess interrupted by user")
        return 1
    except Exception as e:
        print(f"Unexpected error: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
