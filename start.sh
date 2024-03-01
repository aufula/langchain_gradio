#!/bin/bash
ps -ef|grep run_chatbot|grep -v grep|awk "{print \$2}"|xargs kill -9 >/dev/null 2>&1
source venv/bin/activate
nohup python3 run_chatbot.py &
