import json

from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, JsonResponse

from .models import City, Player 

def check_player_name(name):
    if name == '' or name == None:
        player_list = None
    else:
        player_list = Player.objects.filter(name__icontains=name)
        if len(player_list) == 0:
            player_list = None
    return player_list

# Create your views here.
def index(request):
    city_list = City.objects.all()
    context = { 'city_list': city_list }
    return render(request, 'basketball/b.html', context)

def search_player(request):
    if request.method == 'POST':
        player_name_1 = request.POST.get('NBA_search', None)
        player_name_2 = request.POST.get('KBL_search', None)

        context = { 'player_name_1': player_name_1, 'player_name_2': player_name_2 }

        context['player_list_1'] = check_player_name(player_name_1)
        context['player_list_2'] = check_player_name(player_name_2)
    else:
        context = {}
    return render(request, 'basketball/a.html', context)

def get_player_list(request):
    player_name = request.GET.get('player_name', None)
    player_list = check_player_name(player_name)
    if player_list != None:
        player_list = list(player_list.values())
    # return JsonResponse({'data': player_list})
    return JsonResponse(json.dumps(player_list, ensure_ascii=False), safe=False)
