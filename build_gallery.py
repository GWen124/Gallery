#!/usr/bin/env python3
"""
自定义图片画廊生成器
替代Thumbsup，提供完全自定义的静态网站生成
"""

import json
import shutil
import re
from pathlib import Path
from datetime import datetime
import urllib.parse
import hashlib
import base64
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

class GalleryBuilder:
    def __init__(self, config_path="config.json"):
        with open(config_path, 'r', encoding='utf-8') as f:
            self.config = json.load(f)
        
        self.input_dir = Path(self.config['input'])
        self.output_dir = Path(self.config['output'])
        self.title = self.config.get('title', 'Image Gallery')
        self.footer = self.config.get('footer', 'Gallery')
        self.footer_link = self.config.get('footer-link', '#')
        
        # 字体配置
        self.title_font = self.config.get('title-font', '')
        self.footer_font = self.config.get('footer-font', '')
        self.global_font = self.config.get('global-font', '')
        
        # 版权年份配置
        self.start_year = self.config.get('start-year', None)
        self.start_date = self.config.get('start-date', None)
    
    def get_copyright_year(self):
        """生成版权年份字符串"""
        current_year = datetime.now().year
        
        # 优先使用start-date，如果没有则使用start-year
        start_year = None
        
        if self.start_date:
            try:
                # 解析日期字符串，支持多种格式
                if isinstance(self.start_date, str):
                    # 尝试解析 YYYY-MM-DD 格式
                    if '-' in self.start_date:
                        parsed_date = datetime.strptime(self.start_date, '%Y-%m-%d')
                        start_year = parsed_date.year
                    # 尝试解析 YYYY/MM/DD 格式
                    elif '/' in self.start_date:
                        parsed_date = datetime.strptime(self.start_date, '%Y/%m/%d')
                        start_year = parsed_date.year
                    # 尝试解析 YYYY.MM.DD 格式
                    elif '.' in self.start_date:
                        parsed_date = datetime.strptime(self.start_date, '%Y.%m.%d')
                        start_year = parsed_date.year
                    else:
                        # 如果只是年份字符串
                        start_year = int(self.start_date)
                else:
                    start_year = int(self.start_date)
            except (ValueError, TypeError):
                print(f"⚠️  警告: 无法解析start-date '{self.start_date}'，将忽略此配置")
                start_year = None
        
        # 如果没有start_date，使用start_year
        if start_year is None and self.start_year is not None:
            start_year = self.start_year
        
        # 生成版权年份字符串
        if start_year is None:
            # 如果没有设置开始年份，只显示当前年份
            return str(current_year)
        
        # 验证年份范围的合理性
        if start_year > current_year:
            print(f"⚠️  警告: 开始年份 {start_year} 大于当前年份 {current_year}，将使用当前年份")
            return str(current_year)
        
        # 如果设置了开始年份
        if start_year == current_year:
            # 如果开始年份等于当前年份，只显示当前年份
            return str(current_year)
        else:
            # 否则显示年份范围
            return f"{start_year}-{current_year}"
        
    def get_media_type(self, file_path):
        """判断媒体类型"""
        ext = file_path.suffix.lower()
        video_extensions = {'.mp4', '.avi', '.mov', '.wmv', '.flv', '.webm', '.mkv', '.m4v'}
        image_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp', '.tiff', '.svg'}
        
        if ext in video_extensions:
            return 'video'
        elif ext in image_extensions:
            return 'image'
        return 'unknown'
    
    
    def parse_album_name(self, folder_name):
        """
        解析相册文件夹名称，提取序号和显示名称
        支持格式：
        - "01-相册名" -> (1, "相册名", "01-相册名")
        - "001_相册名" -> (1, "相册名", "001_相册名")
        - "相册名" -> (None, "相册名", "相册名")
        """
        # 尝试匹配开头的序号模式：数字 + 分隔符（-、_、空格、.）
        match = re.match(r'^(\d+)[-_\.\s]+(.+)$', folder_name)
        
        if match:
            order = int(match.group(1))
            display_name = match.group(2)
            return (order, display_name, folder_name)
        else:
            # 没有序号，使用原名称
            return (None, folder_name, folder_name)
    
    def scan_gallery(self):
        """扫描画廊目录，获取所有相册和媒体文件"""
        albums = []
        
        # 获取封面配置
        galleries_config = self.config.get('galleries', {})
        
        for item in self.input_dir.iterdir():
            if item.is_dir():
                # 解析文件夹名称，提取序号和显示名称
                order, display_name, folder_name = self.parse_album_name(item.name)
                
                album = {
                    'name': item.name,  # 原始文件夹名（用于文件路径）
                    'display_name': display_name,  # 显示名称（隐藏序号）
                    'order': order,  # 排序序号
                    'path': item,
                    'media': [],
                    'thumbnail': None,
                    'cover': None,
                    'count': 0
                }
                
                # 检查是否有配置的封面
                album_config = galleries_config.get(item.name, {})
                cover_path = album_config.get('cover', '')
                
                if cover_path:
                    # 处理封面路径
                    if cover_path.startswith('http'):
                        # 完整URL
                        album['cover'] = cover_path
                    elif cover_path.startswith('/'):
                        # 相对路径，去掉开头的斜杠
                        album['cover'] = cover_path[1:]
                    else:
                        # 相对路径
                        album['cover'] = cover_path
                
                # 扫描相册内的媒体文件
                media_files = list(item.iterdir())
                media_files.sort(key=lambda x: x.name)  # 按文件名排序确保顺序一致
                for media_file in media_files:
                    if media_file.is_file():
                        media_type = self.get_media_type(media_file)
                        if media_type in ['image', 'video']:
                            media_info = {
                                'name': media_file.name,
                                'path': media_file,
                                'type': media_type,
                                'size': media_file.stat().st_size,
                                'modified': datetime.fromtimestamp(media_file.stat().st_mtime)
                            }
                            
                            album['media'].append(media_info)
                            
                            # 设置相册缩略图（第一个文件）
                            if not album['thumbnail']:
                                album['thumbnail'] = media_info
                
                album['count'] = len(album['media'])
                if album['count'] > 0:
                    albums.append(album)
        
        # 排序：有序号的按序号排序，没有序号的按名称排序，有序号的排在前面
        albums.sort(key=lambda x: (x['order'] is None, x['order'] if x['order'] is not None else 0, x['display_name']))
        return albums
    
    def copy_media_files(self, albums):
        """并行复制媒体文件到输出目录"""
        def copy_single_media(media_info):
            album_name, media = media_info
            album_dir = self.output_dir / album_name
            album_dir.mkdir(parents=True, exist_ok=True)
            
            dest_path = album_dir / media['name']
            
            # 检查文件是否需要复制（避免重复复制）
            if dest_path.exists() and dest_path.stat().st_size == media['size']:
                # 文件已存在且大小相同，跳过复制
                # URL编码文件名以处理特殊字符（如#）
                encoded_name = urllib.parse.quote(media['name'], safe='')
                media['url'] = f'{album_name}/{encoded_name}'
                return f"跳过: {media['name']}"
            
            # 复制文件
            shutil.copy2(media['path'], dest_path)
            # URL编码文件名以处理特殊字符（如#）
            encoded_name = urllib.parse.quote(media['name'], safe='')
            media['url'] = f'{album_name}/{encoded_name}'
            return f"复制: {media['name']}"
        
        # 准备所有复制任务
        copy_tasks = []
        for album in albums:
            for media in album['media']:
                copy_tasks.append((album['name'], media))
        
        # 并行执行复制任务
        print(f"📋 开始并行复制 {len(copy_tasks)} 个媒体文件...")
        start_time = time.time()
        
        with ThreadPoolExecutor(max_workers=min(8, len(copy_tasks))) as executor:
            futures = [executor.submit(copy_single_media, task) for task in copy_tasks]
            
            completed = 0
            for future in as_completed(futures):
                try:
                    result = future.result()
                    completed += 1
                    if completed % 10 == 0 or completed == len(copy_tasks):
                        print(f"   进度: {completed}/{len(copy_tasks)}")
                except Exception as e:
                    print(f"   错误: {e}")
        
        elapsed = time.time() - start_time
        print(f"✅ 媒体文件复制完成，耗时: {elapsed:.2f}秒")
    
    def generate_index_html(self, albums):
        """生成首页HTML"""
        html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{self.title}</title>
    <link rel="stylesheet" href="style.css">
    <link rel="icon" type="image/x-icon" href="favicon.ico">
    <meta name="description" content="图片画廊 - {self.title}">
    <meta name="robots" content="index, follow">
    <link rel="preload" href="style.css" as="style">
    <link rel="preload" href="enhancements.js" as="script">
</head>
<body>
    <div class="header">
        <h1>{self.title}</h1>
    </div>

    <div class="main">
        <div class="breadcrumb">
            <a href="index.html">首页</a> / <span>所有相册</span>
        </div>

        <div class="albums" id="albums-container">
"""
        
        for album in albums:
            # 确定缩略图URL
            thumbnail_url = None
            
            # 优先使用配置的封面
            if album.get('cover'):
                thumbnail_url = album['cover']
            elif album['thumbnail']:
                # 如果相册的第一个文件是视频，使用SVG占位符
                if album['thumbnail']['type'] == 'video':
                    svg_content = '''<svg width="400" height="300" viewBox="0 0 400 300" fill="none" xmlns="http://www.w3.org/2000/svg">
<rect width="400" height="300" fill="#f0f0f0"/>
<circle cx="200" cy="150" r="30" fill="#333"/>
<path d="M185 135L215 150L185 165V135Z" fill="white"/>
<text x="200" y="200" text-anchor="middle" fill="#666" font-family="Arial" font-size="16">视频文件</text>
</svg>'''
                    svg_base64 = base64.b64encode(svg_content.encode('utf-8')).decode('utf-8')
                    thumbnail_url = f'data:image/svg+xml;base64,{svg_base64}'
                else:
                    thumbnail_url = album['thumbnail']['url']
            
            # 确定媒体类型显示
            media_types = set(media['type'] for media in album['media'])
            if 'video' in media_types and 'image' in media_types:
                type_text = f"{album['count']} 个文件"
            elif 'video' in media_types:
                type_text = f"{album['count']} 个视频"
            else:
                type_text = f"{album['count']} 张图片"
            
            # 生成安全的相册页面链接（用下划线替换空格）
            safe_album_name = album['name'].replace(' ', '_')
            
            html += f"""
            <div class="album" data-page="1">
                <a href="album_{safe_album_name}.html">
                    <div class="album-thumbnail">
"""
            
            if thumbnail_url:
                html += f'                        <img src="{thumbnail_url}" alt="{album["display_name"]}" loading="lazy" decoding="async">'
            else:
                html += '                        <div class="no-thumbnail">无预览图</div>'
            
            html += f"""
                    </div>
                    <div class="album-info">
                        <h3 class="album-title">{album['display_name']}</h3>
                        <p class="album-count">{type_text}</p>
                    </div>
                </a>
            </div>
"""
        
        html += """
        </div>
        
        <!-- 分页控件 -->
        <div class="pagination-container">
            <div class="pagination-info">
                <span id="pagination-info">显示 1-9 项，共 10 项</span>
            </div>
            <div class="pagination">
                <button class="pagination-btn prev-btn" id="prev-btn" disabled>
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <polyline points="15,18 9,12 15,6"></polyline>
                    </svg>
                    上一页
                </button>
                <div class="pagination-numbers" id="pagination-numbers">
                </div>
                <button class="pagination-btn next-btn" id="next-btn">
                    下一页
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <polyline points="9,18 15,12 9,6"></polyline>
                    </svg>
                </button>
            </div>
        </div>
    </div>

    <div class="footer">
        <p>© {self.get_copyright_year()} <a href="{self.footer_link}" target="_blank">{self.footer}</a> • Powered By <a href="https://gw124.top/" target="_blank">Wen</a></p>
    </div>

    <script src="enhancements.js"></script>
</body>
</html>"""
        
        return html
    
    def generate_album_html(self, album):
        """生成相册页面HTML"""
        html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{album['display_name']} - {self.title}</title>
    <link rel="stylesheet" href="style.css">
    <link rel="icon" type="image/x-icon" href="favicon.ico">
    <meta name="description" content="相册 - {album['display_name']}">
    <meta name="robots" content="index, follow">
    <link rel="preload" href="style.css" as="style">
    <link rel="preload" href="enhancements.js" as="script">
</head>
<body>
    <div class="header">
        <h1>{self.title}</h1>
    </div>

    <div class="main">
        <div class="breadcrumb">
            <a href="index.html">首页</a> / <span>{album['display_name']}</span>
        </div>

        <div class="album-header">
            <h2>{album['display_name']}</h2>
        </div>

        <div class="albums" id="media-container">
"""
        
        for i, media in enumerate(album['media']):
            # 确定缩略图URL
            if media['type'] == 'video':
                # 视频文件使用占位符，不显示实际视频
                svg_content = '''<svg width="400" height="300" viewBox="0 0 400 300" fill="none" xmlns="http://www.w3.org/2000/svg">
<rect width="400" height="300" fill="#f0f0f0"/>
<circle cx="200" cy="150" r="30" fill="#333"/>
<path d="M185 135L215 150L185 165V135Z" fill="white"/>
<text x="200" y="200" text-anchor="middle" fill="#666" font-family="Arial" font-size="16">视频文件</text>
</svg>'''
                svg_base64 = base64.b64encode(svg_content.encode('utf-8')).decode('utf-8')
                thumbnail_url = f'data:image/svg+xml;base64,{svg_base64}'
            else:
                thumbnail_url = media['url']
            
            # 生成安全的媒体页面链接（使用索引和哈希）
            media_hash = hashlib.md5(media['name'].encode('utf-8')).hexdigest()[:8]
            media_link = f"media_{album['name']}_{i}_{media_hash}.html"
            
            html += f"""
            <div class="album" data-page="1">
                <a href="{media_link}">
                    <div class="album-thumbnail">
                        <img src="{thumbnail_url}" alt="{media['name']}" loading="lazy" decoding="async">
                    </div>
                    <div class="album-info">
                        <h3 class="album-title">{media['name']}</h3>
                        <p class="album-count">{media['modified'].strftime('%Y-%m-%d')}</p>
                    </div>
                </a>
            </div>
"""
        
        html += """
        </div>
        
        <!-- 分页控件 -->
        <div class="pagination-container">
            <div class="pagination-info">
                <span id="pagination-info">显示 1-9 项，共 10 项</span>
            </div>
            <div class="pagination">
                <button class="pagination-btn prev-btn" id="prev-btn" disabled>
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <polyline points="15,18 9,12 15,6"></polyline>
                    </svg>
                    上一页
                </button>
                <div class="pagination-numbers" id="pagination-numbers">
                </div>
                <button class="pagination-btn next-btn" id="next-btn">
                    下一页
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <polyline points="9,18 15,12 9,6"></polyline>
                    </svg>
                </button>
            </div>
        </div>
    </div>

    <div class="footer">
        <p>© {self.get_copyright_year()} <a href="{self.footer_link}" target="_blank">{self.footer}</a> • Powered By <a href="https://gw124.top/" target="_blank">Wen</a></p>
    </div>

    <script src="enhancements.js"></script>
</body>
</html>"""
        
        return html
    
    def generate_media_html(self, album, media):
        """生成媒体查看页面HTML"""
        html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{media['name']} - {album['display_name']} - {self.title}</title>
    <link rel="stylesheet" href="style.css">
    <link rel="icon" type="image/x-icon" href="favicon.ico">
    <meta name="description" content="媒体文件 - {media['name']}">
    <meta name="robots" content="index, follow">
    <link rel="preload" href="style.css" as="style">
    <link rel="preload" href="enhancements.js" as="script">
</head>
<body>
    <div class="header">
        <h1>{self.title}</h1>
    </div>

    <div class="main">
        <div class="breadcrumb">
            <a href="index.html">首页</a> / <a href="album_{album['name'].replace(' ', '_')}.html">{album['display_name']}</a> / <span>{media['name']}</span>
        </div>

        <div class="media-viewer">
            <div class="media-content">
"""
        
        if media['type'] == 'video':
            # 视频路径已经在上面的copy_media_files中编码过了，直接使用
            encoded_url = media['url']
            # 根据文件扩展名确定MIME类型
            ext = media['path'].suffix.lower()
            if ext == '.mp4':
                mime_type = 'video/mp4'
            elif ext == '.webm':
                mime_type = 'video/webm'
            elif ext == '.ogg':
                mime_type = 'video/ogg'
            elif ext == '.avi':
                mime_type = 'video/x-msvideo'
            elif ext == '.mov':
                mime_type = 'video/quicktime'
            else:
                mime_type = 'video/mp4'  # 默认
            
            html += f"""
                <video controls preload="metadata" style="width: 100%; max-width: 800px; height: auto;" onerror="console.error('视频加载失败:', this.error); this.style.display='none'; this.nextElementSibling.style.display='block';">
                    <source src="{encoded_url}" type="{mime_type}">
                    您的浏览器不支持视频播放。
                </video>
                <div style="display: none; padding: 20px; text-align: center; background: #f5f5f5; border-radius: 8px;">
                    <p>视频加载失败</p>
                    <p>文件路径: {media['url']}</p>
                    <p>编码路径: {encoded_url}</p>
                    <p>MIME类型: {mime_type}</p>
                    <a href="{encoded_url}" download>点击下载视频文件</a>
                </div>
"""
        else:
            html += f'                <img src="{media["url"]}" alt="{media["name"]}" loading="eager" decoding="sync">'
        
        html += f"""
            </div>
            
            <div class="media-details">
                <h2>{media['name']}</h2>
                <p class="media-date">{media['modified'].strftime('%Y-%m-%d %H:%M')}</p>
                <p class="media-size">文件大小: {media['size'] // 1024} KB</p>
                
                <div class="media-actions">
                    <button id="copy-url-btn" class="copy-btn" onclick="copyMediaUrl()">
                        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                            <rect x="9" y="9" width="13" height="13" rx="2" ry="2"></rect>
                            <path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"></path>
                        </svg>
                        复制链接
                    </button>
                    <span id="copy-status" class="copy-status"></span>
                </div>
            </div>
        </div>
    </div>

    <div class="footer">
        <p>© {self.get_copyright_year()} <a href="{self.footer_link}" target="_blank">{self.footer}</a> • Powered By <a href="https://gw124.top/" target="_blank">Wen</a></p>
    </div>

    <script>
        // 媒体URL数据
        const mediaUrl = "{media['url']}";
        const mediaType = "{media['type']}";
        
        // 复制媒体URL函数
        function copyMediaUrl() {{
            const fullUrl = window.location.origin + '/' + mediaUrl;
            
            if (navigator.clipboard && window.isSecureContext) {{
                // 使用现代 Clipboard API
                navigator.clipboard.writeText(fullUrl).then(function() {{
                    showCopyStatus('✅ 链接已复制到剪贴板！', 'success');
                }}).catch(function(err) {{
                    console.error('复制失败:', err);
                    fallbackCopy(fullUrl);
                }});
            }} else {{
                // 回退方案
                fallbackCopy(fullUrl);
            }}
        }}
        
        // 回退复制方案
        function fallbackCopy(text) {{
            const textArea = document.createElement('textarea');
            textArea.value = text;
            textArea.style.position = 'fixed';
            textArea.style.left = '-999999px';
            textArea.style.top = '-999999px';
            document.body.appendChild(textArea);
            textArea.focus();
            textArea.select();
            
            try {{
                const successful = document.execCommand('copy');
                if (successful) {{
                    showCopyStatus('✅ 链接已复制到剪贴板！', 'success');
                }} else {{
                    showCopyStatus('❌ 复制失败，请手动复制', 'error');
                }}
            }} catch (err) {{
                console.error('复制失败:', err);
                showCopyStatus('❌ 复制失败，请手动复制', 'error');
            }}
            
            document.body.removeChild(textArea);
        }}
        
        // 显示复制状态
        function showCopyStatus(message, type) {{
            const statusElement = document.getElementById('copy-status');
            statusElement.textContent = message;
            statusElement.className = `copy-status ${{type}}`;
            
            // 3秒后清除状态
            setTimeout(() => {{
                statusElement.textContent = '';
                statusElement.className = 'copy-status';
            }}, 3000);
        }}
    </script>
    
    <script src="enhancements.js"></script>
</body>
</html>"""
        
        return html
    
    def copy_theme_files(self):
        """复制主题文件到输出目录"""
        # 复制CSS文件
        css_src = Path('themes/simple/style.css')
        if css_src.exists():
            shutil.copy2(css_src, self.output_dir / 'style.css')
        
        # 复制JS文件
        js_src = Path('themes/simple/enhancements.js')
        if js_src.exists():
            shutil.copy2(js_src, self.output_dir / 'enhancements.js')
        
        # 复制字体文件
        fonts_src = Path('assets/fonts')
        if fonts_src.exists():
            fonts_dest = self.output_dir / 'assets' / 'fonts'
            fonts_dest.mkdir(parents=True, exist_ok=True)
            for font_file in fonts_src.iterdir():
                if font_file.is_file():
                    shutil.copy2(font_file, fonts_dest / font_file.name)
        
        # 复制配置文件
        config_src = Path('config.json')
        if config_src.exists():
            shutil.copy2(config_src, self.output_dir / 'config.json')
    
    def should_rebuild(self):
        """检查是否需要重新构建"""
        if not self.output_dir.exists():
            return True
        
        # 检查配置文件是否更新
        config_mtime = Path('config.json').stat().st_mtime
        build_mtime = (self.output_dir / 'config.json').stat().st_mtime if (self.output_dir / 'config.json').exists() else 0
        
        if config_mtime > build_mtime:
            return True
        
        # 检查主题文件是否更新
        theme_files = [
            ('themes/simple/style.css', 'style.css'),
            ('themes/simple/enhancements.js', 'enhancements.js'),
            ('build_gallery.py', None)  # 检查构建脚本本身
        ]
        
        for src_path, dest_name in theme_files:
            src = Path(src_path)
            if src.exists():
                if dest_name:
                    dest = self.output_dir / dest_name
                    if not dest.exists() or dest.stat().st_mtime < src.stat().st_mtime:
                        return True
                else:
                    # 对于build_gallery.py，只要它更新了就重新构建
                    if build_mtime < src.stat().st_mtime:
                        return True
        
        # 检查输入目录是否有新文件
        for item in self.input_dir.rglob('*'):
            if item.is_file():
                input_mtime = item.stat().st_mtime
                relative_path = item.relative_to(self.input_dir)
                output_path = self.output_dir / relative_path
                
                if not output_path.exists() or output_path.stat().st_mtime < input_mtime:
                    return True
        
        return False

    def build(self):
        """构建完整的画廊网站"""
        try:
            print("🚀 开始构建画廊...")
            
            # 验证输入目录
            if not self.input_dir.exists():
                raise FileNotFoundError(f"输入目录不存在: {self.input_dir}")
            
            # 检查是否需要重新构建
            if not self.should_rebuild():
                print("✅ 检测到无需重新构建，跳过构建过程")
                return
            
            # 清理输出目录
            if self.output_dir.exists():
                shutil.rmtree(self.output_dir)
            self.output_dir.mkdir(parents=True, exist_ok=True)
            
            # 扫描画廊
            print("📁 扫描画廊目录...")
            albums = self.scan_gallery()
            if not albums:
                print("⚠️  警告: 未找到任何相册")
                return
            print(f"✅ 找到 {len(albums)} 个相册")
            
            # 复制媒体文件
            print("📋 复制媒体文件...")
            self.copy_media_files(albums)
            
            # 生成HTML页面
            print("🌐 生成HTML页面...")
            start_time = time.time()
            
            # 生成首页
            index_html = self.generate_index_html(albums)
            with open(self.output_dir / 'index.html', 'w', encoding='utf-8') as f:
                f.write(index_html)
            print("  ✅ 首页生成完成")
            
            # 并行生成相册和媒体页面
            def generate_album_pages(album):
                """生成单个相册的所有页面"""
                album_html = self.generate_album_html(album)
                safe_album_name = album["name"].replace(' ', '_')
                
                # 写入相册页面
                with open(self.output_dir / f'album_{safe_album_name}.html', 'w', encoding='utf-8') as f:
                    f.write(album_html)
                
                # 生成媒体页面
                media_pages = []
                for i, media in enumerate(album['media']):
                    media_html = self.generate_media_html(album, media)
                    media_hash = hashlib.md5(media['name'].encode('utf-8')).hexdigest()[:8]
                    filename = f'media_{album["name"]}_{i}_{media_hash}.html'
                    
                    with open(self.output_dir / filename, 'w', encoding='utf-8') as f:
                        f.write(media_html)
                    media_pages.append(filename)
                
                return f"相册 {album['name']}: 1个相册页面 + {len(media_pages)}个媒体页面"
            
            # 并行生成所有相册页面
            with ThreadPoolExecutor(max_workers=min(4, len(albums))) as executor:
                futures = [executor.submit(generate_album_pages, album) for album in albums]
                
                completed = 0
                for future in as_completed(futures):
                    try:
                        result = future.result()
                        completed += 1
                        print(f"  ✅ {result}")
                    except Exception as e:
                        print(f"  ❌ 生成页面时出错: {e}")
            
            elapsed = time.time() - start_time
            print(f"✅ HTML页面生成完成，耗时: {elapsed:.2f}秒")
            
            # 复制主题文件
            print("🎨 复制主题文件...")
            self.copy_theme_files()
            
            total_media = sum(len(album['media']) for album in albums)
            print(f"🎉 构建完成！")
            print(f"📊 统计: {len(albums)} 个相册, {total_media} 个媒体文件")
            print(f"📂 输出目录: {self.output_dir}")
            
        except Exception as e:
            print(f"❌ 构建失败: {e}")
            raise

if __name__ == "__main__":
    builder = GalleryBuilder()
    builder.build()
