FROM python:3.10-slim

# Set the working directory
WORKDIR /app

COPY . .

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5001

CMD ["python", "app.py"]