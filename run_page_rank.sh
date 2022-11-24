#!/bin/bash

python /src/prepare_data.py 
python /src/page_rank.py data/data.txt > data/out.json --iter=30 --damping-factor=0.85