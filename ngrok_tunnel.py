#!/usr/bin/env python3
"""
使用 ngrok 创建隧道 - 需要配置 authtoken
"""
import subprocess
import json
import time

def create_ngrok_tunnel():
    """创建 ngrok 隧道"""
    print("正在启动 ngrok 隧道...")
    
    # 启动 ngrok
    process = subprocess.Popen(
        ['ngrok', 'http', '5001', '--log=stdout'],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True
    )
    
    print("等待 ngrok 启动...")
    time.sleep(3)
    
    # 获取隧道 URL
    try:
        result = subprocess.run(
            ['curl', '-s', 'http://localhost:4040/api/tunnels'],
            capture_output=True,
            text=True,
            timeout=5
        )
        data = json.loads(result.stdout)
        if 'tunnels' in data and len(data['tunnels']) > 0:
            url = data['tunnels'][0]['public_url']
            print(f"\n✅ 隧道已创建: {url}")
            print(f"📁 图片库: {url}/library")
            print(f"🎨 设计灵感: {url}/design")
            return url
    except Exception as e:
        print(f"获取隧道信息失败: {e}")
    
    # 保持进程运行
    try:
        process.wait()
    except KeyboardInterrupt:
        print("\n正在关闭隧道...")
        process.terminate()

if __name__ == '__main__':
    create_ngrok_tunnel()
