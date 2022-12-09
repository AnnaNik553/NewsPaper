from django.contrib import messages
from django.shortcuts import render, HttpResponseRedirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.core.mail import send_mail, send_mass_mail, EmailMultiAlternatives, EmailMessage, get_connection
from django.template.loader import render_to_string
from django.views.generic.edit import BaseUpdateView

from .models import Post, Category
from .filters import PostFilter
from .forms import PostForm

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
        self.object = form.save()

        post_categories = self.object.categories.all()
        subscribers = list(set(sum([list(category.subscribers.all()) for category in post_categories], [])))
        if subscribers:
            email_addresses_usernames = [(user.email, user.username) for user in subscribers if user.email]

            letters = [render_to_string('news/letter.html', {'user': user[1], 'title': self.object.title, 'text': self.object.text}) for user in email_addresses_usernames]

            con = get_connection(fail_silently=True)
            con.open()

            emails = []
            for user, letter in zip(email_addresses_usernames, letters):
                em = EmailMultiAlternatives(subject=f'NewsPaper - {self.object.title}',
                                  body=f'NewsPaper - {self.object.title}',
                                  from_email='NewsPaperAdmin <matoko18@yandex.ru>',
                                  to=[user[0]])
                em.attach_alternative(letter, 'text/html')
                emails.append(em)

            con.send_messages(emails)
            con.close()

        return super().form_valid(form)


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
