#!/bin/bash

if $1; then

        make clean-all

        if ! make print; then
                exit 1
        fi

        if ! ./test; then
                exit 4
        fi

        if ! ./testResults.py; then
                exit 3
fi

make clean-all

if ! make; then
        exit 2
fi

if ! ./test; then
        exit 5
fi

exit 0