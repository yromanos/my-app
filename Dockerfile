# Start from an official Python base image
FROM python:3.11-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file first
COPY requirements.txt .

# Install dependencies
RUN pip install -r requirements.txt

# Copy the rest of your app
COPY . .

# Tell Docker what port your app uses
EXPOSE 5000

# The command to run your app
CMD ["python", "src/main.py"]