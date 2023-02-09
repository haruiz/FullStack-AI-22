#!/bin/bash
IMAGE_NAME=mlflow_demo_image
CONTAINER_NAME=mlflow_jupyter
docker build -t mlflow_demo .

if [ "$(docker ps -aq -f status=running -f name=$CONTAINER_NAME)" ]; then
    docker kill $CONTAINER_NAME
fi
docker rm $CONTAINER_NAME
# shellcheck disable=SC2046
docker run --name $CONTAINER_NAME -p 8888:8888 -p 4000:4000 -v $(pwd):/home/jovyan/ -it $IMAGE_NAME
