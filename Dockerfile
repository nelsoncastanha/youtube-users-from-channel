# Use a slim Python base image
FROM python:3.11-slim

# Set the working directory inside the container
WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy your application code
COPY src ./src

# Copy tests folder
COPY tests ./tests

# Set default command (you can override it when running)
ENTRYPOINT ["python", "src/main.py"]