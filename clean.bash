#!/bin/bash

autopep8 ./ --recursive --in-place -a 
autoflake --in-place --remove-all-unused-imports --remove-unused-variables -r ./
