from django.shortcuts import render ,redirect ,get_object_or_404
from .models import *
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.translation import gettext as _


def home(request) :
    return render(request,'todo/layouts/base-todo.html')



@login_required(login_url='login_user')
def todo_not_done(request) :
    todos = Todo.objects.filter(user=request.user, date_completed__isnull=True)
    all_clear = False
    if todos.__len__() == 0:
        all_clear = True
    context = {
        'todos' : todos,
        'all_clear' : all_clear,
    }
    return render(request,'todo/todo_not_done.html',context)


@login_required(login_url='login_user')
def todo_done(request) :
    todos = Todo.objects.filter(user=request.user, date_completed__isnull=False)
    all_clear = False
    if todos.__len__() == 0:
        all_clear = True
    context = {
        'todos': todos,
        'all_clear': all_clear,
    }
    return render(request, 'todo/todo-done.html',context)



@login_required(login_url='login_user')
def add_todo(request) :
    if request.method == "GET" :
        return render(request,'todo/add-todo.html')
    else :
        title = request.POST['title']
        description = request.POST['description']
        if request.POST["is_important"] == "YES":
            is_important = True
        elif request.POST["is_important"] == "NO":
            is_important = False
        if title == "" :
            messages.info(request," please add a title")
            context = {
                'description' : description,
                'is_important' : is_important,
            }
            return render(request,'todo/add-todo.html',context)
        else:
            todo = Todo.objects.create(title=title,
                                   description=description,
                                   is_important=is_important,
                                   user=request.user)
            todo.save()
            return redirect('todo_not_done')



@login_required(login_url='login_user')
def show_todo(request ,todo_id) :
    if request.method == "GET" :
        todo = get_object_or_404(Todo,pk =todo_id,user = request.user)
        context = {
            "todo" : todo,
        }
        return render(request,'todo/show_todo.html',context)



@login_required(login_url='login_user')
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
        if request.POST["is_important"] == "YES" :
            todo.is_important = True
        elif request.POST["is_important"] == "NO" :
            todo.is_important = False
        todo.save()
        context = {
            "todo": todo,
        }
        return render(request,'todo/show_todo.html',context)




@login_required(login_url='login_user')
def delete_todo(request, todo_id):
    todo = get_object_or_404(Todo, pk=todo_id, user=request.user)
    if request.method == "GET" :
        context = {
            'todo' : todo,
        }
        return render(request,'todo/delete_todo.html',context)
    elif request.method == 'POST':
        todo.delete()
        if todo.date_completed is not None :
            return redirect('todo_done')
        else :
            return redirect('todo_not_done')



@login_required(login_url='login_user')
def complate_todo(request,todo_id) :
    todo = get_object_or_404(Todo, pk=todo_id, user=request.user)
    if request.method == "POST" :
        if todo.date_completed is not  None :
            todo.date_completed = None
            todo.save()
            return redirect('todo_not_done')
        else :
            todo.date_completed = timezone.now()
            todo.save()
            return redirect('todo_done')



@login_required(login_url='login_user')
def clear_todo(request) :
    if request.method == "GET" :
        return render(request,'todo/clear.html')
    elif request.method == "POST" :
        if "COM" in request.POST :
            todo = Todo.objects.filter(user=request.user, date_completed__isnull=False)
            if todo.__len__() == 0 :
                messages.info(request, 'there is nothing to clear')
            else :
                todo.delete()
            return render(request,'todo/todo-done.html')
        else :
            todo = Todo.objects.filter(user=request.user, date_completed__isnull=True)
            if todo.__len__() == 0:
                messages.info(request, 'there is nothing to clear')
            else:
                todo.delete()
            return render(request, 'todo/todo_not_done.html')

