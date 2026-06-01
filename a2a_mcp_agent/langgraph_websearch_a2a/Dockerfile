# Use an official Python runtime as a parent image
FROM python:3.12-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container at /app
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container at /app
COPY stock_search_a2a.py .

# Make port 8083 available to the world outside this container
EXPOSE 8083

# Define environment variable with default value
# This can be overridden at runtime with -e
ENV GOOGLE_API_KEY=""

# Run the A2A agent when the container launches
CMD ["python", "stock_search_a2a.py"]

# Made with Bob
