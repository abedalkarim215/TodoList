from django.contrib import admin
from django.urls import path , include
from todo.views import home

urlpatterns = [
    path('admin/', admin.site.urls),

    path('' , home ,name = 'home'),
    path('todo/', include('todo.urls')),
    path('user/', include('user_auth.urls')),
]


handler404 = 'user_auth.views.error_404'