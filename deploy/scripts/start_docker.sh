#!/bin/bash
# Login to AWS ECR
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 390844758498.dkr.ecr.us-east-1.amazonaws.com

# Pull the latest image
docker pull 390844758498.dkr.ecr.us-east-1.amazonaws.com/yt-chrome-plugin-personal:latest

# Check if the container 'campusx-app' is running
if [ "$(docker ps -q -f name=campusx-app)" ]; then
    # Stop the running container
    docker stop campusx-app
fi

# Check if the container 'campusx-app' exists (stopped or running)
if [ "$(docker ps -aq -f name=campusx-app)" ]; then
    # Remove the container if it exists
    docker rm campusx-app
fi

# Run a new container
# Replace these lines in your script with environment variables
docker run -p 80:5000 --name campusx-app \
    -e AWS_ACCESS_KEY_ID=AKIAVWABJXHRN6NXDN7W \
    -e AWS_SECRET_ACCESS_KEY=Y9AS8lWEiAkAcYDET26X9AjNq/PqgXoOX7oYYTOd \
    390844758498.dkr.ecr.us-east-1.amazonaws.com/yt-chrome-plugin-personal:latest
