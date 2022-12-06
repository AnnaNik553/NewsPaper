import django_filters
from django_filters import FilterSet
from .models import Post


class PostFilter(FilterSet):
    created_at = django_filters.DateFilter(lookup_expr='date__gt', label='Дата позже чем')
    title = django_filters.CharFilter(lookup_expr='icontains', label='Заголовок')
    author__user__username = django_filters.CharFilter(lookup_expr='icontains', label='Имя автора')

    class Meta:
        model = Post
        fields = ['created_at', 'title', 'author__user__username']
