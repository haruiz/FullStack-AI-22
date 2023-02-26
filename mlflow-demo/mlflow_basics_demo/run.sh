#!/bin/bash
IMAGE_NAME=mlflow_demo_image
CONTAINER_NAME=mlflow_demo

docker build -t $IMAGE_NAME .
#
#if [ "$(docker ps -aq -f status=running -f name=$CONTAINER_NAME)" ]; then
#    docker kill $CONTAINER_NAME
#fi
# docker rm $CONTAINER_NAME
# shellcheck disable=SC2046
# rm = automatically remove the container when it exits
docker run --name $CONTAINER_NAME  --user root -e GRANT_SUDO=yes --rm -p 8888:8888 -p 4000:4000 -v $(pwd):/home/jovyan/ -it $IMAGE_NAME
