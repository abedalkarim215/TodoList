from django.shortcuts import render
from .models import *

def home(request) :
    return render(request,'todo/layouts/base-todo.html')

def todo_not_done(request) :
    todos = Todo.objects.filter(user=request.user, date_completed__isnull=True)
    context = {
        'todos' : todos
    }
    return render(request,'todo/todo_not_done.html',context)

def todo_done(request) :
    todos = Todo.objects.filter(user=request.user, date_completed__isnull=False)
    context = {
        'todos': todos
    }
    return render(request, 'todo/todo-done.html',context)