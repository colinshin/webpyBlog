#!/bin/sh

find . -type f -name "*.pyc" | xargs rm -rf

[ -d data ] && {
    rm -rf data/*
    mkdir -p data/sessions
}

[ -d static/uploads ] && {
    rm -rf static/uploads
    mkdir -p static/uploads
    mkdir -p static/uploads/temp
    mkdir -p static/uploads/video
    mkdir -p static/uploads/audio
    mkdir -p static/uploads/image
}

echo $OSTYPE | grep linux > /dev/null && {
   chown -R lighttpd:lighttpd data
   chown -R lighttpd:lighttpd static
}
