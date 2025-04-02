#!/bin/bash
# Parsing build requires and requires from a spec file

set -e
echo "Welcome! I need the spec file(s) from you."
echo "Write d for directory or f for single file:"
read char

curdir=$(dirname $(realpath "$0"))

if [ "$char" == "d" ]; then
	echo "Write a path to directory of spec files:"
	read dirname

	if [ -e $dirname ]; then
		cd "$dirname"

		for filename in ./*.spec
		do
			echo "Processing $filename file..."
			rpmspec -P $filename | grep -e %package -e BuildRequires -e Requires >> $curdir/pkg.out
			echo "%mainpackage" >> $curdir/pkg.out
			# That's our label to show that the new spec file is processed
		done
		cd "$curdir"
	else
		echo "Error: $dirname does not exist."
		exit 1
	fi

elif [ "$char" == "f" ]; then
	echo "Write a path to spec file:"
	read filename
	if [ -e $filename ]; then
		filedir=$(dirname $(realpath "$filename"))
		cd $filedir
		filename=$(basename "$filename")
		rpmspec -P $filename | grep -e %package -e BuildRequires -e Requires > $curdir/pkg.out
		cd $curdir
	else
		echo "Error: $filename does not exist."
		exit 1
	fi

else # Not d and not f
	echo "Error: wrong input"
	exit 1
fi

echo " "
python3 ./task.py 

