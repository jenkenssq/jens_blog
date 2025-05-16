from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone

class UserProfile(models.Model):
    """用户资料模型"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    avatar = models.ImageField('头像', upload_to='avatars/', blank=True, null=True)
    bio = models.TextField('个人简介', max_length=500, blank=True)
    website = models.URLField('个人网站', blank=True)
    location = models.CharField('所在地', max_length=100, blank=True)
    
    class Meta:
        verbose_name = '用户资料'
        verbose_name_plural = verbose_name
    
    def __str__(self):
        return f'{self.user.username}的资料'

class Category(models.Model):
    """文章分类模型"""
    name = models.CharField('分类名称', max_length=100)
    description = models.TextField('分类描述', blank=True)
    created_time = models.DateTimeField('创建时间', auto_now_add=True)
    
    class Meta:
        verbose_name = '分类'
        verbose_name_plural = verbose_name
        ordering = ['-created_time']
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('blog:category', kwargs={'pk': self.pk})
    
    def get_post_count(self):
        return self.post_set.count()

class Tag(models.Model):
    """文章标签模型"""
    name = models.CharField('标签名', max_length=100)
    created_time = models.DateTimeField('创建时间', auto_now_add=True)

    class Meta:
        verbose_name = '标签'
        verbose_name_plural = verbose_name
        ordering = ['-created_time']

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('blog:tag', kwargs={'pk': self.pk})
    
    def get_post_count(self):
        return self.post_set.count()

class Post(models.Model):
    """博客文章模型"""
    title = models.CharField('标题', max_length=200)
    content = models.TextField('内容')
    created_time = models.DateTimeField('创建时间', default=timezone.now)
    modified_time = models.DateTimeField('修改时间', auto_now=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='作者')
    excerpt = models.CharField('摘要', max_length=200, blank=True)
    views = models.PositiveIntegerField('阅读量', default=0)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='分类', null=True, blank=True)
    tags = models.ManyToManyField(Tag, verbose_name='标签', blank=True)
    
    class Meta:
        verbose_name = '文章'
        verbose_name_plural = verbose_name
        ordering = ['-created_time']
        
    def __str__(self):
        return self.title
        
    def get_absolute_url(self):
        return reverse('blog:post_detail', kwargs={'pk': self.pk})
        
    def increase_views(self):
        self.views += 1
        self.save(update_fields=['views'])

class Comment(models.Model):
    """评论模型"""
    post = models.ForeignKey(Post, on_delete=models.CASCADE, verbose_name='文章')
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='评论者')
    content = models.TextField('评论内容')
    created_time = models.DateTimeField('创建时间', auto_now_add=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, verbose_name='父评论')
    
    class Meta:
        verbose_name = '评论'
        verbose_name_plural = verbose_name
        ordering = ['-created_time']
    
    def __str__(self):
        return f'{self.author.username}: {self.content[:20]}'
