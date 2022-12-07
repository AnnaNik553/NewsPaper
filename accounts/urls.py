from django.urls import path
from .views import become_author

app_name = 'app_accounts'

urlpatterns = [
    path('upgrade/', become_author, name='become_author')
]