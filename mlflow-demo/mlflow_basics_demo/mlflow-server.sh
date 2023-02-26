#!/bin/bash
CONTAINER_NAME=mlflow_demo

if [ "$(docker ps -aq -f status=running -f name=$CONTAINER_NAME)" ]; then
  docker exec -it $CONTAINER_NAME mlflow server -h 0.0.0.0 -p 4000 --serve-artifacts
fi
