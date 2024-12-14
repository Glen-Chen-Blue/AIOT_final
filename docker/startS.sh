#!/bin/bash

nvidia-smi
# 啟動 ollama 服務並等待 10 秒
ollama serve & sleep 10

echo "MODEL_NAME=llama3.1" > .env
ollama run llama3.1
ollama run mxbai-embed-large

chatchat kb -r
chatchat start -a & sleep 10

python3 proxy.py
# tail -f /dev/null
