#!/bin/bash

exec bin/gunicorn app:app \
  --name assignment \
  -w 4 \
  -b localhost:8000 \
  -t 300
