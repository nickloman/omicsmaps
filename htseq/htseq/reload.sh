#!/bin/bash

# Replace these three settings.
PROJDIR="/home/nick/maps/htseq"
PIDFILE="$PROJDIR/maps.pid"

cd $PROJDIR
if [ -f $PIDFILE ]; then
    kill `cat -- $PIDFILE`
    rm -f -- $PIDFILE
fi

exec /usr/bin/env - \
  python manage.py runfcgi host=127.0.0.1 port=8802 method=threaded pidfile=$PIDFILE daemonize=true
`
