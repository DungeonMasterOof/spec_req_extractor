#!/bin/bash
# Parsing build requires and requires from a spec file

echo "Write a spec file:"
read filename

rpmspec -q --buildrequires $filename >> br.out

rpmspec -q --requires $filename >> r.out
