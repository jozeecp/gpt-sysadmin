# Use the official Python 3.10 image as the base image
FROM python:3.10

# Set the working directory
WORKDIR /app

# Copy the requirements.txt file into the container
COPY requirements.txt .

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Install openssh-server
RUN apt-get update && \
    apt-get install -y openssh-server && \
    apt-get clean

# chmod the /root/.ssh/ directory
RUN mkdir -p /root/.ssh/ && \
    chmod 700 /root/.ssh/

# Copy the Flask app into the container
COPY . .

# Expose the port the app will run on
EXPOSE 5000

# Start the Flask app
CMD ["python", "app.py"]
