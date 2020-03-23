from django.urls import path
from .views import *
urlpatterns = [
    path('not_done' , todo_not_done ,name = 'todo_not_done'),
    path('done' , todo_done ,name = 'todo_done'),
    path('add' , add_todo ,name = 'add_todo'),
    path('show/<int:todo_id>-<str:from_complate_template>' , show_todo ,name = 'show_todo'),
    path('edit/<int:todo_id>' , edit_todo ,name = 'edit_todo'),

]

