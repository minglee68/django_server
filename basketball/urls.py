from django.urls import path

from . import views

app_name = 'basketball'
urlpatterns = [
    path('', views.index, name='index'),
    path('search_player/', views.search_player, name='search_player'),
    path('get_player_list/', views.get_player_list, name='get_player_list'),
    path('crawl_player/', views.crawl_player, name='crawl_player'),
    path('crawl_game_player_stat/', views.crawl_game_player_stat, name='crawl_game_layer_stat'),
]
