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
- **多媒体支持** - 支持图片（JPEG、PNG、GIF、WebP等）和视频（MP4、WebM等）混合展示
- **智能相册排序** - 通过文件夹序号自定义显示顺序，序号自动隐藏
- **自动分页** - 每页9个项目，提升加载性能和用户体验
- **一键复制链接** - 快速分享媒体文件
- **动态版权年份** - 自动计算和显示版权年份范围
- **自定义封面** - 为每个相册设置独特的封面图片
- **SEO优化** - 完整的meta标签和结构化数据

### 🚀 部署特性
- **零配置部署** - 集成GitHub Actions，推送即自动部署
- **纯静态网站** - 无服务器依赖，部署简单
- **CDN友好** - 支持各种CDN和静态托管服务
- **增量构建** - 智能检测文件变化，只构建必要部分
- **并行处理** - 多线程复制和生成，构建速度快

## 🚀 快速开始

### 环境要求

- Python 3.8 或更高版本
- Git（用于版本控制）
- GitHub账户（用于自动部署，可选）

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
     "footer": "GALLERY.GW124.COM",
     "footer-link": "https://gallery.gw124.com",
     "start-date": "2020-10-01",
     "title-font": "brand",
     "footer-font": "brand",
     "global-font": "brand"
   }
   ```

4. **添加媒体文件**
   
   将您的图片和视频放入相应的文件夹中：
   ```
   Gallery/
   ├── 01-精选作品/        # 带序号，优先显示（页面显示：精选作品）
   │   ├── photo1.jpg
   │   └── photo2.png
   ├── 02-最新更新/        # 第二位显示（页面显示：最新更新）
   │   ├── video1.mp4
   │   └── photo3.jpg
   ├── Animation/         # 无序号，按字母排序
   │   └── animation1.gif
   └── Avatar/            # 无序号，按字母排序
       └── avatar1.jpg
   ```
   
   💡 **相册排序提示**：
   - 在文件夹名前添加序号（如 `01-`、`02-`）可以自定义相册显示顺序
   - 序号在页面上会自动隐藏，只显示相册名称
   - 不添加序号的文件夹会按字母顺序排在后面

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
   
   GitHub Actions 会自动构建并部署到 GitHub Pages

## ⚙️ 配置说明

### config.json 参数详解

| 参数 | 类型 | 说明 | 默认值 | 示例 |
|------|------|------|--------|------|
| `input` | string | 媒体文件输入目录 | `./gallery` | `./` |
| `output` | string | 构建输出目录 | `./build_output` | `./dist` |
| `title` | string | 网站标题 | `Image Gallery` | `我的作品集` |
| `footer` | string | 页脚显示名称 | `Gallery` | `我的网站` |
| `footer-link` | string | 页脚链接地址 | `#` | `https://example.com` |
| `start-date` | string | 版权起始日期 | 空（仅当前年份） | `2020-10-01` |
| `start-year` | number | 版权起始年份 | 空（仅当前年份） | `2020` |
| `title-font` | string | 标题字体 | 空（使用默认） | `brand` |
| `footer-font` | string | 页脚字体 | 空（使用默认） | `brand` |
| `global-font` | string | 全局字体 | 空（使用默认） | `brand` |
| `galleries` | object | 相册封面配置 | `{}` | 见下方示例 |

### 完整配置示例

```json
{
  "input": "./",
  "output": "./build_output",
  "title": "我的图片画廊",
  "footer": "GALLERY.GW124.COM",
  "footer-link": "https://gallery.gw124.com",
  "start-date": "2020-10-01",
  "title-font": "brand",
  "footer-font": "brand",
  "global-font": "brand",
  "galleries": {
    "01-精选作品": {
      "cover": "https://example.com/featured-cover.jpg"
    },
    "02-最新更新": {
      "cover": "https://example.com/latest-cover.jpg"
    },
    "Animation": {
      "cover": "./Animation/custom-cover.gif"
    }
  }
}
```

## 🎯 功能详解

### 1. 相册排序功能

通过在文件夹名称前添加序号来控制相册的显示顺序，序号在页面上会自动隐藏。

#### 支持的格式

| 格式 | 示例 | 页面显示 | 说明 |
|------|------|---------|------|
| `数字-相册名` | `01-风景照片` | `风景照片` | 推荐格式 |
| `数字_相册名` | `02_人物照片` | `人物照片` | 下划线分隔 |
| `数字.相册名` | `03.动物照片` | `动物照片` | 点号分隔 |
| `数字 相册名` | `04 建筑照片` | `建筑照片` | 空格分隔 |
| 无序号 | `其他照片` | `其他照片` | 按字母排序 |

#### 排序规则

1. **有序号的相册**：按序号从小到大排序，显示在最前面
2. **无序号的相册**：按名称字母顺序排序，显示在有序号相册后面
3. **序号可以不连续**：如 3、10、15 也能正确排序
4. **序号可以不从1开始**：如从 03、04 开始也完全可以

#### 使用示例

**示例 1：全部使用序号**
```
文件夹结构：
├── 01-春季风光
├── 02-夏日海滩
├── 03-秋天枫叶
└── 04-冬季雪景

页面显示顺序：
1. 春季风光
2. 夏日海滩
3. 秋天枫叶
4. 冬季雪景
```

**示例 2：混合使用（部分有序号）**
```
文件夹结构：
├── 01-精选照片
├── 02-最新作品
├── Animation
├── Avatar
└── Video

页面显示顺序：
1. 精选照片      ← 有序号，优先显示
2. 最新作品      ← 有序号，优先显示
3. Animation     ← 无序号，按字母排序
4. Avatar        ← 无序号，按字母排序
5. Video         ← 无序号，按字母排序
```

**示例 3：序号不连续**
```
文件夹结构：
├── 03-CineGallery
├── 10-Featured
├── Animation
├── Avatar
└── 15-Latest

页面显示顺序：
1. CineGallery   ← 序号 03
2. Featured      ← 序号 10
3. Latest        ← 序号 15
4. Animation     ← 无序号
5. Avatar        ← 无序号
```

#### 重要提示

⚠️ **文件路径使用完整名称**
- 文件夹 `01-Avatar` 在文件系统中仍是 `01-Avatar`
- 只是在页面显示时自动隐藏序号前缀

⚠️ **config.json 配置需使用完整名称**
```json
{
  "galleries": {
    "01-Avatar": {  // ← 使用完整名称（包含序号）
      "cover": "https://example.com/cover.jpg"
    }
  }
}
```

⚠️ **序号必须在文件夹名开头**
- ✅ 正确：`01-相册名`
- ❌ 错误：`相册名-01`

⚠️ **分隔符必须紧跟序号**
- ✅ 正确：`01-相册名`
- ❌ 错误：`01 - 相册名`（序号和分隔符之间有空格）

#### 使用建议

**方案 A：简单直接**
```
想置顶几个就标几个，序号随意
├── 03-CineGallery
├── 04-Video
└── Animation

✅ 优点：操作简单
⚠️  缺点：将来调整顺序需要重命名
```

**方案 B：预留空间（推荐）**
```
从01开始，间隔使用（如 01、05、10、15）
├── 01-Featured
├── 05-CineGallery
├── 10-Latest
└── 15-Video

✅ 优点：将来可在中间插入（如 02、03、06、11）
✅ 优点：不需要重命名其他文件夹
```

**方案 C：规范管理**
```
从01开始，连续编号
├── 01-Featured
├── 02-CineGallery
├── 03-Latest
└── 04-Video

✅ 优点：整齐规范
⚠️  缺点：插入新相册时需要调整多个序号
```

### 2. 动态版权年份

页脚会根据配置自动显示版权年份，无需手动更新。

#### 配置方式

**方式 1：使用 start-date（推荐）**
```json
{
  "start-date": "2020-10-01"
}
```

**方式 2：使用 start-year**
```json
{
  "start-year": 2020
}
```

#### 显示规则

| 配置 | 当前年份 | 显示效果 |
|------|---------|---------|
| `start-date: "2020-10-01"` | 2025 | `© 2020-2025` |
| `start-year: 2020` | 2025 | `© 2020-2025` |
| `start-date: "2025-01-01"` | 2025 | `© 2025` |
| 未设置 | 2025 | `© 2025` |

#### 支持的日期格式

- `YYYY-MM-DD` - 如 `2020-10-01`
- `YYYY/MM/DD` - 如 `2020/10/01`
- `YYYY.MM.DD` - 如 `2020.10.01`
- `YYYY` - 如 `2020`

### 3. 相册封面配置

为每个相册设置自定义封面图片，支持本地路径和远程URL。

#### 配置示例

```json
{
  "galleries": {
    "Animation": {
      "cover": "https://example.com/custom-cover.jpg"
    },
    "Avatar": {
      "cover": "./Avatar/custom-cover.png"
    },
    "01-Featured": {
      "cover": "https://cdn.example.com/featured.jpg"
    }
  }
}
```

#### 封面路径说明

- **完整URL**：`https://example.com/cover.jpg` - 直接使用
- **相对路径**：`./Avatar/cover.png` - 相对于输出目录
- **未配置**：自动使用相册中的第一个文件作为封面

### 4. 自定义字体

支持为标题、页脚和全局内容设置不同的字体。

#### 字体配置

```json
{
  "title-font": "brand",
  "footer-font": "brand",
  "global-font": "brand"
}
```

#### 字体选项

- `brand` - 使用项目内置的 Brand 字体
- `"Arial, sans-serif"` - 使用系统字体
- `""` - 使用默认字体栈

#### 添加自定义字体

1. 将字体文件放入 `assets/fonts/` 目录
2. 在 `config.json` 中设置字体参数
3. 重新构建项目

支持的字体格式：TTF、OTF、WOFF、WOFF2

## 📋 支持的媒体格式

### 图片格式

| 格式 | 扩展名 | 说明 |
|------|--------|------|
| **JPEG** | `.jpg`, `.jpeg` | 推荐用于照片，兼容性最好 |
| **PNG** | `.png` | 推荐用于图形和透明图片 |
| **GIF** | `.gif` | 支持动画GIF |
| **WebP** | `.webp` | 现代格式，文件更小 |
| **BMP** | `.bmp` | Windows位图 |
| **TIFF** | `.tiff` | 高质量图片 |
| **SVG** | `.svg` | 矢量图形 |

### 视频格式

| 格式 | 扩展名 | 说明 |
|------|--------|------|
| **MP4** | `.mp4` | 推荐格式，兼容性最好 |
| **WebM** | `.webm` | 现代格式，文件更小 |
| **AVI** | `.avi` | 传统格式 |
| **MOV** | `.mov` | QuickTime格式 |
| **WMV** | `.wmv` | Windows媒体格式 |
| **FLV** | `.flv` | Flash视频 |
| **MKV** | `.mkv` | 高质量视频 |
| **M4V** | `.m4v` | iTunes视频 |

## 📁 项目结构

```
Gallery/
├── .github/
│   └── workflows/
│       └── Actions.yml         # GitHub Actions 部署工作流
├── assets/
│   └── fonts/
│       └── brand.ttf           # 自定义字体文件
├── themes/
│   └── simple/
│       ├── style.css           # 主题样式文件
│       └── enhancements.js     # 增强功能脚本
├── [相册文件夹]/                # 您的媒体文件
│   ├── 01-精选作品/
│   ├── 02-最新更新/
│   └── Animation/
├── build_gallery.py            # 核心生成器脚本
├── config.json                 # 配置文件
├── requirements.txt            # Python依赖
├── README.md                   # 项目说明
└── build_output/               # 构建输出目录（自动生成）
    ├── index.html              # 首页
    ├── style.css               # 样式文件
    ├── enhancements.js         # 脚本文件
    ├── config.json             # 配置文件副本
    └── [相册文件夹]/            # 复制的媒体文件
```

## 🎨 主题定制

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

### 修改交互功能

编辑 `themes/simple/enhancements.js` 文件来自定义：
- 分页逻辑
- 动画效果
- 用户交互
- 动态加载

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
   - 等待GitHub Actions完成构建（通常1-2分钟）
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
5. **提交代码** - 遵循Git提交规范

### 调试技巧

- 使用浏览器开发者工具检查CSS和JavaScript
- 查看控制台错误信息
- 检查网络请求状态
- 验证文件路径和权限
- 使用 `python build_gallery.py` 查看构建日志

## 📊 性能优化

### 构建优化

- **增量构建** - 智能检测文件变化，只处理修改过的文件
- **并行处理** - 多线程复制和生成，显著提升构建速度
- **智能缓存** - 避免重复处理相同文件
- **主题文件检测** - 自动检测主题文件更新并重新构建

### 运行时优化

- **懒加载** - 图片延迟加载，提升首屏加载速度
- **预加载** - 关键资源预加载
- **响应式图片** - 根据设备加载合适尺寸的图片
- **CDN加速** - 支持静态资源CDN分发

### 性能监控

- 使用浏览器开发者工具的Performance面板
- 监控Core Web Vitals指标（LCP、FID、CLS）
- 测试不同网络条件下的加载速度
- 使用Lighthouse进行性能审计

## 🤝 贡献指南

我们欢迎所有形式的贡献！

### 贡献方式

- 🐛 **报告Bug** - 使用 [GitHub Issues](https://github.com/GWen124/Gallery/issues)
- 💡 **功能建议** - 提出新功能想法
- 📝 **文档改进** - 完善文档内容
- 🔧 **代码贡献** - 提交Pull Request

### 开发规范

- 遵循PEP 8 Python代码规范
- 使用有意义的提交信息
- 添加适当的注释和文档
- 测试新功能的兼容性

## ❓ 常见问题

### 1. 如何更改相册显示顺序？

在文件夹名前添加序号，如 `01-相册名`、`02-相册名`。序号会在页面上自动隐藏。

### 2. 序号必须从1开始吗？

不需要。序号可以是任意数字，如 3、10、15，系统会按数值大小正确排序。

### 3. 可以只给部分相册添加序号吗？

可以。有序号的相册会排在前面，无序号的相册按字母顺序排在后面。

### 4. 如何设置相册封面？

在 `config.json` 的 `galleries` 中配置，支持本地路径和远程URL。

### 5. 如何修改版权年份？

在 `config.json` 中设置 `start-date` 或 `start-year`，系统会自动计算年份范围。

### 6. 构建后网页没有更新？

检查以下几点：
- 清除浏览器缓存
- 确认GitHub Actions构建成功
- 等待CDN缓存更新（可能需要几分钟）

### 7. 如何添加自定义字体？

将字体文件放入 `assets/fonts/` 目录，然后在 `config.json` 中配置字体名称。

## 📄 许可证

本项目采用 [MIT许可证](LICENSE) - 查看LICENSE文件了解详情。

## 🙏 致谢

- 感谢所有贡献者的支持和反馈
- 特别感谢 [Thumbsup](https://github.com/thumbsup/thumbsup) 项目的启发
- 感谢开源社区提供的优秀工具和库

## 📞 支持与联系

- **GitHub Issues** - [报告问题](https://github.com/GWen124/Gallery/issues)
- **GitHub Discussions** - [讨论功能](https://github.com/GWen124/Gallery/discussions)
- **个人网站** - [GW124.COM](https://gw124.com/)
- **在线演示** - [https://gallery.gw124.com/](https://gallery.gw124.com/)

---

**Powered by [Wen](https://gw124.com/) • Made with ❤️ for the community**
