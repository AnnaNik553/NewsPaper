from django.core.mail import EmailMultiAlternatives, get_connection
from django.template.loader import render_to_string
import datetime

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
