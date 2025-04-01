#!/bin/bash
# Building and running the "$container_name" Docker cointainer 
# MUST BE LAUNCHED BY ROOT USER

# Change if you query rpm from other distributives
container_name=fedora

echo "Do you want to rebuild ${container_name}_cont ?"
echo "y/n:"
read char

if [[ "$char" == "n" || "$char" == "N" ]]; then

	availability_check=$(docker container ps -a | grep -o ${container_name})

	if [ -z "$availability_check" ]; then
		echo "Building container from Dockerfile..."
		docker build -t "${container_name}_cont" .

		echo "Launching the container..."
		docker run --name "${container_name}" -it "${container_name}_cont"
	else
		echo "Launching the container..."
		docker run -it "${container_name}_cont"
	fi

elif [[ "$char" == "y" || "$char" == "Y" ]]; then

	echo "Building container from Dockerfile..."
	docker build -t "${container_name}_cont" .

	echo "Launching the container..."
	docker run -it "${container_name}_cont"

else
	echo "Wrong input"
	exit 1
fi
