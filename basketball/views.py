from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse

from .models import City, Player 

# Create your views here.
def index(request):
    city_list = City.objects.all()
    context = { 'city_list': city_list }
    return render(request, 'basketball/a.html', context)

def search_player(request):
    if request.method == 'POST':
        player_name = request.POST.get('NBA_search', None)
        if player_name == '':
            player_list = None
        else:
            player_list = Player.objects.filter(name__icontains=player_name)
            if len(player_list) == 0:
                player_list = None
        context = { 'player_list': player_list }
    return render(request, 'basketball/a.html', context)
