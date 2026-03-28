# Fashion Design Studio - 服装设计图片库

一个专业的服装设计图片库系统，支持图片管理、分类、搜索和设计功能。

## 功能特点

- 📷 **图片库管理** - 上传、删除、分类管理图片
- 🔍 **智能搜索** - 按标签、分类、描述搜索图片
- 🎨 **设计模块** - 基于参考图片生成设计方案
- 🌐 **多语言支持** - 支持中文和英文
- 📱 **响应式设计** - 适配各种设备

## 在线访问

部署到 GitHub Pages 后访问：
```
https://davonute852-creator.github.io/fashion-os/
```

## 本地运行

```bash
pip install -r requirements.txt
python app.py
```

访问 http://localhost:5001

## 目录结构

```
web/
├── app.py              # Flask 应用主文件
├── requirements.txt    # Python 依赖
├── data/
│   └── images.json    # 图片元数据
├── static/
│   └── uploads/       # 上传的图片
└── templates/         # HTML 模板
    ├── base.html
    ├── index.html
    ├── library.html
    └── design.html
```

## 与飞书机器人集成

飞书机器人搜索的图片会自动同步到此图片库中。

## 技术栈

- Python 3.10+
- Flask
- HTML5/CSS3
- JavaScript
