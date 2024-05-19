#!/bin/bash
set -m
python3 /opt/acelist/search.py &
/opt/acestream/start-engine --client-console --bind-all
fg %1