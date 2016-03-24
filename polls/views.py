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

from polls.models import Question
from polls.models import ToDo


def index(request):
    """displays the latest 5 poll questions"""
    # displays the latest 5 poll questions, separated by commas
    # according to publication date

    # [standard]
    # from django.template import loader
    # latest_question_list = Question.objects.order_by('-pub_date')[:5]
    # template = loader.get_template('polls/index.html')
    # context = RequestContext(request, {
    #     'latest_question_list': latest_question_list,
    # })
    # return HttpResponse(template.render(context))

    # [shortcuts]: render
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    context = {'latest_question_list': latest_question_list}
    # add title for template
    context.update({'title': 'latest 5 poll questions'})
    return render(request, 'polls/index.html', context)

    # output = ', '.join([p.question_text for p in latest_question_list])
    # return HttpResponse(output)


def detail(request, question_id):
    """get data of one poll"""
    """
    try:
        question = Question.objects.get(pk=question_id)
    except Question.DoesNotExist:
        raise Http404("Question does not exist")
    """
    # [shortcuts] no need try-except
    from django.shortcuts import get_object_or_404
    question = get_object_or_404(Question, pk=question_id)
    # add title for template
    context = {
        'question': question,
        'title': 'Question # %s' % question_id
    }
    return render(request, 'polls/detail.html', context)


def results(request, question_id):
    msg = "You're looking at the results of question %s." % question_id
    return JsonResponse({'message': msg})


def vote(request, question_id):
    msg = "You're voting on question %s." % question_id
    return JsonResponse({'message': msg})

# - - - - - -  TO-DO list


def all_tasks_html(request):
    """display all todo tasks"""
    """127.0.0.1:8000/polls/all_tasks_html"""
    if request.method == 'GET':
        _all_tasks = ToDo.objects.all().order_by('-pub_date')
        content = {'tasks': _all_tasks}
        if _all_tasks:
            return render(request, 'polls/all_tasks.html', content)


def _all_data_in_model_serialized(Model):
    """get all serialized data from one model"""
    model_data = Model.objects.all()
    # type: <class 'django.db.models.query.QuerySet'>
    return serializers.serialize('json', model_data)


def all_tasks_json(request):  # no-render()
    """display all todo tasks in json"""
    """
    127.0.0.1:8000/polls/all_tasks/
    $ curl -i -X GET  http://127.0.0.1:8000/polls/all_tasks/
    """
    serial_tasks = _all_data_in_model_serialized(ToDo)  # type: unicode
    if serial_tasks:
        tasks_json = json.loads(serial_tasks)  # type: list

        # legacy: use HttpResponse()
        # dump only value of 'fields'
        # data = json.dumps([task['fields'] for task in tasks_json])
        # return HttpResponse(data)

        # NOTE: when use JsonResponse, don't use dumped data
        #    use unrendered data, JsonResponse implicitly calls json.dumps()
        #    if pass dumped data, leads to response with baskslash (dump tiwce)
        # stackoverflow:
        # Why does JSON returned from django have forward slashes in response
        return JsonResponse({'result': [task['fields']
                                        for task in tasks_json]})


def _random_string(N=5):
    import string
    import random
    return ''.join(random.choice(string.ascii_uppercase + string.digits)
                   for _ in range(N))


def new_task(request):
    """create a new task"""
    """
    $ curl -i -H "Content-Type: application/json" -X POST -d '{"task":"learn angularJS"}' http://127.0.0.1:8000/polls/all_tasks/new/
    # -i include HTTP-Header in output, -H Header, -X request, -d data
    """
    if request.method == 'POST':
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
                return JsonResponse({'result': 'failed',
                                     'message': 'reached limit of 30 tasks.'},
                                    status=403)
            from django.utils import timezone
            uri = _random_string()
            ToDo.objects.create(task=_task_name,
                                pub_date=timezone.now(),
                                status=False,
                                uri=uri)
            return JsonResponse({'result': 'successfully created',
                                 'uri': uri},
                                status=201)
            # legacy: redirect with html request with form
            # return HttpResponseRedirect(reverse('polls:all_tasks_html'))


def get_task(request, task_uri):
    """get one task information"""
    """
    curl -i -X GET  http://127.0.0.1:8000/polls/all_tasks/<task_uri>/
    curl -i -X GET  http://127.0.0.1:8000/polls/all_tasks/465Z0/
    """
    _task = ToDo.objects.filter(uri__exact=task_uri)
    # <class 'django.db.models.query.QuerySet'>
    # queryset can be serialized

    #_task = ToDo.objects.get(uri__exact=task_uri) # <class 'polls.models.ToDo'>
    # can access _task.task, _task.pub_date;
    # NOTE: a model instance cannot be serialized

    if _task:
        _task_ser = serializers.serialize('json', _task)
        _task_json = json.loads(_task_ser)  # list
        return JsonResponse({'result': [task['fields']
                                        for task in _task_json]})
    else:
        return JsonResponse({'result': 'failed', 'message': 'bad uri'},
                            status=404)


def update_task(request, task_uri):
    """update name or status of a task"""
    """
    curl -i -H "Content-Type: application/json" -X PUT -d '{"task":"Read a book"}' http://127.0.0.1:8000/polls/all_tasks/<task_uri>/update/

    curl -i -H "Content-Type: application/json" -X PUT -d '{"task":"Read a book"}' http://127.0.0.1:8000/polls/all_tasks/465Z0/update/
    curl -i -H "Content-Type: application/json" -X PUT -d '{"status":false}' http://127.0.0.1:8000/polls/all_tasks/465Z0/update/
    curl -i -H "Content-Type: application/json" -X PUT -d '{"status":true}' http://127.0.0.1:8000/polls/all_tasks/465Z0/update/
    """
    if request.method == 'PUT':
        _task = ToDo.objects.filter(uri__exact=task_uri)  # queryset
        if _task:
            # TODO: validate request.body
            req_body_dict = json.loads(request.body)  # dict
            # update a model with dict
            _task.update(**req_body_dict)  # raise error if contain bad key

            _task_json = json.loads(
                serializers.serialize('json', _task))  # list
            return JsonResponse({'result': "successfully updated",
                                 "data": [task['fields'] for task in _task_json]})
        else:
            return JsonResponse({'result': 'failed', 'message': 'bad uri'},
                                status=404)


def delete_task(request, task_uri):
    """delete a task"""
    """
    curl -i -H "Content-Type: application/json" -X DELETE http://127.0.0.1:8000/polls/all_tasks/<task_uri>/delete/

    curl -i -H "Content-Type: application/json" -X DELETE http://127.0.0.1:8000/polls/all_tasks/465Z0/delete/
    curl -i -H "Content-Type: application/json" -X DELETE http://127.0.0.1:8000/polls/all_tasks/8N5SZ/delete/
    """
    if request.method == 'DELETE':
        _task = ToDo.objects.filter(uri__exact=task_uri)  # queryset
        # NOTE: use .filter() support multiple instances  (queryset)

        #_task = ToDo.objects.get(uri__exact=task_uri)  # model instance
        # NOTE: .get() raises error if return multiple/no matching instances
        if _task:
            _task.delete()
            return JsonResponse({'result': "successfully deleted"})
        else:
            return JsonResponse({'result': 'failed', 'message': 'bad uri'},
                                status=404)


def get_latest_task(request):   # no-render()
    """response latest task, xml request"""
    latest_task = []
    latest_task.append(ToDo.objects.order_by('-pub_date')[0])
    # alter: latest_task = ToDo.objects.order_by('-pub_date')[:1]
    if latest_task:
        latest_task_serialize = serializers.serialize('json', latest_task)
        data = json.dumps(json.loads(latest_task_serialize))
        return HttpResponse(data, content_type="application/json")
