from django.shortcuts import render ,redirect ,get_object_or_404
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

def show_todo(request ,todo_id,from_complate_template) :
    COM = False
    if from_complate_template == "COM" :
        COM = True
    if request.method == "GET" :
        todo = get_object_or_404(Todo,pk =todo_id,user = request.user)
        context = {
            "todo" : todo,
            "from_complate_template" : COM
        }
        return render(request,'todo/show_todo.html',context)

def edit_todo(request,todo_id) :
    todo = get_object_or_404(Todo, pk=todo_id, user=request.user)
    if request.method == "GET" :
        context = {
            "todo": todo,
        }
        return render(request,'todo/edit_todo.html',context)
    else :
        todo.title = request.POST['title']
        todo.description = request.POST['description']
        todo.is_important = "is_important" in request.POST
        todo.save()
        context = {
            "todo": todo,
            "from_complate_template": False
        }
        return render(request,'todo/show_todo.html',context)