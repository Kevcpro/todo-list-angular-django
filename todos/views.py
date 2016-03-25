import json

from django.shortcuts import render
# Create your views here.
from django.http import Http404
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.http import JsonResponse
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt

from todos.models import ToDo

METHOD_NOT_ALLOWED_MSG = {'result':'fail',
                          'message':'Mehod Not Allowed'}

def get_index_page(request):
    """ng app main page"""
    if request.method == 'GET':
        return render(request, 'todos/index.html', status=200)
    else:
        return JsonResponse(METHOD_NOT_ALLOWED_MSG, status=405)


def _random_string(N=5):
    import string, random
    return ''.join(random.choice(string.ascii_letters + string.digits) \
        for _ in range(N))

@csrf_exempt    # marks it as being exempt from the protection by the middleware
def get_all_or_create_new_task(request):
    """display all todo tasks in json, or create a new task."""

    if request.method == 'GET':
        all_tasks_query_set = ToDo.objects.all().order_by('-pub_date')
        # type: <class 'django.db.models.query.QuerySet'>
        serial_tasks = serializers.serialize('json', all_tasks_query_set)
        # typeof(serial_tasks): unicode

        if serial_tasks:
            tasks_json = json.loads(serial_tasks) # type: list

            # legacy: use HttpResponse()
            # dump only value of 'fields'
            # data = json.dumps([task['fields'] for task in tasks_json])
            # return HttpResponse(data)

            # NOTE: when use JsonResponse, don't use dumped data
            #  use unrendered data, JsonResponse implicitly calls json.dumps()
            # if pass dumped data, would response with baskslash (dump tiwce)
            # stackoverflow:
            # Why JSON returned from django have forward slashes in response
            return JsonResponse({'result':'success', 'data': [task['fields'] \
                for task in tasks_json]})
        else:
            return JsonResponse({'result':'success', 'data':[]})

    # create a new task
    elif request.method == 'POST':
        # legacy: parse from HTTP request with form
        #  _task_name = request.POST.get("task")
        # _task_name = request.POST.get(u'task')
        # print(request.POST) # <QueryDict: {u'task': [u'task name']}>

        # TODO: understand request api:
        #     e.g. request.body, request.POST

        # parse json from request.body (str)
        req_body_dict = json.loads(request.body)  # dict
        _task_name = req_body_dict.get('task')

        if _task_name:
            # handle if db is over space limit
            if ToDo.objects.count() >= 30:
                return JsonResponse({'result':'failed',
                                    'message':'reached limit of 30 tasks.'},
                                    status=403)

            from django.utils import timezone
            task_id = _random_string()
            ToDo.objects.create(task=_task_name,
                                pub_date=timezone.now(),
                                status=False,
                                task_id=task_id)

            return JsonResponse({'result': 'successfully created',
                                 'task_id': task_id},
                                 status=201)
            # legacy: redirect with html request with form
            # return HttpResponseRedirect(reverse('todos:all_tasks_html'))
        else:
            return JsonResponse({'result':'failed',
                                'message':'bad request'},
                                status=400)
    else:
        return JsonResponse(METHOD_NOT_ALLOWED_MSG, status=405)

@csrf_exempt
def get_update_delete_one_task(request, task_id):
    """get one task information, or update one, or delete one."""

    # get one task
    if request.method == 'GET':
        _task = ToDo.objects.filter(task_id__exact=task_id)
        # <class 'django.db.models.query.QuerySet'>
        # queryset can be serialized

        # NOTE: c.f. a model instance cannot be serialized
        # _task = ToDo.objects.get(task_id__exact=task_id)
        # <class 'todos.models.ToDo'>
        # can access _task.task, _task.pub_date;

        if _task:
            _task_ser = serializers.serialize('json', _task)
            _task_json = json.loads(_task_ser)  # list
            return JsonResponse({'result': [task['fields'] \
                for task in _task_json]})
        else:
            return JsonResponse({'result': 'failed', 'message':'bad uri'},
                                status=404)
    # update one task
    elif request.method == 'PUT':
        _task = ToDo.objects.filter(task_id__exact=task_id)  # queryset
        if _task:
            # TODO: validate request.body: only extracts request.body['status']
            req_body_dict = json.loads(request.body)  # dict
            # update a model with dict
            _task.update(**req_body_dict) # raise error if contain bad key

            _task_json = json.loads(serializers.serialize('json', _task))# list
            return JsonResponse({'result' : "successfully updated", \
                "data" : [task['fields'] for task in _task_json]})
        else:
            return JsonResponse({'result': 'failed', 'message':'bad uri'},
                                status=404)

    # delete a task
    elif request.method == 'DELETE':
        _task = ToDo.objects.filter(task_id__exact=task_id)  # queryset
        # NOTE: use .filter() support multiple instances  (queryset)

        #_task = ToDo.objects.get(task_id__exact=task_id)  # model instance
        # NOTE: .get() raises error if return multiple/no matching instances

        if _task:
            _task.delete()
            return JsonResponse({'result' : "successfully deleted"})
        else:
            return JsonResponse({'result': 'failed',
                                'message':'bad uri'},
                                status=404)

    else:
        return JsonResponse(METHOD_NOT_ALLOWED_MSG, status=405)


def latest_task(request):
    """response latest task, deprecated"""
    #return JsonResponse({'result':'sucess', 'data':[]})
    if request.method == 'GET':
        print 'GET enter'
        if ToDo.objects.count() == 0:
            return JsonResponse({'result':'sucess', 'data':[]})
        latest_task = []
        latest_task.append(ToDo.objects.order_by('-pub_date')[0])
        # alter: latest_task = ToDo.objects.order_by('-pub_date')[:1]
        if latest_task:
            latest_task_serialize = serializers.serialize('json', latest_task)
            _task_json = json.loads(latest_task_serialize)  # list
            return JsonResponse({'result': 'sucess', 'data': [task['fields'] \
                for task in _task_json]})

    else:
        return JsonResponse(METHOD_NOT_ALLOWED_MSG, status=405)
