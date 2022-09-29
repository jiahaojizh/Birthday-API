#!/bin/sh

# Build docker image
echo "Building docker image..."
docker build . -t hello

# Create database if it is not present already
echo "Creating database..."
if test -f ./database/birthday.db; then 
    echo "Database created, skipping creation process.."; 
else
    python3 ./flaskr/init-db.py;
fi

# Run docker container with volume mount
echo "Starting docker container..."
docker run -d -v $(pwd)/database:/app/database hello