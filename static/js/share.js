/**
 * 社交媒体分享功能
 */

// 分享到微信
function shareToWeChat(title, url) {
    // 微信需要使用微信API，这里我们使用一个弹窗展示二维码
    const qrCodeUrl = `https://api.qrserver.com/v1/create-qr-code/?size=200x200&data=${encodeURIComponent(url)}`;
    
    // 创建弹窗
    const modal = document.createElement('div');
    modal.className = 'share-modal';
    modal.innerHTML = `
        <div class="share-modal-content">
            <span class="share-modal-close">&times;</span>
            <h3>分享到微信</h3>
            <p>请使用微信扫描下方二维码</p>
            <div class="qrcode-container">
                <img src="${qrCodeUrl}" alt="二维码" class="qr-code">
            </div>
            <p class="small text-muted mt-2">或复制链接分享给好友</p>
            <div class="copy-link-container">
                <input type="text" readonly value="${url}" class="form-control copy-link-input">
                <button class="btn btn-primary copy-link-btn">复制</button>
            </div>
        </div>
    `;
    
    document.body.appendChild(modal);
    
    // 添加关闭事件
    const closeBtn = modal.querySelector('.share-modal-close');
    closeBtn.addEventListener('click', () => {
        document.body.removeChild(modal);
    });
    
    // 添加点击外部区域关闭
    modal.addEventListener('click', (e) => {
        if (e.target === modal) {
            document.body.removeChild(modal);
        }
    });
    
    // 复制链接
    const copyBtn = modal.querySelector('.copy-link-btn');
    const copyInput = modal.querySelector('.copy-link-input');
    
    copyBtn.addEventListener('click', () => {
        copyInput.select();
        document.execCommand('copy');
        copyBtn.textContent = '已复制';
        setTimeout(() => {
            copyBtn.textContent = '复制';
        }, 2000);
    });
}

// 分享到微博
function shareToWeibo(title, url, imageUrl = '') {
    const weiboUrl = `https://service.weibo.com/share/share.php?url=${encodeURIComponent(url)}&title=${encodeURIComponent(title)}`;
    window.open(weiboUrl, '_blank', 'width=700,height=500');
}

// 分享到QQ
function shareToQQ(title, url, desc = '') {
    const qqUrl = `https://connect.qq.com/widget/shareqq/index.html?url=${encodeURIComponent(url)}&title=${encodeURIComponent(title)}&desc=${encodeURIComponent(desc)}`;
    window.open(qqUrl, '_blank', 'width=700,height=500');
}

// 复制链接
function copyLink(url) {
    // 创建临时输入框
    const tempInput = document.createElement('input');
    tempInput.value = url;
    document.body.appendChild(tempInput);
    
    // 选择内容并复制
    tempInput.select();
    document.execCommand('copy');
    
    // 移除临时输入框
    document.body.removeChild(tempInput);
    
    // 显示提示
    const tooltip = document.createElement('div');
    tooltip.className = 'copy-tooltip';
    tooltip.textContent = '链接已复制！';
    document.body.appendChild(tooltip);
    
    // 2秒后移除提示
    setTimeout(() => {
        document.body.removeChild(tooltip);
    }, 2000);
}

// 初始化分享按钮
function initShareButtons() {
    // 获取当前页面信息
    const pageTitle = document.title;
    const pageUrl = window.location.href;
    
    // 绑定分享按钮事件
    const wechatBtn = document.getElementById('share-wechat');
    const weiboBtn = document.getElementById('share-weibo');
    const qqBtn = document.getElementById('share-qq');
    const linkBtn = document.getElementById('share-link');
    
    if (wechatBtn) {
        wechatBtn.addEventListener('click', (e) => {
            e.preventDefault();
            shareToWeChat(pageTitle, pageUrl);
        });
    }
    
    if (weiboBtn) {
        weiboBtn.addEventListener('click', (e) => {
            e.preventDefault();
            shareToWeibo(pageTitle, pageUrl);
        });
    }
    
    if (qqBtn) {
        qqBtn.addEventListener('click', (e) => {
            e.preventDefault();
            shareToQQ(pageTitle, pageUrl);
        });
    }
    
    if (linkBtn) {
        linkBtn.addEventListener('click', (e) => {
            e.preventDefault();
            copyLink(pageUrl);
        });
    }
}

// 文档加载完成后初始化
document.addEventListener('DOMContentLoaded', initShareButtons); 