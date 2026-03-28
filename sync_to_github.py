#!/usr/bin/env python3
"""
同步图片库到GitHub Pages
自动将新采集的图片提交到GitHub仓库
"""

import os
import subprocess
import json
from datetime import datetime

def run_command(cmd, cwd=None):
    """运行shell命令"""
    result = subprocess.run(cmd, shell=True, cwd=cwd, capture_output=True, text=True)
    return result.returncode == 0, result.stdout, result.stderr

def sync_to_github():
    """同步图片库到GitHub"""
    web_dir = "/Users/zhangyanqiang/Downloads/OS/web"
    
    print("🔄 开始同步图片库到GitHub...")
    print("=" * 50)
    
    # 1. 检查是否有新图片
    print("\n📁 检查新图片...")
    success, stdout, stderr = run_command("git status --short", cwd=web_dir)
    
    if not stdout.strip():
        print("✅ 没有新图片需要同步")
        return True
    
    print(f"发现更改:\n{stdout}")
    
    # 2. 复制静态文件到docs目录（用于GitHub Pages）
    print("\n📋 更新docs目录...")
    run_command("cp static/library_static.html docs/index.html", cwd=web_dir)
    run_command("cp static/design_static.html docs/", cwd=web_dir)
    run_command("cp data/images.json docs/data/", cwd=web_dir)
    run_command("cp -r static/uploads/* docs/uploads/ 2>/dev/null || true", cwd=web_dir)
    
    # 3. 添加所有更改
    print("\n📤 添加文件到git...")
    run_command("git add docs/ data/ static/uploads/", cwd=web_dir)
    
    # 4. 提交更改
    print("\n💾 提交更改...")
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    commit_msg = f"自动同步图片库 - {timestamp}\n\n- 更新图片数据\n- 同步新采集的图片到GitHub Pages"
    
    success, stdout, stderr = run_command(f'git commit -m "{commit_msg}"', cwd=web_dir)
    if not success:
        print(f"⚠️ 提交失败或无更改: {stderr}")
        return False
    
    print(f"✅ 提交成功: {stdout}")
    
    # 5. 推送到GitHub
    print("\n🚀 推送到GitHub...")
    success, stdout, stderr = run_command("git push origin main", cwd=web_dir)
    if not success:
        print(f"❌ 推送失败: {stderr}")
        return False
    
    print(f"✅ 推送成功!")
    print("\n" + "=" * 50)
    print("🎉 同步完成!")
    print(f"📍 GitHub Pages将在几分钟后更新")
    print(f"🔗 访问: https://davonute852-creator.github.io/fashion-os/")
    
    return True

if __name__ == "__main__":
    sync_to_github()
