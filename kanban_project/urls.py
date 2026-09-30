"""
URL configuration for kanban_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from boards import views

urlpatterns = [
    path('admin/', admin.site.urls),
    
    path('accounts/login/', LoginView.as_view(template_name='boards/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    
    path('register/', views.register_view, name='register'),
    path('', views.dashboard_view, name='dashboard'),
    
    path('board//', views.board_detail_view, name='board_detail'),
    path('board//delete/', views.delete_board_view, name='delete_board'),
    path('board//task/create/', views.create_task_view, name='create_task'),
    
    path('task//edit/', views.edit_task_view, name='edit_task'),
    path('task//delete/', views.delete_task_view, name='delete_task'),
]