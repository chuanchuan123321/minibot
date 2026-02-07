#!/bin/bash
# 设置终端编码和行编辑模式
export LANG=en_US.UTF-8
export LC_ALL=en_US.UTF-8

# 禁用readline的某些功能以避免删除问题
export INPUTRC=/dev/null

# 运行Python脚本
python3 /Users/a1-6/Desktop/AI智能体/chat.py
