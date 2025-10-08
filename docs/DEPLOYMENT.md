# 🚀 部署指南

本指南将帮助您将Gallery项目部署到各种静态托管平台。

## 📋 部署前准备

### 1. 确保项目配置正确

检查 `config.json` 文件：

```json
{
  "input": "./gallery",
  "output": "./build_output",
  "title": "您的画廊标题",
  "footer": "您的网站名称",
  "footer-link": "https://您的网站.com",
  "title-font": "brand",
  "footer-font": "brand",
  "global-font": "brand"
}
```

### 2. 本地测试

```bash
# 构建项目
python build_gallery.py

# 本地预览
cd build_output
python -m http.server 8000
```

访问 `http://localhost:8000` 确认一切正常。

## 🌐 GitHub Pages 部署

### 自动部署（推荐）

1. **Fork 仓库**
   - 访问 [Gallery仓库](https://github.com/GWen124/Gallery)
   - 点击 "Fork" 按钮

2. **启用 GitHub Pages**
   - 进入您的仓库设置
   - 找到 "Pages" 部分
   - 选择 "GitHub Actions" 作为源

3. **推送代码**
   ```bash
   git clone https://github.com/您的用户名/Gallery.git
   cd Gallery
   
   # 添加您的媒体文件到 gallery/ 目录
   # 修改 config.json 配置
   
   git add .
   git commit -m "初始化画廊"
   git push origin main
   ```

4. **查看部署状态**
   - 进入仓库的 "Actions" 标签页
   - 查看部署进度
   - 部署完成后，访问 `https://您的用户名.github.io/Gallery`

### 手动部署

如果自动部署失败，可以手动部署：

```bash
# 构建项目
python build_gallery.py

# 将 build_output/ 目录内容推送到 gh-pages 分支
git subtree push --prefix build_output origin gh-pages
```

## 🔧 其他静态托管平台

### Netlify

1. **连接仓库**
   - 登录 [Netlify](https://netlify.com)
   - 选择 "New site from Git"
   - 连接您的GitHub仓库

2. **配置构建设置**
   ```
   Build command: python build_gallery.py
   Publish directory: build_output
   Python version: 3.9
   ```

3. **添加构建钩子**
   - 在仓库设置中添加 `requirements.txt`
   - 确保Python环境正确

### Vercel

1. **安装 Vercel CLI**
   ```bash
   npm i -g vercel
   ```

2. **创建 vercel.json**
   ```json
   {
     "builds": [
       {
         "src": "build_gallery.py",
         "use": "@vercel/python"
       }
     ],
     "routes": [
       {
         "src": "/(.*)",
         "dest": "/build_output/$1"
       }
     ]
   }
   ```

3. **部署**
   ```bash
   vercel --prod
   ```

### Cloudflare Pages

1. **连接仓库**
   - 登录 [Cloudflare Pages](https://pages.cloudflare.com)
   - 选择 "Connect to Git"
   - 连接您的仓库

2. **配置构建设置**
   ```
   Build command: python build_gallery.py
   Build output directory: build_output
   Python version: 3.9
   ```

## 🔍 故障排除

### 常见问题

1. **构建失败**
   - 检查Python版本（需要3.7+）
   - 确认所有依赖已安装
   - 查看错误日志

2. **媒体文件不显示**
   - 检查文件路径是否正确
   - 确认文件格式受支持
   - 检查文件大小限制

3. **样式不生效**
   - 清除浏览器缓存
   - 检查CSS文件路径
   - 确认字体文件存在

4. **GitHub Actions 失败**
   - 检查仓库权限设置
   - 确认GitHub Pages已启用
   - 查看Actions日志

### 调试技巧

1. **本地调试**
   ```bash
   # 详细输出
   python build_gallery.py
   
   # 检查生成的文件
   ls -la build_output/
   ```

2. **检查配置**
   ```bash
   # 验证JSON格式
   python -m json.tool config.json
   ```

3. **测试媒体文件**
   ```bash
   # 检查文件类型
   file gallery/*/*
   ```

## 📊 性能优化

### 图片优化

1. **压缩图片**
   - 使用工具如 [TinyPNG](https://tinypng.com) 压缩图片
   - 考虑使用WebP格式

2. **响应式图片**
   - 为不同设备提供不同尺寸的图片
   - 使用适当的图片尺寸

### 加载优化

1. **懒加载**
   - 图片懒加载已内置
   - 视频按需加载

2. **缓存策略**
   - 设置适当的HTTP缓存头
   - 使用CDN加速

## 🔒 安全考虑

1. **文件上传**
   - 限制文件类型和大小
   - 扫描恶意文件

2. **访问控制**
   - 考虑添加访问密码
   - 限制敏感内容

3. **HTTPS**
   - 确保使用HTTPS
   - 配置安全头

## 📈 监控和分析

1. **访问统计**
   - 集成Google Analytics
   - 使用GitHub Pages统计

2. **性能监控**
   - 使用PageSpeed Insights
   - 监控Core Web Vitals

3. **错误监控**
   - 设置错误日志
   - 监控构建状态

---

**需要帮助？** 请查看 [Issues](https://github.com/GWen124/Gallery/issues) 或提交新的问题。