from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('', views.dashboard_view, name='dashboard'),
    path('board//', views.board_detail_view, name='board_detail'),
    path('board//delete/', views.delete_board_view, name='delete_board'),
    path('board//task/create/', views.create_task_view, name='create_task'),
    path('task//edit/', views.edit_task_view, name='edit_task'),
    path('task//delete/', views.delete_task_view, name='delete_task'),
]