#!/bin/bash

# ./usrun.sh -p batch --time 48:00:00 --gpus 1 --mem 32GB --pty /bin/bash
export PIP_INDEX_URL=http://pypi-cache/index
export PIP_TRUSTED_HOST=pypi-cache
export PIP_NO_CACHE=true
export HUGGINGFACE_CACHE_DIR=/ds/models/llms/cache
export HUGGINGFACE_HUB_CACHE=/ds/models/llms/cache
export HF_DATASETS_CACHE=/netscratch/nehring/cache/hf_datasets

#cd "$(dirname "$0")"
#cd ..

cd /netscratch/nehring/projects/industry/benchmarking/lm-evaluation-harness
pip install -e .


python main.py \
    --model llm-tools \
    --tasks squad2 \

