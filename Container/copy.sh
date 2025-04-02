#!/bin/bash
# Copying png and graphs from "fedora" Docker container
# MUST BE LAUNCHED BY ROOT USER

# Change if you use another distributive
container_name=fedora

echo "Processing cp from container..."
docker cp ${container_name}_name:/app/build_requires.png /tmp
docker cp ${container_name}_name:/app/runtime_requires.png /tmp
docker cp ${container_name}_name:/app/build_requires /tmp
docker cp ${container_name}_name:/app/runtime_requires /tmp

chmod 666 /tmp/snap-private-tmp/snap.docker/tmp/*
mv /tmp/snap-private-tmp/snap.docker/tmp/*.png ./
mv /tmp/snap-private-tmp/snap.docker/tmp/build_requires ./
mv /tmp/snap-private-tmp/snap.docker/tmp/runtime_requires ./


