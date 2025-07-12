# Use a lightweight Python image as the base
FROM python:3.12-slim-bookworm

# Set the working directory in the container
WORKDIR /app

# Install uv (a fast Python package installer and resolver)
# See: https://github.com/astral-sh/uv
RUN pip install uv

# Copy pyproject.toml and uv.lock to leverage Docker cache for dependencies
COPY pyproject.toml uv.lock ./

# Install backend dependencies using uv
RUN uv sync

# Copy the rest of the application code
COPY . .

# Expose the port FastAPI runs on
EXPOSE 8000

# Command to run the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
