from django.shortcuts import render
from django.views.generic import ListView, DetailView

from .models import Post

# Create your views here.


class PostListView(ListView):
    model = Post
    template_name = 'news/posts.html'
    context_object_name = 'posts'
    ordering = '-created_at'


class PostDetailView(DetailView):
    model = Post
    template_name = 'news/post.html'
    context_object_name = 'post'