from django.urls import path
from . import views
urlpatterns = [
    path('', views.index, name='index'),
    path('add/', views.add_student, name='add'),
    path('update/<int:id>/', views.update_data, name='update'),
    path('delete/<int:id>/', views.delete_data, name='delete'),
    path('set-name/', views.set_name, name='set_name'),
    path('lobby/', views.chat_lobby, name='chat_lobby'),
    path('chat/<str:receiver_name>/', views.personal_chat, name='personal_chat'),
    path('search-student/', views.search_student, name='search_student'),


]
