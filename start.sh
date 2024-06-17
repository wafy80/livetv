#!/bin/bash
cd /opt/acestream/playlist
set -m
gunicorn -w 2 -b 0.0.0.0:6880 --access-logfile search.log search:app &
/opt/acestream/start-engine --client-console --bind-all
fg %1
