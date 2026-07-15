from django.urls import path
from .import views

urlpatterns = [
    path("create-cinema/", views.create_cinema, name="create_cinema"),
    path('update-cinema/<str:pk>', views.update_cinema, name='update_cinema'),
    path('list-cinema/', views.list_cinema, name='list_cinema'),
    path('delete-cinema/<str:pk>', views.delete_cinema, name='delete_cinema'),

]
