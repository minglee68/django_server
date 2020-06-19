import json
import datetime

from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, JsonResponse

from .crawl import crawl_players, crawl_gamePlayerStat
from .models import City, Player, Position, Player, Playerposition, Season, Game, Gameplayerstat, Playerteam, Team


IS_CRAWLING = False		# Read-only!!

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

def get_player_stats(request):
    labels = ['MP', 'FG', 'FGA', '3P', '3PA', 'FT', 'FTA', 'ORB', 'DRB', 'AST', 'PF', 'ST', 'TOV', 'BS', 'PTS']
    stats = [0,]
    player_name = request.GET.get('player_name', None)
    player_list = check_player_name(player_name)
    playerid = player_list[0].playerid
    try:
        playerstats = Gameplayerstat.objects.filter(playerid=playerid)
        stats = [
            0,#playerstats[0].mp,
            playerstats[0].fg,
            playerstats[0].fga,
            playerstats[0].number_3p,
            playerstats[0].number_3pa,
            playerstats[0].ft,
            playerstats[0].fta,
            playerstats[0].orb,
            playerstats[0].drb,
            playerstats[0].ast,
            playerstats[0].pf,
            playerstats[0].st,
            playerstats[0].tov,
            playerstats[0].bs,
            playerstats[0].pts
        ]
    except:
        print('no data');

    context = {'chart_labels':labels, 'chart_data':stats}

    return JsonResponse(context)

def crawl_player(request):
    global IS_CRAWLING
    if IS_CRAWLING:
        return None

    IS_CRAWLING = True
    player_list, error_list = crawl_players()
    for player in player_list:
        try:
            player_object = Player.objects.get(name=player['name'])
        except Player.DoesNotExist:
            continue
        player_object.imageurl = player['img']
        player_object.save()

    IS_CRAWLING = False
    return None

def crawl_game_player_stat(request):
    global IS_CRAWLING
    if IS_CRAWLING:
        return None

    IS_CRAWLING = True
    game_data_list = crawl_gamePlayerStat()
    for game in game_data_list:
        year = int(game['date'][2:4])
        month = int(game['date'][4:6])
        day = int(game['date'][6:])
        if month > 8:
            season = str(year) + str(year + 1)
        else:
            season = str(year - 1) + str(year)
        try:
            season_object = Season.objects.get(year=season)
        except Season.DoesNotExist:
            season_object = Season(year=season, type='NBA')
            season_object.save()
        
        date = datetime.date(int(game['date'][:4]), month, day)
        home_name = game['home']['team']
        away_name = game['away']['team']
        if home_name == 'Charlotte Bobcats':
            home_name = 'Charlotte Hornets'
        if away_name == 'Charlotte Bobcats':
            away_name = 'Charlotte Hornets'
        home_object = Team.objects.get(name=home_name)
        away_object = Team.objects.get(name=away_name)
        game_object = Game(homeid=home_object, awayid=away_object, seasonid=season_object, date=date)
        game_object.save()
        
        for player in game['home']['players']:
            if (len(player) < 10):
                continue
            try:
                player_object = Player.objects.get(name=player['name'])
            except Player.DoesNotExist:
                continue
            try:
                playerteam_object = Playerteam.objects.get(seasonid=season_object, teamid=home_object, playerid=player_object)
            except Playerteam.DoesNotExist:
                playerteam_object = Playerteam(seasonid=season_object, teamid=home_object, playerid=player_object)
                playerteam_object.save()
            try:
                gameplayerstat_object = Gameplayerstat.objects.get(gameid=game_object, playerid=player_object)
            except:
                mp = player['mp'].split(':')
                second = int(mp[0]) * 60 + int(mp[1])

                gameplayerstat_object = Gameplayerstat(playerid=player_object, gameid=game_object, mp=str(second), fg=player['fg'], fga=player['fga'], number_3p=player['fg3'], number_3pa=player['fg3a'], ft=player['ft'], fta=player['fta'], orb=player['orb'], drb=player['drb'], ast=player['ast'], pf=player['pf'], st=player['stl'], tov=player['tov'], bs=player['blk'], pts=player['pts'])
                gameplayerstat_object.save()

    IS_CRAWLING = False
    return render(request, 'basketball/b.html')
