# Use the official Python image as a base image
FROM python:3.11-alpine

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install any dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire local project directory into the container
COPY . .

# Expose port 8080 for the application
EXPOSE 8080

# Command to run the application
CMD ["python", "app/app.py"]
