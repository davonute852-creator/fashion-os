# 部署到 GitHub Pages

## 步骤 1: 创建 GitHub 仓库

1. 登录 GitHub: https://github.com/davonute852-creator/fashion-os
2. 确保仓库已存在（之前已创建）

## 步骤 2: 推送代码到 GitHub

在终端中执行：

```bash
cd /Users/zhangyanqiang/Downloads/OS/web

# 添加远程仓库
git remote add origin https://github.com/davonute852-creator/fashion-os.git

# 推送代码
git push -u origin main
```

如果遇到网络问题，可以：
1. 使用 GitHub Desktop 客户端
2. 或者手动上传文件到 GitHub

## 步骤 3: 启用 GitHub Pages

1. 进入仓库页面: https://github.com/davonute852-creator/fashion-os
2. 点击 **Settings** 标签
3. 点击左侧 **Pages** 菜单
4. 在 **Source** 部分选择：
   - **Deploy from a branch**
   - Branch: **main**
   - Folder: **/(root)**
5. 点击 **Save**

## 步骤 4: 等待部署完成

- GitHub Actions 会自动运行部署工作流
- 等待几分钟，访问: https://davonute852-creator.github.io/fashion-os/

## 图片同步说明

飞书机器人搜索的图片会自动保存到 `web/static/uploads/` 目录。

要同步到 GitHub：

```bash
cd /Users/zhangyanqiang/Downloads/OS/web
git add static/uploads/
git commit -m "Sync images from bot"
git push origin main
```

GitHub Actions 会自动重新部署，图片库会更新。

## 自动同步脚本

创建自动同步脚本 `sync_images.sh`：

```bash
#!/bin/bash
cd /Users/zhangyanqiang/Downloads/OS/web
git add static/uploads/ data/images.json
git commit -m "Auto sync: $(date '+%Y-%m-%d %H:%M:%S')"
git push origin main
```

添加到定时任务（每30分钟同步一次）：
```bash
crontab -e
# 添加：
*/30 * * * * /Users/zhangyanqiang/Downloads/OS/web/sync_images.sh
```
