FROM python:3.11-slim

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Set working directory
WORKDIR /app

# Copy application files
COPY . .

# Expose API port
EXPOSE 8676

# Run the app
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8676"]