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

## 🚀 Quick Start

### Using Docker (Recommended)

#### 1. Build and Run the Container

**Option A: Using docker-compose (Easiest)**
```bash
docker-compose up --build
```

**Option B: Using docker commands directly**
```bash
# Build the Docker image
docker build -t pdf2md-service .

# Run the container
docker run -d -p 8000:8000 --name pdf2md-service pdf2md-service
```

#### 2. Access the API

Once the container is running, access the service at:

- **📖 Swagger UI (Interactive API Docs):** http://localhost:8000/docs
- **📄 ReDoc (Alternative API Docs):** http://localhost:8000/redoc
- **❤️ Health Check:** http://localhost:8000/health
- **🔄 API Endpoint:** http://localhost:8000/api/v1/convert

#### 3. Test the Conversion

1. Open http://localhost:8000/docs in your browser
2. Find the `POST /api/v1/convert` endpoint
3. Click **"Try it out"**
4. Upload a PDF file
5. Click **"Execute"**
6. View the Markdown output in the response

#### 4. Stopping the Service

**If using docker-compose:**
```bash
docker-compose down
```

**If using docker directly:**
```bash
docker stop pdf2md-service
docker rm pdf2md-service
```

---

### Local Development (Without Docker)

```bash
# Run the server
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

# Or with environment variables
HOST=0.0.0.0 PORT=8000 uvicorn app.main:app --reload
```

---

## 📡 API Endpoints

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

### Convert PDF to Markdown
```bash
POST /api/v1/convert
Content-Type: multipart/form-data

File: <pdf_file>
```

**Response:**
```json
{
  "filename": "document.pdf",
  "markdown": "# Document Title\n\nContent in markdown format..."
}
```

---

## 📚 API Documentation

Once running, access the interactive API documentation at:

- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc
- **OpenAPI JSON:** http://localhost:8000/openapi.json

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| HOST | 0.0.0.0 | Server host |
| PORT | 8000 | Server port |
| PROJECT_NAME | PDF to Markdown Converter | Project name |
| VERSION | 0.1.0 | API version |

## License

MIT
