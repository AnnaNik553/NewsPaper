from django.core.mail import EmailMultiAlternatives, get_connection
from django.template.loader import render_to_string
import datetime

from django.core.mail import send_mail
from news.models import Category
from django.db.models import Count


NUMBER_ALLOWED_POSTS_DEY = 3


def notifying_subscribers_about_news(obj, path_link):
    post_categories = obj.categories.all()
    subscribers = list(set(sum([list(category.subscribers.all()) for category in post_categories], [])))
    if subscribers:
        email_addresses_usernames = [(user.email, user.username) for user in subscribers if user.email]
        url = path_link
        letters = [render_to_string('news/letter.html', {'user': user[1], 'title': obj.title, 'text': obj.text, 'url': url}) for user in email_addresses_usernames]

        con = get_connection(fail_silently=True)
        con.open()

        emails = []
        for user, letter in zip(email_addresses_usernames, letters):
            em = EmailMultiAlternatives(subject=f'NewsPaper - {obj.title}',
                              body=f'NewsPaper - {obj.title}',
                              from_email='NewsPaperAdmin <matoko18@yandex.ru>',
                              to=[user[0]])
            em.attach_alternative(letter, 'text/html')
            emails.append(em)

        con.send_messages(emails)
        con.close()
    return


def can_author_create_post(user):
    author = user.author
    posts = author.post_set.filter(created_at__date=datetime.date.today()).count()
    return posts < NUMBER_ALLOWED_POSTS_DEY


def weekly_newsletter():
    # категории, где есть подписчики
    category = [c for c in Category.objects.annotate(Count('subscribers')) if c.subscribers__count > 0]
    # получаем статьи к каждой категории за неделю
    posts = [c.post_set.filter(created_at__date__gt=datetime.date.today() - datetime.timedelta(days=8),
                               created_at__date__lt=datetime.date.today()) for c in category]

    for cat, post in zip(category, posts):
        if post:
            subscribers = cat.subscribers.all()
            if subscribers:
                html_message = '<h2>Статьи и новости за прошедшую неделю</h2>'
                for p in post:
                    url = 'http://127.0.0.1:8000' + p.get_absolute_url()
                    html_message += f'<h3>{p.title}</h3><a href="{url}">Прочитать</a>'
                email_addresses = [user.email for user in subscribers if user.email]
                send_mail('NesPaper - Статьи и новости за прошедшую неделю',
                          'NesPaper - Статьи и новости за прошедшую неделю',
                          from_email='NewsPaperAdmin <matoko18@yandex.ru>',
                          recipient_list=email_addresses,
                          fail_silently=False,
                          html_message=html_message)
