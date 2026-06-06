# PDF to Markdown Converter Microservice

A highly accurate PDF to Markdown conversion service powered by [docling](https://github.com/DS4SD/docling) (IBM's state-of-the-art document parser).

## Features

- 🚀 FastAPI-based REST API
- 📄 High-fidelity PDF to Markdown conversion
- 🏗️ Structured output with preserved layout, tables, and images
- 🔒 No external API keys required
- 🐳 Docker-ready architecture

## Project Structure

```
pdf2md_service/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application entry point
│   ├── api/                 # API routes and endpoints
│   │   └── __init__.py
│   ├── core/                # Core configuration and settings
│   │   ├── __init__.py
│   │   └── config.py
│   ├── models/              # Pydantic models for request/response
│   │   └── __init__.py
│   ├── services/            # Business logic (PDF conversion)
│   │   └── __init__.py
│   └── utils/               # Utility functions
│       └── __init__.py
├── tests/                   # Test suite
│   └── __init__.py
├── requirements.txt         # Python dependencies
└── README.md
```

## Installation

```bash
# Clone the repository
git clone <repository-url>
cd pdf2md_service

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## Usage

```bash
# Run the server
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

# Or with environment variables
HOST=0.0.0.0 PORT=8000 uvicorn app.main:app --reload
```

## API Endpoints

### Health Check
```bash
GET /health
```

Response:
```json
{
  "status": "healthy",
  "service": "pdf2md-converter"
}
```

### Convert PDF to Markdown (Coming in Phase 2)
```bash
POST /api/v1/convert
Content-Type: multipart/form-data

File: <pdf_file>
```

## API Documentation

Once running, access the interactive API documentation at:
- Swagger UI: http://localhost:8000/api/v1/docs
- ReDoc: http://localhost:8000/api/v1/redoc
- OpenAPI JSON: http://localhost:8000/api/v1/openapi.json

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| HOST | 0.0.0.0 | Server host |
| PORT | 8000 | Server port |
| PROJECT_NAME | PDF to Markdown Converter | Project name |
| VERSION | 0.1.0 | API version |

## License

MIT
