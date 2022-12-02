from django.urls import path
from .views import PostListView, PostDetailView

app_name = 'news'

urlpatterns = [
    path('', PostListView.as_view(), name='all_news'),
    path('<int:pk>/', PostDetailView.as_view(), name='detail'),
]