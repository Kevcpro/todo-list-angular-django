from django.contrib import admin

from todos.models import ToDo


class ToDoAdmin(admin.ModelAdmin):
    # ui display: http://127.0.0.1:8000/admin/todos/todo/
    # referencing models.ToDo
    list_display = ('task', 'status', 'task_id', 'pub_date', 'was_published_recently')
    fieldsets = [
        (None,               {'fields': ['task', 'task_id', 'status']}),
        ('Date information', {'fields': ['pub_date'], 'classes': ['collapse']}),
    ]

    # add filter, search ui
    # http://127.0.0.1:8000/admin/todos/todo/
    list_filter = ['pub_date', 'status']
    search_fields = ['task']

# at most 3 arguments
admin.site.register(ToDo, ToDoAdmin)
