from django.urls import path
from .views import *
urlpatterns = [

    path('not_done/' , todo_not_done ,name = 'todo_not_done'),
    path('done/' , todo_done ,name = 'todo_done'),
    path('add/' , add_todo ,name = 'add_todo'),
    path('show/<int:todo_id>' , show_todo ,name = 'show_todo'),
    path('edit/<int:todo_id>' , edit_todo ,name = 'edit_todo'),
    path('delete/<int:todo_id>' , delete_todo ,name = 'delete_todo'),
    path('complate/<int:todo_id>' , complate_todo ,name = 'complate_todo'),
    path('clear/' , clear_todo ,name = 'clear_todo'),
    path('settings/' , account_settings ,name = 'account_settings'),

]

