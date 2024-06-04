#!/bin/bash
set -m
python3 /opt/acestream/search.py &
/opt/acestream/start-engine --client-console --bind-all
fg %1