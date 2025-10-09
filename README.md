# 🖼️ Gallery - 静态图片画廊生成器

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![GitHub Pages](https://img.shields.io/badge/GitHub%20Pages-Deployed-brightgreen.svg)](https://pages.github.com/)

一个简洁、现代、高性能的静态图片和视频画廊生成器，专为个人作品集、项目展示和内容管理设计。支持自定义主题、响应式设计和自动部署。

## ✨ 核心特性

### 🎨 设计特性
- **简洁现代设计** - 采用极简主义设计理念，突出内容本身
- **响应式布局** - 完美适配桌面、平板和移动设备
- **自定义主题** - 支持字体、颜色、布局的完全自定义
- **优雅动画** - 流畅的过渡动画和交互效果

### 📱 功能特性
- **多媒体支持** - 支持图片和视频文件的混合展示
- **相册排序** - 支持通过文件夹序号自定义相册显示顺序
- **智能分页** - 自动分页显示，每页9个项目，提升加载性能
- **链接复制** - 一键复制媒体文件链接，便于分享
- **动态版权** - 自动计算和显示版权年份范围
- **SEO优化** - 完整的meta标签和结构化数据
- **性能优化** - 懒加载、预加载、并行处理等优化技术

### 🚀 部署特性
- **零配置部署** - 集成GitHub Actions，推送即部署
- **静态网站** - 纯静态HTML/CSS/JS，无服务器依赖
- **CDN友好** - 支持各种CDN和静态托管服务
- **增量构建** - 智能检测文件变化，只构建必要部分

## 🚀 快速开始

### 环境要求

- Python 3.8 或更高版本
- Git（用于版本控制）
- GitHub账户（用于自动部署）

### 安装步骤

1. **克隆仓库**
   ```bash
   git clone https://github.com/GWen124/Gallery.git
   cd Gallery
   ```

2. **安装依赖**
   ```bash
   pip install -r requirements.txt
   ```

3. **配置画廊**
   
   编辑 `config.json` 文件：
   ```json
   {
     "input": "./",
     "output": "./build_output",
     "title": "我的图片画廊",
     "footer": "GALLERY.GW124.TOP",
     "footer-link": "https://gallery.gw124.top",
     "title-font": "brand",
     "footer-font": "brand",
     "global-font": "brand"
   }
   ```

4. **添加媒体文件**
   
   将您的图片和视频放入相应的文件夹中：
   ```
   Gallery/
   ├── 01-Animation/       # 动画文件夹（带序号，优先显示）
   │   ├── animation1.gif
   │   └── animation2.mp4
   ├── 02-Avatar/          # 头像文件夹
   │   ├── avatar1.jpg
   │   └── avatar2.png
   └── Background/         # 背景文件夹（无序号，按名称排序）
       └── bg1.jpg
   ```
   
   💡 **相册排序提示**：在文件夹名前添加序号（如 `01-`、`02-`）可以自定义相册显示顺序，序号在页面上会自动隐藏。

5. **本地预览**
   ```bash
   # 构建画廊
   python build_gallery.py
   
   # 启动本地服务器
   cd build_output
   python -m http.server 8000
   ```
   
   访问 `http://localhost:8000` 查看效果

6. **部署到GitHub Pages**
   ```bash
   git add .
   git commit -m "更新画廊内容"
   git push origin main
   ```

## ⚙️ 配置说明

### config.json 参数详解

| 参数 | 类型 | 说明 | 默认值 | 示例 |
|------|------|------|--------|------|
| `input` | string | 媒体文件输入目录 | `./gallery` | `./` |
| `output` | string | 构建输出目录 | `./build_output` | `./dist` |
| `title` | string | 网站标题 | `Image Gallery` | `我的作品集` |
| `footer` | string | 页脚显示名称 | `Gallery` | `我的网站` |
| `footer-link` | string | 页脚链接地址 | `#` | `https://example.com` |
| `title-font` | string | 标题字体 | 空（使用默认） | `brand` |
| `footer-font` | string | 页脚字体 | 空（使用默认） | `brand` |
| `global-font` | string | 全局字体 | 空（使用默认） | `brand` |
| `start-date` | string | 版权起始日期 | 空（仅当前年份） | `2020-10-01` |
| `start-year` | number | 版权起始年份 | 空（仅当前年份） | `2020` |
| `galleries` | object | 相册封面配置 | `{}` | 见下方示例 |

### 版权年份配置

页脚会根据配置自动显示版权年份：
- 设置 `start-date: "2020-10-01"` 且当前年份是 2025 → 显示 `© 2020-2025`
- 设置 `start-year: 2020` 且当前年份是 2025 → 显示 `© 2020-2025`
- 起始年份等于当前年份 → 只显示 `© 2025`
- 未设置任何起始时间 → 只显示当前年份 `© 2025`

支持的日期格式：`YYYY-MM-DD`、`YYYY/MM/DD`、`YYYY.MM.DD`

### 相册排序配置

通过在文件夹名称前添加序号来控制相册显示顺序：

**支持的格式：**
- `01-相册名` （推荐，使用连字符）
- `01_相册名` （使用下划线）
- `01.相册名` （使用点号）
- `01 相册名` （使用空格）

**示例：**
```
文件夹结构：
├── 01-精选作品     → 显示为 "精选作品"
├── 02-最新更新     → 显示为 "最新更新"
├── 03-经典收藏     → 显示为 "经典收藏"
└── Others         → 显示为 "Others"（无序号，按名称排序）
```

**注意事项：**
- 页面上会自动隐藏序号前缀，只显示相册名称
- 文件路径仍使用完整的文件夹名（包含序号）
- 在 `config.json` 配置封面时需使用完整名称（包含序号）
- 有序号的相册会排在无序号的相册前面

### 相册封面配置

```json
{
  "galleries": {
    "Animation": {
      "cover": "https://example.com/custom-cover.jpg"
    },
    "Avatar": {
      "cover": "./custom-avatar-cover.png"
    }
  }
}
```

### 字体配置选项

- `brand` - 使用项目内置的Brand字体
- `"Arial, sans-serif"` - 使用系统字体
- `""` - 使用默认字体栈

## 📁 项目结构

```
Gallery/
├── .github/
│   └── workflows/
│       └── deploy.yml          # GitHub Actions 部署工作流
├── assets/
│   └── fonts/
│       └── brand.ttf           # 自定义字体文件
├── themes/
│   └── simple/
│       ├── style.css           # 主题样式文件
│       └── enhancements.js     # 增强功能脚本
├── build_gallery.py            # 核心生成器脚本
├── config.json                 # 配置文件
├── requirements.txt            # Python依赖
├── README.md                   # 项目说明
├── CONTRIBUTING.md             # 贡献指南
├── CHANGELOG.md                # 更新日志
├── LICENSE                     # 开源许可证
└── build_output/               # 构建输出目录（自动生成）
    ├── index.html              # 首页
    ├── style.css               # 样式文件
    ├── enhancements.js         # 脚本文件
    ├── config.json             # 配置文件副本
    └── [相册文件夹]/            # 媒体文件
```

## 🎨 主题定制

### 添加自定义字体

1. 将字体文件放入 `assets/fonts/` 目录
2. 在 `config.json` 中设置字体参数
3. 重新构建项目

支持的字体格式：
- TTF (.ttf)
- OTF (.otf)
- WOFF (.woff)
- WOFF2 (.woff2)

### 修改样式

编辑 `themes/simple/style.css` 文件：

```css
:root {
  --primary-color: #your-color;      /* 主色调 */
  --secondary-color: #your-color;    /* 辅助色 */
  --background-color: #your-color;   /* 背景色 */
  --card-background: #your-color;    /* 卡片背景 */
  --text-color: #your-color;         /* 文字颜色 */
  --border-radius: 12px;             /* 圆角大小 */
  --shadow: 0 4px 12px rgba(0,0,0,0.1); /* 阴影效果 */
}
```

### 自定义布局

可以通过修改CSS变量来调整：
- 网格列数
- 间距大小
- 动画效果
- 响应式断点

## 📋 支持的媒体格式

### 图片格式
- **JPEG** (.jpg, .jpeg) - 推荐用于照片
- **PNG** (.png) - 推荐用于图形和透明图片
- **GIF** (.gif) - 支持动画GIF
- **WebP** (.webp) - 现代格式，文件更小
- **BMP** (.bmp) - Windows位图
- **TIFF** (.tiff) - 高质量图片
- **SVG** (.svg) - 矢量图形

### 视频格式
- **MP4** (.mp4) - 推荐格式，兼容性最好
- **WebM** (.webm) - 现代格式，文件更小
- **AVI** (.avi) - 传统格式
- **MOV** (.mov) - QuickTime格式
- **WMV** (.wmv) - Windows媒体格式
- **FLV** (.flv) - Flash视频
- **MKV** (.mkv) - 高质量视频
- **M4V** (.m4v) - iTunes视频

## 🚀 部署指南

### GitHub Pages（推荐）

1. **Fork本仓库**
   - 访问 [Gallery仓库](https://github.com/GWen124/Gallery)
   - 点击右上角的"Fork"按钮

2. **启用GitHub Pages**
   - 进入你的Fork仓库
   - 点击"Settings"标签
   - 滚动到"Pages"部分
   - 选择"GitHub Actions"作为源

3. **推送代码**
   ```bash
   git add .
   git commit -m "初始化画廊"
   git push origin main
   ```

4. **访问你的画廊**
   - 等待GitHub Actions完成构建
   - 访问 `https://你的用户名.github.io/Gallery`

### 其他静态托管服务

#### Netlify
1. 运行 `python build_gallery.py` 构建项目
2. 将 `build_output/` 目录拖拽到Netlify
3. 或连接GitHub仓库自动部署

#### Vercel
1. 安装Vercel CLI: `npm i -g vercel`
2. 在项目根目录运行: `vercel`
3. 选择 `build_output` 作为输出目录

#### 自定义服务器
1. 构建项目: `python build_gallery.py`
2. 将 `build_output/` 目录内容上传到你的服务器
3. 配置Web服务器（Nginx/Apache）提供静态文件

## 🔧 开发指南

### 本地开发环境

```bash
# 克隆仓库
git clone https://github.com/GWen124/Gallery.git
cd Gallery

# 创建虚拟环境（推荐）
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或
venv\Scripts\activate     # Windows

# 安装依赖
pip install -r requirements.txt

# 开发模式构建
python build_gallery.py

# 启动开发服务器
cd build_output
python -m http.server 8000
```

### 添加新功能

1. **修改生成器** - 编辑 `build_gallery.py`
2. **更新样式** - 修改 `themes/simple/style.css`
3. **增强交互** - 更新 `themes/simple/enhancements.js`
4. **测试功能** - 本地构建和测试
5. **提交代码** - 遵循[贡献指南](CONTRIBUTING.md)

### 调试技巧

- 使用浏览器开发者工具检查CSS和JavaScript
- 查看控制台错误信息
- 检查网络请求状态
- 验证文件路径和权限

## 📊 性能优化

### 构建优化
- **增量构建** - 只处理修改过的文件
- **并行处理** - 多线程复制和生成
- **智能缓存** - 避免重复处理相同文件

### 运行时优化
- **懒加载** - 图片延迟加载
- **预加载** - 关键资源预加载
- **压缩优化** - CSS和JS压缩
- **CDN加速** - 静态资源CDN分发

### 性能监控
- 使用浏览器开发者工具的Performance面板
- 监控Core Web Vitals指标
- 测试不同网络条件下的加载速度

## 🤝 贡献指南

我们欢迎所有形式的贡献！请查看 [CONTRIBUTING.md](CONTRIBUTING.md) 了解详细的贡献指南。

### 贡献方式
- 🐛 **报告Bug** - 使用GitHub Issues
- 💡 **功能建议** - 提出新功能想法
- 📝 **文档改进** - 完善文档内容
- 🔧 **代码贡献** - 提交Pull Request

### 开发规范
- 遵循PEP 8 Python代码规范
- 使用有意义的提交信息
- 添加适当的注释和文档
- 测试新功能的兼容性

## 📄 许可证

本项目采用 [MIT许可证](LICENSE) - 查看LICENSE文件了解详情。

## 🙏 致谢

- 感谢所有贡献者的支持和反馈
- 特别感谢 [Thumbsup](https://github.com/thumbsup/thumbsup) 项目的启发
- 感谢开源社区提供的优秀工具和库

## 📞 支持与联系

- **GitHub Issues** - [报告问题](https://github.com/GWen124/Gallery/issues)
- **GitHub Discussions** - [讨论功能](https://github.com/GWen124/Gallery/discussions)
- **个人网站** - [GW124.TOP](https://gw124.top/)

---

**Powered by [Wen](https://gw124.top/) • Made with ❤️ for the community**