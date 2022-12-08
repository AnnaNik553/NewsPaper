from django.shortcuts import HttpResponseRedirect
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required

@login_required
def become_author(request):
    user = request.user
    author_group = Group.objects.get(name='authors')
    if not request.user.groups.filter(name='authors').exists():
        author_group.user_set.add(user)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
