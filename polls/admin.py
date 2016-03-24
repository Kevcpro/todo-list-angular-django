from django.contrib import admin
# Register your models here.
from polls.models import Question, Choice, ToDo

# class ChoiceInline(admin.StackedInline):    # different ui element
class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3


class QuestionAdmin(admin.ModelAdmin):
    # ui display : http://127.0.0.1:8000/admin/polls/question/
    list_display = ('question_text', 'pub_date', 'was_published_recently')
    fieldsets = [
        (None,               {'fields': ['question_text']}),
        ('Date information', {'fields': ['pub_date'], 'classes': ['collapse']}),
    ]

    # add related ChoiceInline model
    # ui display : http://127.0.0.1:8000/admin/polls/question/2/
    inlines = [ChoiceInline]

    # add filter, search ui
    # http://127.0.0.1:8000/admin/polls/question/
    list_filter = ['pub_date']
    search_fields = ['question_text']


class ToDoAdmin(admin.ModelAdmin):
    # ui display: http://127.0.0.1:8000/admin/polls/todo/
    # referencing models.ToDo
    list_display = ('task', 'status', 'uri', 'pub_date', 'was_published_recently')
    fieldsets = [
        (None,               {'fields': ['task']}),
        ('Date information', {'fields': ['pub_date'], 'classes': ['collapse']}),
    ]

    # add filter, search ui
    # http://127.0.0.1:8000/admin/polls/todo/
    list_filter = ['pub_date', 'status']
    search_fields = ['task']

# at most 3 arguments
admin.site.register(Question, QuestionAdmin)
admin.site.register(ToDo, ToDoAdmin)
