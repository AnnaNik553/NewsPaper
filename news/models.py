from django.db import models
from django.contrib.auth.models import User


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0, verbose_name='рейтинг')

    def update_rating(self):
        articles = sum([art.rating for art in Post.objects.filter(author=self, type_of_post='arti')]) * 3
        comments = sum([com.rating for com in Comment.objects.filter(user=self.user)])
        articles_comments = sum([com.rating for com in Comment.objects.filter(post__author=self, post__type_of_post='arti')])
        self.rating = articles + comments + articles_comments
        self.save()

    def __str__(self):
        return f'{self.user}'


class Category(models.Model):
    title = models.CharField(max_length=255, unique=True, verbose_name='название категории')

    def __str__(self):
        return self.title


class Post(models.Model):
    TYPES = (
        ('arti', 'статья'),
        ('news', 'новость')
    )
    author = models.ForeignKey(Author, on_delete=models.SET('автор неизвестен'), verbose_name='автор')
    type_of_post = models.CharField(max_length=4, choices=TYPES, default='news', verbose_name='тип поста')
    created_at = models.DateTimeField(auto_now_add=True)
    categories = models.ManyToManyField(Category, through='PostCategory', verbose_name='категории')
    title = models.CharField(max_length=255, verbose_name='заголовок')
    text = models.TextField(verbose_name='текст')
    rating = models.IntegerField(default=0, verbose_name='рейтинг')

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
        return f'{self.text[:124]}...'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return f'/news/{self.id}'


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField(verbose_name='текст')
    created_at = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0, verbose_name='рейтинг')

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()



