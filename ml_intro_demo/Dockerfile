FROM jupyter/scipy-notebook

USER root
RUN sudo apt-get update
RUN sudo apt-get install libx11-dev libatlas-base-dev libpng-dev -y
RUN sudo apt-get install libgtk-3-dev libboost-python-dev curl ffmpeg mpg123 -y

USER jovyan
RUN pip install -U pip wheel cmake
RUN pip install dlib
RUN pip install scikit-learn imutils opencv-python face_recognition librosa pandas matplotlib seaborn scipy
