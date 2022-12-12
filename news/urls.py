from django.urls import path
from .views import PostListView, PostDetailView, SearchPostListView, PostCreateView, PostUpdateView, PostDeleteView
from .views import subscribe

app_name = 'news'

urlpatterns = [
    path('', PostListView.as_view(), name='all_news'),
    path('category/<int:category_pk>/', PostListView.as_view(), name='all_news'),
    path('search/', SearchPostListView.as_view(), name='search'),
    path('<int:pk>/', PostDetailView.as_view(), name='detail'),
    path('add/', PostCreateView.as_view(), name='add_post'),
    path('subscribe/<int:category_pk>/', subscribe, name='subscribe'),
    path('<int:pk>/edit/', PostUpdateView.as_view(), name='update_post'),
    path('<int:pk>/delete/', PostDeleteView.as_view(), name='delete_post'),
]