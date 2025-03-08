FROM ubuntu:latest

RUN apt-get update && apt-get install -y \
    curl \
    vim \
    net-tools \
    && rm -rf /var/lib/apt/lists/*

