FROM jupyter/scipy-notebook

USER root
RUN sudo apt-get update && sudo apt install tree -y

USER jovyan
RUN pip install mlflow sklearn
