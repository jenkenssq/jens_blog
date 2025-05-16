from django import template
from django.utils.safestring import mark_safe
import re

register = template.Library()

@register.filter
def highlight(text, search):
    """高亮显示文本中的搜索词"""
    if not search:
        return text
    
    # 转义搜索词中的特殊字符
    search = re.escape(search)
    
    # 使用正则表达式进行不区分大小写的搜索
    pattern = re.compile(f'({search})', re.IGNORECASE)
    
    # 在匹配的文本周围添加高亮样式
    highlighted = pattern.sub(r'<span class="text-highlight">\1</span>', str(text))
    
    return mark_safe(highlighted) 