# Use an official Python base image
FROM python:3.11-slim

# Set the working directory
WORKDIR /app

# Copy files into the container
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the Flask port
EXPOSE 5000

# Start the server
CMD ["python", "app.py"]
