# Use an official Python runtime as a parent image
FROM python:3.12-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container at /app
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container at /app
COPY a2a_agent.py .

# Make port 8082 available to the world outside this container
EXPOSE 8082

# Define environment variables with default values
# These can be overridden at runtime with -e
ENV MCP_SERVER_URL=http://localhost:8081/mcp
ENV GOOGLE_API_KEY=""

# Run the A2A agent when the container launches
CMD ["python", "a2a_agent.py"]
