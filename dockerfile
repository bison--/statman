# Dockerfile

# Set the base image
FROM python:3.9

# Set a working directory
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install the python dependencies
RUN pip install -r requirements.txt

# Copy the rest of the code into the container
COPY . .

# Set the command to run the server
CMD ["python", "app.py"]

