#!/bin/bash
APP_DIR=`dirname $0`
cd $APP_DIR
echo $APP_DIR
exec bin/gunicorn app:app \
  --name assignment \
  -w 4 \
  -b localhost:8000 \
  -t 300
