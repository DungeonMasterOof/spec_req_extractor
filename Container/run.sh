#!/bin/bash
# Building and running the "$container_name" Docker cointainer 
# MUST BE LAUNCHED BY ROOT USER

# Change if you query rpm from other distributives
container_name=fedora

echo "Do you want to build ${container_name}_img?"
echo "y/n:"
read char

availability_check=$(docker container ps -a | grep ${container_name}_name)

if [[ "$char" == "n" || "$char" == "N" ]]; then

	if [ -n "$availability_check" ]; then # If a container with the name exists already
		echo "Removing old container with the name ${container_name}_name..."
		docker rm "${container_name}_name"
	fi

	echo "Launching the container..."
	docker run --name "${container_name}_name" -it "${container_name}_img"
	
elif [[ "$char" == "y" || "$char" == "Y" ]]; then

	echo "Building container from Dockerfile..."
	docker build -t "${container_name}_img" .
	
	if [ -n "$availability_check" ]; then # If a container with the name exists already
		echo "Removing old container with the name ${container_name}_name..."
		docker rm "${container_name}_name"
	fi
	
	echo "Launching the container..."
	docker run --name "${container_name}_name" -it "${container_name}_img"

else
	echo "Wrong input"
	exit 1
fi
