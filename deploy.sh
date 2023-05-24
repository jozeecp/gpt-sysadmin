#!/bin/bash

# Check if Docker is installed
if ! command -v docker &> /dev/null
then
    echo "Docker is not installed. Please install Docker before running this script."
    exit 1
fi

# Check if Docker is running by trying to get the version info
if ! docker version &> /dev/null
then
    echo "Docker is not running. Please start Docker before running this script."
    exit 1
fi

echo "Building GPT-SysAdmin..."
echo "Starting at: $(date)"

# Step 0: Remove existing containers
echo "Removing existing containers..."
docker-compose down --remove-orphans

# Step 1: Create SSH key named test_idrsa_key (with no password)
rm ./test_idrsa_key*
ssh-keygen -t rsa -b 4096 -C "example@example.com" -f ./test_idrsa_key -N ''
echo "SSH key created"

# Step 2: Export SSH public key as variable PUBLIC_KEY
export PUBLIC_KEY=$(cat ./test_idrsa_key.pub)
echo "SSH public key exported as variable PUBLIC_KEY:"
echo $PUBLIC_KEY

# Step 3: Build application
time docker-compose build

# Step 4: Start application
echo "starting application..."
docker-compose up -d
echo ""
echo ""
echo "Application started at: $(date)"

# step 4.5: print IPs of services
docker inspect -f '{{range.NetworkSettings.Networks}}{{.IPAddress}}{{end}}' $(docker ps -aqf "name=backend")
docker inspect -f '{{range.NetworkSettings.Networks}}{{.IPAddress}}{{end}}' $(docker ps -aqf "name=frontend")
docker inspect -f '{{range.NetworkSettings.Networks}}{{.IPAddress}}{{end}}' $(docker ps -aqf "name=redis")
docker inspect -f '{{range.NetworkSettings.Networks}}{{.IPAddress}}{{end}}' $(docker ps -aqf "name=test_host")

# Step 5: Print some useful commands the user can use to monitor or interact with the containers
echo ""
echo ""
echo "Access UI at http://localhost:80"
echo "API running at http://localhost:5000"
echo "Grafana monitoring UI running at http://localhost:3000"
echo ""
echo ""
echo "To monitor the logs of the containers, you can use:"
echo "docker-compose logs -f"
echo ""
echo "To interact with a specific service, you can use:"
echo "docker-compose exec backend bash   # for the backend service"
echo "docker-compose exec frontend bash  # for the frontend service"
echo "docker-compose exec redis bash     # for the redis service"
echo "docker-compose exec test_host bash # for the test_host service"
echo ""
echo "To monitor the logs of a specific service, you can use:"
echo "docker-compose logs -f backend   # for the backend service"
echo "docker-compose logs -f frontend  # for the frontend service"
echo "docker-compose logs -f redis     # for the redis service"
echo "docker-compose logs -f test_host # for the test_host service"

exit 0
