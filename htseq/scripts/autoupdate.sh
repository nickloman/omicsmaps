#!/bin/bash

cd /home/nick/maps/htseq/scripts

PYTHONPATH="/home/nick/maps:/home/nick/maps/htseq" DJANGO_SETTINGS_MODULE=htseq.settings python test_akismet.py

