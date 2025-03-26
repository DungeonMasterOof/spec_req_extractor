#!/bin/bash
# Parsing build requires and requires from a spec file

echo "Welcome! I need the spec file(s) from you."
echo "Write d for directory or f for single file:"
read char
if [ "$char" == "d" ]; then
	echo "Write a directory of spec files:"
	read dirname

	if [ -e $dirname ]; then
		for filename in $dirname/*
		do
			echo "Processing $filename file..."
		        rpmspec -q --buildrequires $filename >> br.out
		        rpmspec -q --requires $filename >> r.out
		done
	else
		echo "Error: $dirname does not exist."
		exit 1
	fi

elif [ "$char" == "f" ]; then
	echo "Write a name of spec file:"
	read filename
	rpmspec -q --buildrequires $filename >> br.out
	rpmspec -q --requires $filename >> r.out

else # Not d and not f
	echo "Error: wrong input"
	exit 1
fi
