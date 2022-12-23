from django.contrib import admin
from .models import Author, Post, Category, Comment, PostCategory


class AuthorAdmin(admin.ModelAdmin):
    list_display = ('user', 'rating')
    list_filter = ('user',)
    search_fields = ('user',)


class PostAdmin(admin.ModelAdmin):
    list_display = ['author', 'type_of_post', 'created_at', 'title', 'rating']
    search_fields = ('author', 'title', 'rating')


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title',)
    list_filter = ('title',)


# Register your models here.
admin.site.register(Author, AuthorAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Comment)
admin.site.register(PostCategory)




