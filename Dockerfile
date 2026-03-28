# Select a lightweight base image for Python
FROM python:3.10-slim

# Define the container's work directory
WORKDIR /app

# Download the requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of project files into container
COPY . .

# Expose port 7860 for Hugging Face Spaces routing
EXPOSE 7860

# Run Fast API server using uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "7860"]