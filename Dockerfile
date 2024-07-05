
# Use an official Python runtime as the base image
FROM python:3.8

# Set the working directory inside the container
WORKDIR /app

# Copy your Python script and requirements file into the container
COPY main.py .
COPY requirements.txt .

# Install any necessary dependencies
RUN pip install -r requirements.txt

# Run your Python script
CMD ["python", "main.py"]

# Expose any necessary ports (if applicable)
EXPOSE 8080

# Define a volume for the output directory
VOLUME /output
