from django.forms import ModelForm
from .models import Post


class PostForm(ModelForm):

    class Meta:
        model = Post
        fields = ['author', 'type_of_post', 'categories', 'title', 'text']
