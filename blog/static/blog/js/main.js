// 评论框焦点效果
document.addEventListener('DOMContentLoaded', function() {
    // 评论表单显示/隐藏逻辑
    const showCommentFormBtn = document.getElementById('show-comment-form-btn');
    const commentForm = document.getElementById('comment-form');
    const commentButtonContainer = document.getElementById('comment-button-container');
    const cancelCommentBtn = document.getElementById('cancel-comment-btn');
    
    if (showCommentFormBtn && commentForm) {
        showCommentFormBtn.addEventListener('click', function() {
            // 显示评论表单
            commentForm.classList.remove('d-none');
            // 隐藏按钮
            commentButtonContainer.classList.add('d-none');
            // 聚焦到评论输入框
            const textarea = commentForm.querySelector('textarea');
            if (textarea) {
                textarea.focus();
            }
        });
        
        // 取消按钮点击事件
        if (cancelCommentBtn) {
            cancelCommentBtn.addEventListener('click', function() {
                // 清空输入框
                const textarea = commentForm.querySelector('textarea');
                if (textarea) {
                    textarea.value = '';
                }
                // 隐藏评论表单
                commentForm.classList.add('d-none');
                // 显示按钮
                commentButtonContainer.classList.remove('d-none');
            });
        }
    }
    
    // 评论文本框焦点效果
    const commentTextareas = document.querySelectorAll('.comment-input-container textarea');
    
    commentTextareas.forEach(textarea => {
        textarea.addEventListener('focus', function() {
            this.parentElement.classList.add('focused');
        });
        
        textarea.addEventListener('blur', function() {
            if (this.value.trim() === '') {
                this.parentElement.classList.remove('focused');
            }
        });
        
        // 检查是否已有内容，如有则添加focused类
        if (textarea.value.trim() !== '') {
            textarea.parentElement.classList.add('focused');
        }
    });
    
    // 回复按钮效果增强
    const replyBtns = document.querySelectorAll('.reply-btn');
    replyBtns.forEach(btn => {
        btn.addEventListener('mouseenter', function() {
            this.querySelector('i').classList.add('fa-bounce');
        });
        
        btn.addEventListener('mouseleave', function() {
            this.querySelector('i').classList.remove('fa-bounce');
        });
    });
}); 