from django.shortcuts import render ,redirect ,get_object_or_404
from .models import *
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .filters import Todo_Filter
from user_auth.models import UserProfile

def home(request) :

    context = {
        'nav_home' : True,
    }
    return render(request, 'todo/index.html',context)



@login_required(login_url='login_user')
def todo_not_done(request) :
    todos = Todo.objects.filter(user=request.user, date_completed__isnull=True)
    todo_filter = Todo_Filter(request.POST, queryset=todos)
    empty_search = False
    get_by_search = False
    if request.method == "POST" :
        get_by_search = True
        if todo_filter.qs.__len__() == 0 :
            empty_search = True
    todos = todo_filter.qs

    context = {
        'todos' : todos,
        'todo_filter' : todo_filter,
        'empty_search' : empty_search,
        'get_by_search' : get_by_search,
    }

    return render(request,'todo/todo_not_done.html',context)


@login_required(login_url='login_user')
def todo_done(request) :
    todos = Todo.objects.filter(user=request.user, date_completed__isnull=False)

    context = {
        'todos': todos,
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
        return redirect('show_todo',todo.id)




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
        context = {
        }
        return render(request,'todo/clear.html',context)
    elif request.method == "POST" :
        if "COM" in request.POST :
            todo = Todo.objects.filter(user=request.user, date_completed__isnull=False)
            if todo.__len__() == 0 :
                messages.info(request, 'there is nothing to clear')
            else :
                todo.delete()
                messages.info(request, 'Delete all the TODO\'s done Successfully')
            return redirect('todo_done')
        else :
            todo = Todo.objects.filter(user=request.user, date_completed__isnull=True)
            if todo.__len__() == 0:
                messages.info(request, 'there is nothing to clear')
            else:
                todo.delete()
                messages.info(request, 'Delete all the TODO\'s done Successfully')
            return redirect('todo_not_done')



@login_required(login_url='login_user')
def account_settings(request) :
    user = get_object_or_404(User,pk=request.user.id)
    user_profile = get_object_or_404(UserProfile,user=request.user)
    context = {
        'user_' : user,
        'user_profile' : user_profile,
    }
    return render(request,'todo/account_settings.html',context)