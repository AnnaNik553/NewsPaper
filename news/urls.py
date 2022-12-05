from django.urls import path
from .views import PostListView, PostDetailView, SearchPostListView

app_name = 'news'

urlpatterns = [
    path('', PostListView.as_view(), name='all_news'),
    path('search/', SearchPostListView.as_view(), name='search'),
    path('<int:pk>/', PostDetailView.as_view(), name='detail'),
]