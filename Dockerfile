# syntax=docker/dockerfile:1.3

FROM ubuntu:20.04
ENV DEBIAN_FRONTEND=noninteractive
RUN mv /etc/apt/sources.list /etc/apt/sources.list.backup
RUN echo "deb http://mirrors.163.com/ubuntu/ jammy main restricted universe multiverse\n" >> /etc/apt/sources.list
RUN echo "deb http://mirrors.163.com/ubuntu/ jammy-security main restricted universe multiverse\n" >> /etc/apt/sources.list
RUN echo "deb http://mirrors.163.com/ubuntu/ jammy-updates main restricted universe multiverse\n" >> /etc/apt/sources.list
RUN echo "deb http://mirrors.163.com/ubuntu/ jammy-proposed main restricted universe multiverse\n" >> /etc/apt/sources.list
RUN echo "deb http://mirrors.163.com/ubuntu/ jammy-backports main restricted universe multiverse\n" >> /etc/apt/sources.list
RUN echo "deb-src http://mirrors.163.com/ubuntu/ jammy main restricted universe multiverse\n" >> /etc/apt/sources.list
RUN echo "deb-src http://mirrors.163.com/ubuntu/ jammy-security main restricted universe multiverse\n" >> /etc/apt/sources.list
RUN echo "deb-src http://mirrors.163.com/ubuntu/ jammy-updates main restricted universe multiverse\n" >> /etc/apt/sources.list
RUN echo "deb-src http://mirrors.163.com/ubuntu/ jammy-proposed main restricted universe multiverse\n" >> /etc/apt/sources.list
RUN echo "deb-src http://mirrors.163.com/ubuntu/ jammy-backports main restricted universe multiverse\n" >> /etc/apt/sources.list
RUN apt -y update
RUN apt install -y --fix-missing \
    build-essential \
    cmake \
    gfortran \
    git \
    wget \
    curl \
    pkg-config \
    python3-dev \
    python3-pip \
    python3-numpy \
    python3-opencv\
    software-properties-common \
    zip \
    && apt clean && rm -rf /tmp/* /var/tmp/*

COPY backend.py backend.py
COPY requirements.txt requirements.txt
COPY keras_model_9.h5 keras_model_9.h5
RUN --mount=type=cache,target=/root/.cache pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -U pip
RUN --mount=type=cache,target=/root/.cache pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt

CMD uvicorn backend:app --host 0.0.0.0 --port 8888 
