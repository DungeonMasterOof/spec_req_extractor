# Change if you want to use another directory
FROM fedora:latest

RUN dnf install -y make rpmspec python3 python3-graphviz && \
    dnf clean all

WORKDIR /app

COPY . .

