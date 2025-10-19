# Elasticsearch JSON Parse Codebase

A backend pipeline that integrates SerpAPI (Google search results) with Elasticsearch for structured search result indexing.

## Features

- Fetches search results from Google via SerpAPI with pagination
- Categorizes results into videos and articles based on metadata
- Structures results into clean JSON documents
- Bulk indexes results into Elasticsearch
- Command-line interface for easy usage
- Modular architecture for easy extension

## Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Environment Variables

Copy the example environment file and fill in your credentials:

```bash
cp .env.example .env
```

Edit `.env` with your actual values:

```env
SERPAPI_KEY=your_actual_serpapi_key
ELASTIC_URL=http://localhost:9200
```

### 3. Get SerpAPI Credentials

1. **SerpAPI Key**: Go to [SerpAPI](https://serpapi.com/)
   - Sign up for a free account
   - Get your API key from the dashboard
   - Free tier includes 100 searches per month

### 4. Start Elasticsearch

Make sure Elasticsearch is running on your system:

```bash
# Using Docker
docker run -d -p 9200:9200 -e "discovery.type=single-node" elasticsearch:8.11.0

# Or install locally and start the service
```

## Usage

### Basic Usage

```bash
python src/run_query.py "machine learning tutorials"
```

### Advanced Usage

```bash
# Fetch more pages (up to 10 pages)
python src/run_query.py "biology for beginners" --pages 10

# Validate configuration only
python src/run_query.py --validate-config
```

### Example Output

```
Processing query: 'machine learning tutorials'
==================================================
Step 1: Fetching results from Google via SerpAPI...
Fetching page 1 (results 1-10)...
Fetching page 2 (results 11-20)...
Fetching page 3 (results 21-30)...
Fetching page 4 (results 31-40)...
Fetching page 5 (results 41-50)...
Successfully fetched 50 total results

Step 2: Categorizing results...
Found 5 videos and 5 articles

Step 3: Structuring results into JSON documents...
Created 10 structured documents

Step 4: Indexing documents to Elasticsearch...
Created Elasticsearch index: search_results
Successfully indexed 10 documents to Elasticsearch

==================================================
✅ Pipeline completed successfully!
📊 Indexed 10 documents:
   - 5 videos
   - 5 articles
```

## Architecture

```
src/
├── config.py                 # Environment configuration
├── run_query.py             # CLI entry point
├── google_client/
│   └── search_client.py     # SerpAPI client for Google search results
├── parsers/
│   └── result_parser.py     # Result categorization and structuring
└── elasticsearch_client/
    └── es_client.py         # Elasticsearch indexing client
```

## Data Structure

Each indexed document contains:

```json
{
  "query": "machine learning tutorials",
  "category": "video",
  "title": "Machine Learning Tutorial for Beginners",
  "url": "https://example.com/ml-tutorial",
  "description": "A comprehensive guide to machine learning...",
  "source": "google",
  "rank": 1,
  "thumbnailUrl": "https://example.com/thumb.jpg",
  "author": "Example Author",
  "timestamp": "2024-01-15T10:30:00Z"
}
```

## Configuration

### Environment Variables

- `SERPAPI_KEY`: Your SerpAPI key (required)
- `ELASTIC_URL`: Elasticsearch URL (default: http://localhost:9200)

### Constants (in config.py)

- `RESULTS_PER_PAGE`: Number of results per page (default: 10)
- `MAX_PAGES`: Maximum pages to fetch (default: 5)
- `TOP_RESULTS_PER_CATEGORY`: Top results per category (default: 5)
- `ELASTIC_INDEX`: Elasticsearch index name (default: search_results)

## Extending the System

The modular architecture makes it easy to extend:

### Adding New Result Types

1. Update `ResultParser._classify_item()` to detect new types
2. Modify `categorize_results()` to handle new categories
3. Update Elasticsearch mapping in `es_client.py`

### Adding AI/LLM Features

The pipeline is designed for easy integration of AI features:

- **Re-ranking**: Add re-ranking logic in `result_parser.py`
- **Content Analysis**: Extend `ResultParser` with LLM analysis
- **Semantic Search**: Enhance Elasticsearch queries with vector search

### Custom Processing

- **Filters**: Add filtering logic in `categorize_results()`
- **Enrichment**: Enhance documents in `structure_json_document()`
- **Storage**: Extend `index_to_elastic()` for additional storage backends

## Error Handling

The system includes comprehensive error handling:

- API rate limiting and retries
- Missing field handling with defaults
- Elasticsearch connection validation
- Graceful degradation for partial failures

## Development

### Running Tests

```bash
pytest tests/
```

### Code Style

The codebase follows Python best practices:

- Type hints for all functions
- Comprehensive error handling
- Clear docstrings and comments
- Modular, testable design

## License

MIT License - see LICENSE file for details.
