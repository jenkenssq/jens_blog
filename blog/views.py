from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (
    ListView, 
    DetailView, 
    CreateView, 
    UpdateView,
    DeleteView
)
from django.db.models import Q
from django.http import JsonResponse
from .models import Post, Category, Tag, Comment, UserProfile
from .forms import UserRegisterForm, PostForm, CommentForm, UserUpdateForm, ProfileUpdateForm
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from .utils import generate_verification_code, send_verification_email, save_verification_code, verify_code

def register(request):
    """用户注册视图"""
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            verification_code = form.cleaned_data.get('verification_code')
            
            # 验证验证码
            if verify_code(email, verification_code):
                form.save()
                username = form.cleaned_data.get('username')
                messages.success(request, f'账号 {username} 已创建，现在您可以登录了')
                return redirect('login')
            else:
                messages.error(request, '验证码错误或已过期，请重新获取')
    else:
        form = UserRegisterForm()
    return render(request, 'blog/register.html', {'form': form})

def send_verification_code(request):
    """发送验证码的视图函数"""
    if request.method == 'POST':
        email = request.POST.get('email')
        if not email:
            return JsonResponse({'status': 'error', 'message': '请提供邮箱地址'})
        
        # 生成验证码
        code = generate_verification_code()
        
        # 保存验证码到缓存
        save_verification_code(email, code)
        
        # 发送验证码邮件
        try:
            send_verification_email(email, code)
            return JsonResponse({'status': 'success', 'message': '验证码已发送，请查收邮件'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': f'发送邮件失败: {str(e)}'})
    
    return JsonResponse({'status': 'error', 'message': '非法请求'})

@login_required
def profile(request):
    """用户个人中心视图"""
    # 尝试获取用户资料，如果不存在则创建
    try:
        profile = request.user.profile
    except UserProfile.DoesNotExist:
        profile = UserProfile.objects.create(user=request.user)
    
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)
        
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, '您的个人资料已更新！')
            return redirect('blog:profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=profile)
    
    # 获取用户的文章
    user_posts = Post.objects.filter(author=request.user).order_by('-created_time')
    
    context = {
        'u_form': u_form,
        'p_form': p_form,
        'user_posts': user_posts,
        'categories': Category.objects.all(),
        'tags': Tag.objects.all(),
    }
    
    return render(request, 'blog/profile.html', context)

class PostListView(ListView):
    """文章列表视图"""
    model = Post
    template_name = 'blog/home.html'
    context_object_name = 'posts'
    ordering = ['-created_time']
    paginate_by = 5
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['tags'] = Tag.objects.all()
        return context

class PostDetailView(DetailView):
    """文章详情视图"""
    model = Post
    template_name = 'blog/post_detail.html'
    
    def get_object(self):
        # 获取文章对象并增加阅读量
        obj = super().get_object()
        obj.increase_views()
        return obj
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = Comment.objects.filter(post=self.object, parent=None)
        context['comment_form'] = CommentForm()
        context['categories'] = Category.objects.all()
        context['tags'] = Tag.objects.all()
        return context

class PostCreateView(LoginRequiredMixin, CreateView):
    """创建文章视图"""
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['tags'] = Tag.objects.all()
        return context

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """更新文章视图"""
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
        
    def test_func(self):
        # 检查当前用户是否为文章作者
        post = self.get_object()
        return self.request.user == post.author
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['tags'] = Tag.objects.all()
        return context

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """删除文章视图"""
    model = Post
    template_name = 'blog/post_confirm_delete.html'
    success_url = '/'
    
    def test_func(self):
        # 检查当前用户是否为文章作者
        post = self.get_object()
        return self.request.user == post.author

class CategoryView(ListView):
    """分类文章列表视图"""
    model = Post
    template_name = 'blog/category.html'
    context_object_name = 'posts'
    paginate_by = 5
    
    def get_queryset(self):
        category = get_object_or_404(Category, pk=self.kwargs.get('pk'))
        return Post.objects.filter(category=category).order_by('-created_time')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = get_object_or_404(Category, pk=self.kwargs.get('pk'))
        context['category'] = category
        context['categories'] = Category.objects.all()
        context['tags'] = Tag.objects.all()
        return context

class TagView(ListView):
    """标签文章列表视图"""
    model = Post
    template_name = 'blog/tag.html'
    context_object_name = 'posts'
    paginate_by = 5
    
    def get_queryset(self):
        tag = get_object_or_404(Tag, pk=self.kwargs.get('pk'))
        return tag.post_set.order_by('-created_time')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tag = get_object_or_404(Tag, pk=self.kwargs.get('pk'))
        context['tag'] = tag
        context['categories'] = Category.objects.all()
        context['tags'] = Tag.objects.all()
        return context

class CategoryListView(ListView):
    """分类列表视图"""
    model = Category
    template_name = 'blog/category_list.html'
    context_object_name = 'categories'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tags'] = Tag.objects.all()
        return context

class TagListView(ListView):
    """标签列表视图"""
    model = Tag
    template_name = 'blog/tag_list.html'
    context_object_name = 'tags'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context

@login_required
def add_comment(request, pk):
    """添加评论视图"""
    post = get_object_or_404(Post, pk=pk)
    
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            messages.success(request, '评论已发布！')
            return redirect('blog:post_detail', pk=post.pk)
    else:
        form = CommentForm()
    
    return redirect('blog:post_detail', pk=post.pk)

@login_required
def add_reply(request, pk):
    """添加回复视图"""
    parent_comment = get_object_or_404(Comment, pk=pk)
    post = parent_comment.post
    
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            reply = form.save(commit=False)
            reply.post = post
            reply.author = request.user
            reply.parent = parent_comment
            reply.save()
            messages.success(request, '回复已发布！')
    
    return redirect('blog:post_detail', pk=post.pk)

@login_required
def delete_comment(request, pk):
    """删除评论视图"""
    comment = get_object_or_404(Comment, pk=pk)
    post_pk = comment.post.pk
    
    # 检查是否是评论作者或文章作者
    if request.user == comment.author or request.user == comment.post.author:
        comment.delete()
        messages.success(request, '评论已删除！')
    else:
        messages.error(request, '您没有权限删除此评论！')
    
    return redirect('blog:post_detail', pk=post_pk)

def search(request):
    """搜索视图"""
    query = request.GET.get('q')
    if query:
        posts = Post.objects.filter(
            Q(title__icontains=query) | Q(content__icontains=query)
        ).distinct().order_by('-created_time')
        
        # 分页处理
        paginator = Paginator(posts, 5)  # 每页显示5篇文章
        page = request.GET.get('page')
        try:
            posts = paginator.page(page)
        except PageNotAnInteger:
            # 如果页码不是整数，显示第一页
            posts = paginator.page(1)
        except EmptyPage:
            # 如果页码超出范围，显示最后一页
            posts = paginator.page(paginator.num_pages)
            
        context = {
            'posts': posts,
            'query': query,
            'categories': Category.objects.all(),
            'tags': Tag.objects.all(),
            'is_paginated': True if paginator.num_pages > 1 else False,
            'page_obj': posts,
        }
        return render(request, 'blog/search_results.html', context)
    else:
        return redirect('blog:home')
