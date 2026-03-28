#!/usr/bin/env python3
"""
简单的 HTTP 隧道服务 - 使用 serveo.net 无需验证
"""
import subprocess
import re
import time
import sys

def create_tunnel():
    """创建 serveo 隧道并提取 URL"""
    print("正在创建隧道...")
    
    # 使用 ssh 创建隧道
    process = subprocess.Popen(
        ['ssh', '-o', 'StrictHostKeyChecking=no', '-R', '80:localhost:5001', 'serveo.net'],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True
    )
    
    url = None
    for line in process.stdout:
        print(line, end='')
        # 提取 URL
        match = re.search(r'https://[a-z0-9-]+\.serveousercontent\.com', line)
        if match:
            url = match.group(0)
            print(f"\n✅ 隧道已创建: {url}")
            print(f"📁 图片库: {url}/library")
            print(f"🎨 设计灵感: {url}/design")
            break
    
    # 保持进程运行
    try:
        process.wait()
    except KeyboardInterrupt:
        print("\n正在关闭隧道...")
        process.terminate()

if __name__ == '__main__':
    create_tunnel()
