# Use an official lightweight Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code and data into the container
COPY server.py .
COPY doctors.json .

# Set environment variables to ensure output is not buffered
# This is important for MCP servers using stdio transport
ENV PYTHONUNBUFFERED=1

# Expose the port the server will run on
EXPOSE 8081

# Run the server when the container launches
ENTRYPOINT ["python", "server.py"]
