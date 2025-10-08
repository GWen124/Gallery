/**
 * Gallery Simple Theme - 增强功能脚本
 * 提供动态配置、页脚增强、默认缩略图等功能
 */

(function() {
    'use strict';
    
    // 等待页面加载完成
    document.addEventListener('DOMContentLoaded', function() {
        initializeEnhancements();
    });
    
    async function initializeEnhancements() {
        try {
            // 应用配置
            await applyConfiguration();
            
            // 初始化分页
            initializePagination();
            
        } catch (error) {
            console.error('Error initializing enhancements:', error);
        }
    }
    
    async function applyConfiguration() {
        let config = {};
        
        try {
            const response = await fetch('./config.json?' + Date.now());
            if (response.ok) {
                config = await response.json();
            }
        } catch (error) {
            console.warn('无法读取 config.json，使用默认配置:', error);
        }
        
        // 应用字体配置
        applyFontConfiguration(config);
        
        // 应用页脚配置
        applyFooterConfiguration(config);
    }
    
    function applyFontConfiguration(config) {
        const root = document.documentElement;
        
        // 标题字体
        let titleFont = '-apple-system, BlinkMacSystemFont, sans-serif';
        if (config['title-font'] && config['title-font'].trim() !== '') {
            if (config['title-font'] === 'brand') {
                titleFont = "'Brand', -apple-system, BlinkMacSystemFont, sans-serif";
            } else {
                titleFont = config['title-font'];
            }
        }
        
        // 页脚字体
        let footerFont = '-apple-system, BlinkMacSystemFont, sans-serif';
        if (config['footer-font'] && config['footer-font'].trim() !== '') {
            if (config['footer-font'] === 'brand') {
                footerFont = "'Brand', -apple-system, BlinkMacSystemFont, sans-serif";
            } else {
                footerFont = config['footer-font'];
            }
        }
        
        // 全局字体
        let globalFont = '-apple-system, BlinkMacSystemFont, sans-serif';
        if (config['global-font'] && config['global-font'].trim() !== '') {
            if (config['global-font'] === 'brand') {
                globalFont = "'Brand', -apple-system, BlinkMacSystemFont, sans-serif";
            } else {
                globalFont = config['global-font'];
            }
        }
        
        // 设置 CSS 变量
        root.style.setProperty('--title-font', titleFont);
        root.style.setProperty('--footer-font', footerFont);
        root.style.setProperty('--global-font', globalFont);
        
    }
    
    function applyFooterConfiguration(config) {
        const footer = document.querySelector('.footer');
        if (!footer) return;
        
        const footerP = footer.querySelector('p');
        if (!footerP) return;
        
        // 获取配置值
        const siteName = config.footer || 'GALLERY.GW124.TOP';
        const siteLink = config['footer-link'] || 'https://gw124.top';
        
        // 创建新的页脚内容
        footerP.innerHTML = `© 2025 <a href="${siteLink}" target="_blank">${siteName}</a> • Powered By <a href="https://gw124.top/" target="_blank">Wen</a>`;
        
    }
    
    function initializePagination() {
        const albums = document.querySelectorAll('.album');
        if (albums.length === 0) return;
        
        const itemsPerPage = 9;
        const totalItems = albums.length;
        const totalPages = Math.ceil(totalItems / itemsPerPage);
        
        if (totalPages <= 1) {
            // 如果只有一页，隐藏分页控件
            const paginationContainer = document.querySelector('.pagination-container');
            if (paginationContainer) {
                paginationContainer.style.display = 'none';
            }
            return;
        }
        
        // 为每个相册添加页码属性
        albums.forEach((album, index) => {
            const page = Math.floor(index / itemsPerPage) + 1;
            album.setAttribute('data-page', page);
        });
        
        // 初始化分页控件
        const pagination = new Pagination(totalItems, itemsPerPage);
        pagination.init();
    }
    
    // 分页类
    class Pagination {
        constructor(totalItems, itemsPerPage) {
            this.totalItems = totalItems;
            this.itemsPerPage = itemsPerPage;
            this.totalPages = Math.ceil(totalItems / itemsPerPage);
            this.currentPage = 1;
            this.albums = document.querySelectorAll('.album');
        }
        
        init() {
            this.generatePaginationNumbers();
            this.setupEventListeners();
            this.updatePagination();
            this.showPage(1);
        }
        
        generatePaginationNumbers() {
            const paginationNumbers = document.getElementById('pagination-numbers');
            if (!paginationNumbers) return;
            
            // 清空现有页码
            paginationNumbers.innerHTML = '';
            
            // 生成页码按钮
            for (let i = 1; i <= this.totalPages; i++) {
                const numberBtn = document.createElement('button');
                numberBtn.className = 'pagination-number';
                numberBtn.dataset.page = i;
                numberBtn.textContent = i;
                paginationNumbers.appendChild(numberBtn);
            }
        }
        
        setupEventListeners() {
            // 上一页按钮
            const prevBtn = document.getElementById('prev-btn');
            if (prevBtn) {
                prevBtn.addEventListener('click', () => {
                    if (this.currentPage > 1) {
                        this.showPage(this.currentPage - 1);
                    }
                });
            }
            
            // 下一页按钮
            const nextBtn = document.getElementById('next-btn');
            if (nextBtn) {
                nextBtn.addEventListener('click', () => {
                    if (this.currentPage < this.totalPages) {
                        this.showPage(this.currentPage + 1);
                    }
                });
            }
            
            // 页码按钮
            document.querySelectorAll('.pagination-number').forEach(btn => {
                btn.addEventListener('click', () => {
                    const page = parseInt(btn.dataset.page);
                    this.showPage(page);
                });
            });
        }
        
        showPage(page) {
            this.currentPage = page;
            
            // 隐藏所有相册
            this.albums.forEach(album => {
                album.style.display = 'none';
            });
            
            // 显示当前页的相册
            const startIndex = (page - 1) * this.itemsPerPage;
            const endIndex = Math.min(startIndex + this.itemsPerPage, this.totalItems);
            
            for (let i = startIndex; i < endIndex; i++) {
                if (this.albums[i]) {
                    this.albums[i].style.display = 'block';
                }
            }
            
            this.updatePagination();
        }
        
        updatePagination() {
            // 更新分页信息
            const startItem = (this.currentPage - 1) * this.itemsPerPage + 1;
            const endItem = Math.min(this.currentPage * this.itemsPerPage, this.totalItems);
            const paginationInfo = document.getElementById('pagination-info');
            if (paginationInfo) {
                paginationInfo.textContent = `显示 ${startItem}-${endItem} 项，共 ${this.totalItems} 项`;
            }
            
            // 更新按钮状态
            const prevBtn = document.getElementById('prev-btn');
            const nextBtn = document.getElementById('next-btn');
            
            if (prevBtn) {
                prevBtn.disabled = this.currentPage === 1;
            }
            if (nextBtn) {
                nextBtn.disabled = this.currentPage === this.totalPages;
            }
            
            // 更新页码按钮状态
            document.querySelectorAll('.pagination-number').forEach(btn => {
                btn.classList.remove('active');
                if (parseInt(btn.dataset.page) === this.currentPage) {
                    btn.classList.add('active');
                }
            });
        }
    }
    
    // 如果页面已经加载完成，立即执行
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initializeEnhancements);
    } else {
        initializeEnhancements();
    }
    
})();
