#!/bin/bash
PYTHONPATH="/home/nick/maps:/home/nick/maps/htseq"
export PYTHONPATH
export DJANGO_SETTINGS_MODULE=htseq.settings
exec $1 $2
