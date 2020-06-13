from django.urls import path

from . import views

app_name = 'basketball'
urlpatterns = [
    path('', views.index, name='index'),
    path('search_nba_player/', views.search_player, name='search_nba_player')
]
