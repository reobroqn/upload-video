# Blabla Backend

FastAPI-based backend service for the Blabla video platform.

## Features

- 🚀 FastAPI for high-performance API endpoints
- 🔐 JWT authentication
- 🗄️ PostgreSQL database with SQLAlchemy ORM
- 📦 File uploads to S3 using presigned URLs
- 🎬 Background video processing with Redis
- 📊 API documentation with Swagger UI
- 🧪 Comprehensive test suite with pytest

## Project Structure

```
backend/
├── app/
│   ├── api/              # API routes
│   ├── core/             # Core configurations
│   ├── db/               # Database models and migrations
│   ├── schemas/          # Pydantic models
│   └── services/         # Business logic
├── tests/               # Test files
└── migrations/          # Database migrations
```

## Setup

1. **Create virtual environment and install dependencies**
   ```bash
   uv sync
   ```

2. **Activate the virtual environment**
   ```bash
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Set up environment variables**
   Copy `.env.example` to `.env` and update the values:
   ```bash
   cp .env.example .env
   ```

4. **Run database migrations**
   ```bash
   alembic upgrade head
   ```

## Development

- **Run the development server**:
  ```bash
  uvicorn app.main:app --reload
  ```

- **Run tests**:
  ```bash
  uv run pytest
  ```

- **Generate API documentation**:
  - Swagger UI: http://localhost:8000/docs
  - ReDoc: http://localhost:8000/redoc

## Environment Variables

Required environment variables are defined in `.env.example`. Make sure to set them in your `.env` file.
