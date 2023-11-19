from django.urls import path
from . import views

urlpatterns = [
    path('rooms/', views.room_list, name='room_list'),
    path('rooms/<str:id_room>/', views.room_detail, name='room_detail'),
    path('films/', views.film_list, name='film_list'),
    path('films/<str:id_film>/', views.film_detail, name='film_detail'),
    path('films/<str:id_film>/?<str:message>', views.film_detail, name='film_detail_mes'),
]
