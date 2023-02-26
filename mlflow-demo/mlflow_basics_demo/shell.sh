#!/bin/bash
CONTAINER_NAME=mlflow_demo

if [ "$(docker ps -aq -f status=running -f name=$CONTAINER_NAME)" ]; then
    docker exec -it $CONTAINER_NAME bash
fi
