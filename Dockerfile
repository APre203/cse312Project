# Use a lightweight Python image
FROM python:3.9

# Install system dependencies for OpenSSL bindings (adjust for your OS)
RUN apt-get update

# Set working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy your Flask app and other files
COPY . .

# Expose port for Flask app
EXPOSE 8080

# Add wait script
ADD https://github.com/ufoscout/docker-compose-wait/releases/download/2.2.1/wait /wait
RUN chmod +x /wait

# Run the Flask app
CMD /wait && python -u app.py

# Environment variable for MongoDB connection
# Update this to connect to your MongoDB instance
ENV MONGO_URI=mongodb://host.docker.internal:27017/your_database
