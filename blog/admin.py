from django.contrib import admin
from .models import Post, Category, Tag, Comment, UserProfile

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'category', 'created_time', 'modified_time', 'views')
    list_filter = ('created_time', 'category', 'author')
    search_fields = ('title', 'content')
    date_hierarchy = 'created_time'
    ordering = ('-created_time',)
    filter_horizontal = ('tags',)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'created_time')
    search_fields = ('name', 'description')
    date_hierarchy = 'created_time'
    ordering = ('-created_time',)

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_time')
    search_fields = ('name',)
    date_hierarchy = 'created_time'
    ordering = ('-created_time',)

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'content', 'post', 'created_time')
    list_filter = ('created_time', 'author')
    search_fields = ('content', 'author__username', 'post__title')
    date_hierarchy = 'created_time'
    ordering = ('-created_time',)

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'location', 'website')
    search_fields = ('user__username', 'bio', 'location')
