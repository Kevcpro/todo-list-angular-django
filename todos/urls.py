from django.conf.urls import patterns, url

from todos import views

urlpatterns = patterns('',
    # hook ./views.py
    # e.g. /todos/home/
    url(r'^home/$', views.get_index_page, name='home'),
    # e.g. /todos/all
    url(r'^$', views.get_all_or_create_new_task,
        name='get_all_or_create_new_task'),
    # e.g. /todos/latest/
    url(r'^latest/$', views.latest_task, name='latest_task'),
    # NOTE this pattern should be matched before resource uri
    # e.g. /todos/<task_id>/
    url(r'^(?P<task_id>[\w\d]+)/$', views.get_update_delete_one_task,
        name='get_update_delete_one_task'),
)

# NOTE
# e.g. http://hostname/todos/50/results
# here processing url is '50/results' as remaining
# since leading '/todos/' is already chopped in mysite/urls.py
