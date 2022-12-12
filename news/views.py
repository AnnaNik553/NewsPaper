from django.contrib import messages
from django.shortcuts import HttpResponseRedirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib import messages

from .models import Post, Category
from .filters import PostFilter
from .forms import PostForm
from .utils import notifying_subscribers_about_news, can_author_create_post

# Create your views here.


class PostListView(ListView):
    model = Post
    template_name = 'news/posts.html'
    context_object_name = 'posts'
    ordering = '-created_at'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['count'] = len(self.get_queryset())
        context['categories'] = Category.objects.all()
        if self.request.user.is_authenticated:
            context['is_not_author'] = not self.request.user.groups.filter(name='authors').exists()
        category = self.request.resolver_match.kwargs.get('category_pk')
        context['is_category'] = category
        if category:
            context['current_category'] = Category.objects.get(pk=category)
        return context

    def get_queryset(self):
        category_pk = self.request.resolver_match.kwargs.get('category_pk')
        if category_pk:
            queryset = Post.objects.filter(categories__pk=category_pk)
        else:
            queryset = Post.objects.all()
        ordering = self.get_ordering()
        if ordering:
            if isinstance(ordering, str):
                ordering = (ordering,)
            queryset = queryset.order_by(*ordering)
        return queryset


class SearchPostListView(ListView):
    model = Post
    template_name = 'news/search_posts.html'
    context_object_name = 'posts'
    ordering = '-created_at'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = PostFilter(self.request.GET, queryset=self.get_queryset())
        return context


class PostDetailView(DetailView):
    model = Post
    template_name = 'news/post.html'
    context_object_name = 'post'


class PostCreateView(PermissionRequiredMixin, CreateView):
    template_name = 'news/post_create.html'
    form_class = PostForm
    permission_required = ('news.add_post',)

    def form_valid(self, form):
        """If the form is valid, save the associated model."""

        if can_author_create_post(self.request.user):

            self.object = form.save()

            notifying_subscribers_about_news(self.object, self.request.build_absolute_uri(self.object.get_absolute_url()))

            return super().form_valid(form)
        else:
            messages.error(self.request, 'Вы не можете публиковать более трех постов в день. Попробуйте завтра.')
            return self.get(self, self.request)


class PostUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    template_name = 'news/post_create.html'
    form_class = PostForm
    permission_required = ('news.change_post',)

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)


class PostDeleteView(DeleteView):
    template_name = 'news/post_delete.html'
    queryset = Post.objects.all()
    success_url = '/news/'


def subscribe(request, category_pk):
    category = Category.objects.get(pk=category_pk)
    if not category.subscribers.filter(pk=request.user.pk).exists():
        category.subscribers.add(request.user)
        category.save()
        messages.success(request, 'Вы успешно подписаны')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
