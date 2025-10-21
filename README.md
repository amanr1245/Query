# Elasticsearch JSON Parse Codebase

A backend pipeline that integrates SerpAPI (Google search results) with Elasticsearch for structured search result indexing. Supports both local development and Elastic Cloud serverless deployment.

## Features

- Fetches search results from Google via SerpAPI with pagination
- Categorizes results into videos and articles based on metadata
- Structures results into clean JSON documents
- Bulk indexes results into Elasticsearch (local or cloud)
- Command-line interface for easy usage
- Modular architecture for easy extension
- **Cloud-ready**: Supports Elastic Cloud serverless deployment

## Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Environment Variables

Copy the example environment file and fill in your credentials:

```bash
cp env.example .env
```

### 3. Get SerpAPI Credentials

1. **SerpAPI Key**: Go to [SerpAPI](https://serpapi.com/)
   - Sign up for a free account
   - Get your API key from the dashboard
   - Free tier includes 250 searches per month

## Deployment Options

### Option A: Local Development

For local development, you can use a local Elasticsearch instance:

```bash
# Using Docker
docker run -d -p 9200:9200 -e "discovery.type=single-node" elasticsearch:8.11.0

# Or install locally and start the service
```

Configure your `.env` file:

```env
SERPAPI_KEY=your_actual_serpapi_key
ELASTIC_URL=http://localhost:9200
```

### Option B: Elastic Cloud Deployment (Recommended for Production)

#### 1. Create Elastic Cloud Account

1. Go to [Elastic Cloud](https://cloud.elastic.co/)
2. Sign up for a free account (14-day trial)
3. Create a new deployment
4. Choose "Serverless" deployment type for optimal cost efficiency

#### 2. Get Your Cloud Credentials

After creating your deployment, you'll need:

- **Elasticsearch URL**: Found in your deployment overview
- **API Key**: Generate from the Security section

#### 3. Configure for Cloud Deployment

Edit your `.env` file with cloud credentials:

```env
# SerpAPI Configuration
SERPAPI_KEY=your_actual_serpapi_key

# Elastic Cloud Configuration
ELASTIC_URL=https://your-deployment-id.region.aws.found.io:9243
ELASTIC_API_KEY=your_api_key_here
```

#### 4. Generate API Key (if needed)

If you don't have an API key:

1. Go to your Elastic Cloud deployment
2. Navigate to **Security** → **API Keys**
3. Click **Create API Key**
4. Give it a name (e.g., "search-pipeline")
5. Copy the generated key

#### 5. Test Cloud Connection

```bash
# Quick validation
python deploy_cloud.py

# Or use the built-in validation
python main.py --validate-cloud
```

This will validate your cloud configuration and test the connection.

> 📖 **For detailed cloud deployment instructions, see [CLOUD_DEPLOYMENT.md](CLOUD_DEPLOYMENT.md)**

## Usage

### Basic Usage

```bash
python main.py "machine learning tutorials"
```

### Advanced Usage

```bash
# Fetch more pages (up to 10 pages)
python main.py "biology for beginners" --pages 10

# Validate configuration only
python main.py --validate-config
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
Pipeline completed successfully!
Indexed 10 documents:
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

#### Required Variables
- `SERPAPI_KEY`: Your SerpAPI key (required for all deployments)

#### Local Deployment
- `ELASTIC_URL`: Elasticsearch URL (default: http://localhost:9200)

#### Cloud Deployment
- `ELASTIC_URL` (cloud endpoint) + `ELASTIC_API_KEY`

#### Optional Variables
- `ELASTIC_INDEX`: Elasticsearch index name (default: search_results)

### Cloud-Specific Features

The pipeline automatically detects cloud deployment and:

- Uses API key authentication instead of basic auth
- Applies serverless-compatible index settings (no shard/replica configuration)
- Implements connection retry logic for cloud reliability
- Uses appropriate timeouts for cloud environments

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

## Troubleshooting

### Cloud Deployment Issues

#### Connection Errors
```bash
# Test your cloud connection
python main.py --validate-config
```

Common issues:
- **Invalid API Key**: Regenerate your API key in Elastic Cloud
- **Wrong Elasticsearch URL**: Double-check your Elasticsearch URL in the deployment overview
- **Network Issues**: Ensure your firewall allows outbound HTTPS connections

#### Index Creation Issues
- Serverless deployments automatically handle index settings
- If you get permission errors, ensure your API key has the necessary privileges

### Local Development Issues

#### Elasticsearch Connection
```bash
# Check if Elasticsearch is running
curl http://localhost:9200

# Check cluster health
curl http://localhost:9200/_cluster/health
```

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
