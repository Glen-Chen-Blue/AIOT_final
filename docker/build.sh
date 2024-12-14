#!/bin/bash

# Assign command-line arguments to variables
s1=$1  # Folder
s2=$2  # Tag

# Build the Docker image with the provided arguments
docker build --build-arg Folder=$s1 --no-cache -f Dockerfile.test -t $s2 .


#  ./build.sh data1 3 first_test
# docker network create chat
# docker run --gpus "device=0" --network chat -p 8000:6000 --name cloud cloud
# docker run --gpus "device=0" --network chat -p 6000:6000 --name edge edge
# curl -X POST http://brave_liskov:6000/bot/ragChat      -H "Content-Type: application/json"      -d '{"query": "甚麼是edge computing？"}'
# docker stop $(docker ps -q)