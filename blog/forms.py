from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Post, Category, Tag, Comment, UserProfile

class UserRegisterForm(UserCreationForm):
    """用户注册表单"""
    email = forms.EmailField()
    verification_code = forms.CharField(
        label='验证码',
        max_length=6,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '请输入邮箱验证码'
        })
    )
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'verification_code']

class PostForm(forms.ModelForm):
    """文章表单"""
    class Meta:
        model = Post
        fields = ['title', 'content', 'excerpt', 'category', 'tags']
        widgets = {
            'tags': forms.CheckboxSelectMultiple(),
        }

class CommentForm(forms.ModelForm):
    """评论表单"""
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'rows': 4, 
                'placeholder': '在此输入评论...', 
                'class': 'form-control shadow-sm border-primary rounded-3',
                'style': 'resize:none; transition:all 0.3s ease; height:120px;'
            }),
        } 

class UserUpdateForm(forms.ModelForm):
    """用户信息更新表单"""
    email = forms.EmailField()
    
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
        }

class ProfileUpdateForm(forms.ModelForm):
    """用户资料更新表单"""
    class Meta:
        model = UserProfile
        fields = ['avatar', 'bio', 'location', 'website']
        widgets = {
            'avatar': forms.FileInput(attrs={
                'class': 'form-control d-none',
                'accept': 'image/*'
            }),
            'bio': forms.Textarea(attrs={
                'rows': 4, 
                'class': 'form-control',
                'placeholder': '简单介绍一下自己吧...'
            }),
            'location': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '您的所在地，如：北京'
            }),
            'website': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': '您的个人网站，如：https://example.com'
            }),
        } 