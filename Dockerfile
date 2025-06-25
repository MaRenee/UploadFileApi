# Use official Python base image
FROM python:3.11-slim

# Set the working directory
WORKDIR /app

# Copy project files
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Explicitly install pydantic with email support (email-validator)
RUN pip install --no-cache-dir "pydantic[email]"

# Expose port for the API
EXPOSE 8000

# Run the FastAPI app with Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
