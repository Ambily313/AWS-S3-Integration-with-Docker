# Use a Python base image
FROM python:3.9-slim-buster

# Set the working directory in the container
WORKDIR /app

# Copy the application code into the container
COPY . /app/

# Install any dependencies
RUN pip install -r requirements.txt

# Set an environment variable (example)
ENV DEFAULT_NAME="User"

# Make the script executable
CMD ["python", "/app/greeting_app.py"]