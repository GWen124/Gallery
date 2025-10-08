# 🖼️ Gallery - 静态图片画廊生成器

一个简洁、现代的静态图片和视频画廊生成器，专为GitHub Pages设计。支持自定义主题、响应式设计和自动部署。

## ✨ 特性

- 🎨 **简洁现代设计** - 采用简洁大方的UI设计，支持自定义主题
- 📱 **响应式布局** - 完美适配桌面、平板和移动设备
- 🎬 **多媒体支持** - 支持图片和视频文件展示
- 🔤 **自定义字体** - 支持标题、页脚和全局字体自定义
- 📄 **分页功能** - 自动分页显示，每页9个项目
- 🔗 **链接复制** - 一键复制媒体文件链接
- 🚀 **自动部署** - 集成GitHub Actions，推送即部署
- ⚡ **高性能** - 纯静态网站，加载速度快

## 🚀 快速开始

### 1. 克隆仓库

```bash
git clone https://github.com/GWen124/Gallery.git
cd Gallery
```

### 2. 配置画廊

编辑 `config.json` 文件：

```json
{
  "input": "./gallery",
  "output": "./build_output",
  "title": "Image Gallery",
  "footer": "GALLERY.GW124.TOP",
  "footer-link": "https://gallery.gw124.top",
  "title-font": "brand",
  "footer-font": "brand",
  "global-font": "brand"
}
```

### 3. 添加媒体文件

将您的图片和视频放入 `gallery/` 目录中，按文件夹组织：

```
gallery/
├── Album 1/
│   ├── photo1.jpg
│   └── video1.mp4
├── Album 2/
│   └── photo2.png
└── ...
```

### 4. 安装依赖

```bash
pip install -r requirements.txt
```

### 5. 本地预览

```bash
# 使用Python生成器构建
python build_gallery.py

# 启动本地服务器
cd build_output
python -m http.server 8000
```

### 6. 部署到GitHub Pages

推送代码到GitHub，GitHub Actions将自动构建和部署：

```bash
git add .
git commit -m "更新画廊内容"
git push origin main
```

## ⚙️ 配置说明

### config.json 参数

| 参数 | 类型 | 说明 | 默认值 |
|------|------|------|--------|
| `input` | string | 媒体文件输入目录 | `./gallery` |
| `output` | string | 构建输出目录 | `./build_output` |
| `title` | string | 网站标题 | `Image Gallery` |
| `footer` | string | 页脚显示名称 | `Gallery` |
| `footer-link` | string | 页脚链接地址 | `#` |
| `title-font` | string | 标题字体 | 空（使用默认） |
| `footer-font` | string | 页脚字体 | 空（使用默认） |
| `global-font` | string | 全局字体 | 空（使用默认） |

### 字体配置

支持以下字体配置：

- `brand` - 使用自定义Brand字体
- 自定义字体名称 - 如 `"Arial, sans-serif"`
- 空字符串 - 使用系统默认字体

## 📁 项目结构

```
.
├── .github/workflows/deploy.yml  # GitHub Actions 部署工作流
├── assets/                       # 静态资源 (例如字体)
├── build_gallery.py              # 自定义静态网站生成器
├── build_output/                 # 生成的静态网站文件 (被 .gitignore 忽略)
├── config.json                   # 画廊配置
├── gallery/                      # 您的图片和视频源文件
├── requirements.txt              # Python依赖包
├── themes/simple/                # 主题文件
│   ├── style.css                 # 样式文件
│   └── enhancements.js           # 增强功能脚本
├── .gitignore                    # Git 忽略文件
└── README.md                     # 项目说明
```

## 🎨 主题定制

### 添加自定义字体

1. 将字体文件放入 `assets/fonts/` 目录
2. 在 `config.json` 中设置字体参数
3. 重新构建项目

### 修改样式

编辑 `themes/simple/style.css` 文件来自定义样式：

- 颜色主题
- 布局样式
- 动画效果
- 响应式断点

## 🔧 开发指南

### 本地开发

```bash
# 安装依赖
pip install -r requirements.txt

# 构建项目
python build_gallery.py

# 启动本地服务器
cd build_output
python -m http.server 8000
```

### 添加新功能

1. 修改 `build_gallery.py` 添加生成逻辑
2. 更新 `themes/simple/style.css` 添加样式
3. 修改 `themes/simple/enhancements.js` 添加交互功能

## 📋 支持的媒体格式

### 图片格式
- JPEG (.jpg, .jpeg)
- PNG (.png)
- GIF (.gif)
- WebP (.webp)
- BMP (.bmp)
- TIFF (.tiff)
- SVG (.svg)

### 视频格式
- MP4 (.mp4)
- WebM (.webm)
- AVI (.avi)
- MOV (.mov)
- WMV (.wmv)
- FLV (.flv)
- MKV (.mkv)
- M4V (.m4v)

## 🚀 部署

### GitHub Pages

1. Fork 本仓库
2. 在仓库设置中启用 GitHub Pages
3. 推送代码，GitHub Actions 将自动部署

### 其他静态托管

1. 运行 `python build_gallery.py` 构建项目
2. 将 `build_output/` 目录内容上传到您的静态托管服务

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

## 🙏 致谢

- 感谢所有贡献者的支持
- 特别感谢 [Thumbsup](https://github.com/thumbsup/thumbsup) 项目的启发

---

**Powered by [Wen](https://gw124.top/)**# Trigger rebuild
