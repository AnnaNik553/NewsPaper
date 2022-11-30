# python manage.py shell
#
# # 1. Создать двух пользователей (с помощью метода User.objects.create_user).
#
# from django.contrib.auth.models import User
# user1 = User.objects.create_user(username='user1')
# user2 = User.objects.create_user(username='user2')
#
# # 2. Создать два объекта модели Author, связанные с пользователями.
#
# from news.models import Author
# Author.objects.create(user=user1)
# Author.objects.create(user=user2)
# a1 = Author.objects.get(pk=1)
# a2 = Author.objects.get(pk=2)
#
# # 3. Добавить 4 категории в модель Category.
#
# from news.models import Category
# Category.objects.create(title='Спорт')
# Category.objects.create(title='Политика')
# Category.objects.create(title='Образование')
# Category.objects.create(title='Здоровье')
#
# # 4. Добавить 2 статьи и 1 новость.
#
# from news.models import Post
# art1 = Post.objects.create(author=a1, type_of_post='arti', title='Статья 1', text='test test test')
# art2 = Post.objects.create(author=a2, type_of_post='arti', title='Статья 2', text='test test test')
# news1 = Post.objects.create(author=a1, type_of_post='news', title='Новость 1', text='test test test')
#
# # 5. Присвоить им категории (как минимум в одной статье/новости должно быть не меньше 2 категорий).
#
# sport = Category.objects.get(title='Спорт')
# politic = Category.objects.get(title='Политика')
# art1.categories.add(sport, politic)
# art2.categories.add(sport)
# news1.categories.add(politic)
#
# # 6. Создать как минимум 4 комментария к разным объектам модели Post (в каждом объекте должен быть как минимум один комментарий).
#
# from news.models import Comment
# com1 = Comment.objects.create(post=art1, user=user2, text='комментарий 1')
# com2 = Comment.objects.create(post=art1, user=user2, text='комментарий 2')
# com3 = Comment.objects.create(post=art2, user=user1, text='комментарий 3')
# com4 = Comment.objects.create(post=news1, user=user1, text='комментарий 4')
#
# # 7. Применяя функции like() и dislike() к статьям/новостям и комментариям, скорректировать рейтинги этих объектов.
#
# com1.like()
# com1.like()
# com1.like()
# com1.dislike()
#
# art1.like()
# art1.dislike()
# art1.dislike()
# art1.dislike()
# art1.dislike()
#
# art2.like()
# art2.like()
# art2.like()
# art2.like()
# art2.like()
# art2.like()
# art2.like()
#
# # 8.Обновить рейтинги пользователей.
#
# a1.update_rating()
# a2.update_rating()
#
# # 9. Вывести username и рейтинг лучшего пользователя (применяя сортировку и возвращая поля первого объекта).
#
# Author.objects.all().order_by('-rating').values('user__username', 'rating')[0]
#
# # 10. Вывести дату добавления, username автора, рейтинг, заголовок и превью лучшей статьи, основываясь на лайках/дислайках к этой статье.
#
# best = Post.objects.filter(type_of_post='arti').order_by('-rating')[0]
# values = Post.objects.filter(pk=best.pk).values('created_at', 'author__user__username', 'rating', 'title')[0]
# values
# best.preview()
#
# # 11. Вывести все комментарии (дата, пользователь, рейтинг, текст) к этой статье.
#
# best.comment_set.all().values_list('created_at', 'user__username', 'rating', 'text')