from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'mysite.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^polls/', include('polls.urls', namespace="polls")),  # hook polls/urls.py
    url(r'^todos/', include('todos.urls', namespace="todos")),  # hook todo/urls.py
    url(r'^admin/', include(admin.site.urls))
    # note: here regex only cares about leading of url
)

# NOTE
# Whenever Django encounters include(),
# it chops off whatever part of the URL matched up to that point and
# sends the remaining string to the included URLconf for further processing.
#     e.g. http://hostname/todos/50/results
# match: todos/ : chopped
# remaining string: '50/results' to todos.urls.py
