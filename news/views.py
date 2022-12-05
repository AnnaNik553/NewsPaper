from django.shortcuts import render
from django.views.generic import ListView, DetailView

from .models import Post
from .filters import PostFilter

# Create your views here.


class PostListView(ListView):
    model = Post
    template_name = 'news/posts.html'
    context_object_name = 'posts'
    ordering = '-created_at'
    paginate_by = 10


class SearchPostListView(ListView):
    model = Post
    template_name = 'news/search_posts.html'
    context_object_name = 'posts'
    ordering = '-created_at'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = PostFilter(self.request.GET, queryset=self.get_queryset())
        return context


class PostDetailView(DetailView):
    model = Post
    template_name = 'news/post.html'
    context_object_name = 'post'