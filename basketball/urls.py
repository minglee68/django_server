from django.urls import path

from . import views

app_name = 'basketball'
urlpatterns = [
    path('', views.index, name='index'),
    path('players/', views.players, name='players'),
    path('teams/', views.teams, name='teams'),
    path('leagues/', views.leagues, name='leagues'),
    path('search_player/', views.search_player, name='search_player'),
    path('get_player_list/', views.get_player_list, name='get_player_list'),
    path('get_player_stats/', views.get_player_stats, name='get_player_stats'),
    # path('crawl_nba_player/', views.crawl_nba_player, name='crawl_nba_player'),
    # path('crawl_nba_game_player_stat/', views.crawl_nba_game_player_stat, name='crawl_nba_game_layer_stat'),
    # path('crawl_kbl_player/', views.crawl_kbl_player, name='crawl_kbl_player'),
    # path('crawl_kbl_game_player_stat/', views.crawl_kbl_game_player_stat, name='crawl_kbl_game_layer_stat'),
]
