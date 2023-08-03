cd /opt/lowcode_langchain

mkdir -p /var/log/lowcode_langchain
export PYTHONPATH=.:$PYTHONPATH
export PORT0=6668

python3 ai_proxy/server.py --port $PORT0 1>>/var/log/lowcode_langchain/stdout.log 2>>/var/log/lowcode_langchain/stderr.log
