FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY . .

# Expose port 5000 for the Flask app
EXPOSE 8000

# Run the Flask server
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "-w", "2", "main:app"]