# Agentic Marketplace Insights API

An AI-powered FastAPI application that leverages Ollama (free, open-source LLM) to generate intelligent product insights for marketplace analysis. This application helps businesses understand market trends, pricing strategies, competitive positioning, and actionable recommendations for their products.

## Features

- 🤖 **AI-Powered Insights**: Generate comprehensive product insights using Ollama's free LLM models
- 📊 **Multiple Insight Types**: 
  - Trend analysis
  - Pricing insights
  - Competitor analysis
  - General product insights
- 🗄️ **MongoDB Integration**: Store products and insights for historical analysis
- 🚀 **FastAPI**: Modern, fast, async API framework
- 🔄 **Product Comparison**: Compare multiple products side-by-side
- 📈 **RESTful API**: Clean, well-documented API endpoints

## Tech Stack

- **Python 3.8+**
- **FastAPI** - Modern web framework for building APIs
- **MongoDB** - NoSQL database for storing products and insights
- **Motor** - Async MongoDB driver
- **Ollama** - Free, local LLM inference server
- **Pydantic** - Data validation using Python type annotations
- **httpx** - Async HTTP client for Ollama API calls

## Prerequisites

Before you begin, ensure you have the following installed:

1. **Python 3.8+** - [Download Python](https://www.python.org/downloads/)
2. **MongoDB** - [Install MongoDB](https://www.mongodb.com/try/download/community)
3. **Ollama** - [Install Ollama](https://ollama.ai/)

### Installing Ollama

1. Download and install Ollama from [ollama.ai](https://ollama.ai/)
2. Pull a model (e.g., llama3.2):
   ```bash
   ollama pull llama3.2
   ```
3. Start Ollama server (usually runs automatically):
   ```bash
   ollama serve
   ```

## Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd agentic_marketplace_clients
   ```

2. **Create a virtual environment**:
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**:
   ```bash
   cp .env.example .env
   ```
   
   Edit `.env` file with your configuration:
   ```env
   MONGODB_URL=mongodb://localhost:27017
   MONGODB_DATABASE=marketplace_insights
   OLLAMA_BASE_URL=http://localhost:11434
   OLLAMA_MODEL=llama3.2
   DEBUG=false
   ```

5. **Start MongoDB** (if not running):
   ```bash
   # On Windows (if installed as service, it should be running)
   # On macOS/Linux
   mongod
   ```

## Running the Application

Start the FastAPI server:

```bash
uvicorn app.main:app --reload
```

The API will be available at:
- **API**: http://localhost:8000
- **Interactive API Docs**: http://localhost:8000/docs
- **Alternative API Docs**: http://localhost:8000/redoc

## API Endpoints

### Product Management

#### Create Product
```http
POST /api/v1/products
Content-Type: application/json

{
  "name": "Wireless Bluetooth Headphones",
  "description": "Premium noise-cancelling headphones",
  "category": "Electronics",
  "price": 199.99,
  "marketplace": "Amazon",
  "product_id": "B08XYZ123",
  "url": "https://example.com/product"
}
```

#### Get Products
```http
GET /api/v1/products?skip=0&limit=10&marketplace=Amazon&category=Electronics
```

#### Get Product by ID
```http
GET /api/v1/products/{product_id}
```

#### Update Product
```http
PUT /api/v1/products/{product_id}
Content-Type: application/json

{
  "price": 179.99,
  "description": "Updated description"
}
```

#### Delete Product
```http
DELETE /api/v1/products/{product_id}
```

### Insights Generation

#### Generate Product Insight
```http
POST /api/v1/insights/generate
Content-Type: application/json

{
  "product_id": "507f1f77bcf86cd799439011",
  "insight_type": "trend_analysis",
  "context": "Launching in Q4 2024",
  "include_competitors": false
}
```

**Insight Types:**
- `general` - Comprehensive product insights (default)
- `trend_analysis` - Market trends and demand analysis
- `pricing_insight` - Pricing strategy and competitiveness
- `competitor_analysis` - Competitive landscape analysis

#### Get Product Insights
```http
GET /api/v1/insights/product/{product_id}
```

#### Compare Products
```http
POST /api/v1/insights/compare
Content-Type: application/json

[
  {
    "name": "Product A",
    "price": 99.99,
    "features": "Feature list..."
  },
  {
    "name": "Product B",
    "price": 149.99,
    "features": "Feature list..."
  }
]
```

#### List Available Ollama Models
```http
GET /api/v1/insights/models
```

### Health Check
```http
GET /health
```

## Usage Examples

### Python Example

```python
import httpx

# Create a product
async with httpx.AsyncClient() as client:
    response = await client.post(
        "http://localhost:8000/api/v1/products",
        json={
            "name": "Smart Watch Pro",
            "description": "Advanced fitness tracking smartwatch",
            "category": "Wearables",
            "price": 299.99,
            "marketplace": "Amazon"
        }
    )
    product = response.json()

# Generate insights
response = await client.post(
    "http://localhost:8000/api/v1/insights/generate",
    json={
        "product_id": product["id"],
        "insight_type": "trend_analysis"
    }
)
insight = response.json()
print(insight["insight"]["insight_content"])
```

### cURL Example

```bash
# Create a product
curl -X POST "http://localhost:8000/api/v1/products" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Wireless Mouse",
    "category": "Computer Accessories",
    "price": 29.99,
    "marketplace": "Amazon"
  }'

# Generate pricing insight
curl -X POST "http://localhost:8000/api/v1/insights/generate" \
  -H "Content-Type: application/json" \
  -d '{
    "product_name": "Wireless Mouse",
    "price": 29.99,
    "insight_type": "pricing_insight"
  }'
```

## Project Structure

```
agentic_marketplace_clients/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI application entry point
│   ├── config.py               # Configuration settings
│   ├── database.py             # MongoDB connection
│   ├── models/
│   │   ├── __init__.py
│   │   └── product.py          # Pydantic models
│   ├── routers/
│   │   ├── __init__.py
│   │   ├── insights.py         # Insight endpoints
│   │   └── products.py         # Product endpoints
│   └── services/
│       ├── __init__.py
│       ├── ollama_service.py   # Ollama AI service
│       └── product_service.py  # Product database service
├── .env.example                # Environment variables template
├── .gitignore
├── requirements.txt            # Python dependencies
└── README.md
```

## Configuration

The application can be configured via environment variables (`.env` file):

| Variable | Description | Default |
|----------|-------------|---------|
| `MONGODB_URL` | MongoDB connection string | `mongodb://localhost:27017` |
| `MONGODB_DATABASE` | Database name | `marketplace_insights` |
| `OLLAMA_BASE_URL` | Ollama server URL | `http://localhost:11434` |
| `OLLAMA_MODEL` | Default Ollama model | `llama3.2` |
| `DEBUG` | Debug mode | `false` |

## Available Ollama Models

You can use any Ollama model. Popular options include:

- `llama3.2` - Meta's Llama 3.2 (recommended)
- `llama3` - Meta's Llama 3
- `mistral` - Mistral AI model
- `codellama` - Code-focused model
- `phi3` - Microsoft's Phi-3

To use a different model, either:
1. Set `OLLAMA_MODEL` in your `.env` file
2. Pull the model: `ollama pull <model-name>`

## Development

### Running Tests

```bash
# Install test dependencies
pip install pytest pytest-asyncio httpx

# Run tests
pytest
```

### Code Formatting

```bash
pip install black isort
black app/
isort app/
```

## Troubleshooting

### Ollama Connection Issues

- Ensure Ollama is running: `ollama serve`
- Check if the model is downloaded: `ollama list`
- Verify the base URL in `.env` matches your Ollama server

### MongoDB Connection Issues

- Ensure MongoDB is running
- Check connection string in `.env`
- Verify MongoDB is accessible: `mongosh` or `mongo`

### Port Already in Use

If port 8000 is in use, run with a different port:
```bash
uvicorn app.main:app --reload --port 8001
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is open source and available under the MIT License.

## Support

For issues, questions, or contributions, please open an issue on the GitHub repository.

## Acknowledgments

- [Ollama](https://ollama.ai/) for providing free, local LLM inference
- [FastAPI](https://fastapi.tiangolo.com/) for the excellent web framework
- [MongoDB](https://www.mongodb.com/) for the robust database solution
