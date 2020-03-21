from django.shortcuts import render


def home(request) :
    return render(request,'todo/layouts/base-todo.html')