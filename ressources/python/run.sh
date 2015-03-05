#!/bin/bash

if [ "$1" = 1 ]; then

    if ! python -c "from main import run;run(1)"; then
        exit 4
    fi

    if ! ./testResults.py; then
        exit 3
    fi
fi

if ! python -c "from main import run;run(0)"; then
    exit 5
fi

exit 0
