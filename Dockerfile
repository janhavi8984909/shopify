FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all project files
COPY . .

# Make startup script executable
RUN chmod +x start_all.sh

# Expose main port
EXPOSE 8000

# Start all services
CMD ["./start_all.sh"]
