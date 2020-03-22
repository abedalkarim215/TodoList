from django.shortcuts import render ,redirect
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

def add_todo(request) :
    if request.method == "GET" :
        return render(request,'todo/add-todo.html')
    else :
        title = request.POST['title']
        description = request.POST['description']
        is_important = "is_important" in request.POST
        todo = Todo.objects.create(title=title,
                                   description=description,
                                   is_important=is_important,
                                   user=request.user)
        todo.save()
        return redirect('todo_not_done')
