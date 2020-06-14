from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='crawling'),
	path('players', views.players, name='crawl_players'),
]
