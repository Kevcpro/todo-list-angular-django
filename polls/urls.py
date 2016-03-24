from django.conf.urls import patterns, url

from polls import views

urlpatterns = patterns('',
    # hook ./views.py
    # e.g. /polls/
    url(r'^$', views.index, name='index'),
    # e.g. /polls/5/
    url(r'^(?P<question_id>\d+)/$', views.detail, name='detail'),
    # e.g. /polls/5/results/
    url(r'^(?P<question_id>\d+)/results/$', views.results, name='results'),
    # e.g. /polls/5/vote/
    url(r'^(?P<question_id>\d+)/vote/$', views.vote, name='vote'),
    # e.g. /polls/get_latest_task/
    url(r'^get_latest_task/$', views.get_latest_task, name='get_latest_task'),
    # e.g. /polls/all_tasks_html/
    url(r'^all_tasks_html/$', views.all_tasks_html, name='all_tasks_html'),
    # e.g. /polls/all_tasks_json
    url(r'^all_tasks/$', views.all_tasks_json, name='all_tasks_json'),
    # e.g. /polls/all_tasks/new, POST
    url(r'^all_tasks/new/$', views.new_task, name='new_task'),
    # e.g. /polls/all_tasks/<task_uri>
    url(r'^all_tasks/(?P<task_uri>[\w\d]+)/$',
        views.get_task, name='get_task'),
    # e.g. /polls/all_tasks/<task_uri>/update
    url(r'^all_tasks/(?P<task_uri>[\w\d]+)/update/$',
        views.update_task, name='update_task'),
    # e.g. /polls/all_tasks/<task_uri>/update
    url(r'^all_tasks/(?P<task_uri>[\w\d]+)/delete/$',
        views.delete_task, name='delete_task'),
    # customize url
    url(r'^$', views.index, name='home')
)

# /polls/50/results
# here processing url is '50/results' as remaining
# since leading '/polls/' is already chopped in mysite/urls.py
