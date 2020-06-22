import json
import datetime

from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.forms.models import model_to_dict
from django.db.models import Q

from .crawl import crawl_NBA_players, crawl_NBA_gamePlayerStat, crawl_NBA_quarter_gamePlayerStat, crawl_KBL_players, crawl_KBL_gamePlayerStat, crawl_KBL_quarter_gamePlayerStat
from .models import City, Player, Position, Player, Playerposition, Season, Game, Gameplayerstat, Playerteam, Team, Player_stat, Quarter, Team_stat, League_stat


IS_CRAWLING = False		# Read-only!!

def check_player_name(name):
    if name == '' or name == None:
        player_list = None
    else:
        player_list = Player.objects.filter(name__icontains=name)
        if len(player_list) == 0:
            player_list = None
    return player_list

def check_team_name(name):
    if name == '' or name == None:
        team_list = None
    else:
        team_list = Team.objects.filter(name__icontains=name)
        if len(team_list) == 0:
            team_list = None
    return team_list

def check_kbl_team_name(name):
    if name.find('KGC') != -1:
        team_id = 31
    elif name.find('KT') != -1:
        team_id = 32
    elif name.find('LG') != -1:
        team_id = 33
    elif name.find('KCC') != -1:
        team_id = 36
    elif name.find('SK') != -1:
        team_id = 38
    elif name.find('DB') != -1 or name == '원주동부':
        team_id = 40
    elif name == '서울삼성':
        team_id = 37
    elif name == '울산현대모비스' or name == '울산모비스':
        team_id = 39
    elif name == '인천전자랜드':
        team_id = 35
    elif name == '고양오리온' or name == '고양오리온스':
        team_id = 34
    else:
        return None

    return team_id

# Create your views here.
def index(request):
    return HttpResponseRedirect(reverse('basketball:players'))

def players(request):
    return render(request, 'basketball/players.html')

def teams(request):
    return render(request, 'basketball/teams.html')

def leagues(request):
    return render(request, 'basketball/leagues.html')

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

def get_team_list(request):
    team_name = request.GET.get('team_name', None)
    team_list = check_team_name(team_name)
    if team_list != None:
        team_list = list(team_list.values())
    # return JsonResponse({'data': player_list})
    return JsonResponse(json.dumps(team_list, ensure_ascii=False), safe=False)

def get_player_stats(request):
    labels = ['MP', 'FG', 'FGA', 'FGP', '3P', '3PA', '3PP', 'FT', 'FTA', 'FTP', 'ORB', 'DRB', 'AST', 'PF', 'ST', 'TOV', 'BS', 'PTS']
    stats = [0,]
    player_name = request.GET.get('player_name', None)
    player_list = check_player_name(player_name)
    name = player_list[0].name
    gameplays = {}
    '''
    try:
        gameplayerstats = Gameplayerstat.objects.filter(playerid=player_list[0])
        for game in gameplayerstats:
            if game.gameid.seasonid.year in gameplays:
                gameplays[game.gameid.seasonid.year] += 1
            else:
                gameplays[game.gameid.seasonid.year] = 1
    except Gameplayerstat.DoesNotExist:
        print('game_player_stat no data')
    '''

    try:
        playerstats = Player_stat.objects.filter(player_name=name)
        stats = [0 for _ in range(18)]
        for playerstat in playerstats:
            stats[0] += 0 #int(playerstat.mp)
            stats[1] += int(playerstat.fg)
            stats[2] += int(playerstat.fga)
            stats[3] += int(playerstat.fgp)
            stats[4] += int(playerstat.number_3p)
            stats[5] += int(playerstat.number_3pa)
            stats[6] += int(playerstat.number_3pp)
            stats[7] += int(playerstat.ft)
            stats[8] += int(playerstat.fta)
            stats[9] += int(playerstat.ftp)
            stats[10] += int(playerstat.orb)
            stats[11] += int(playerstat.drb)
            stats[12] += int(playerstat.ast)
            stats[13] += int(playerstat.pf)
            stats[14] += int(playerstat.st)
            stats[15] += int(playerstat.tov)
            stats[16] += int(playerstat.bs)
            stats[17] += int(playerstat.pts)
        for i in range(18):
            stats[i] = stats[i] / len(playerstats)
    except Player_stat.DoesNotExist:
        print('player_stat_no data');

    context = {'chart_labels':labels, 'chart_data':stats}

    return JsonResponse(context)

def get_team_stats(request):
    labels = ['FG', 'FGA', 'FGP', '3P', '3PA', '3PP', 'FT', 'FTA', 'FTP', 'ORB', 'DRB', 'AST', 'PF', 'ST', 'TOV', 'BS']
    stats = [0,]
    team_name = request.GET.get('team_name', None)
    team_object = Team.objects.get(name=team_name)
    try:
        teamstats = Team_stat.objects.filter(team_name=team_name)
        stats = [0 for _ in range(16)]
        for teamstat in teamstats:
            season_object = Season.objects.get(year=teamstat.year, type=teamstat.league_name[:3])
            teamgames = Game.objects.filter(Q(seasonid=season_object)&(Q(homeid=team_object)|Q(awayid=team_object)))
            stats[0] += int(teamstat.fg / len(teamgames))
            stats[1] += int(teamstat.fga / len(teamgames))
            stats[2] += int(teamstat.fgp)
            stats[3] += int(teamstat.number_3p / len(teamgames))
            stats[4] += int(teamstat.number_3pa / len(teamgames))
            stats[5] += int(teamstat.number_3pp)
            stats[6] += int(teamstat.ft / len(teamgames))
            stats[7] += int(teamstat.fta / len(teamgames))
            stats[8] += int(teamstat.ftp)
            stats[9] += int(teamstat.orb / len(teamgames))
            stats[10] += int(teamstat.drb / len(teamgames))
            stats[11] += int(teamstat.ast / len(teamgames))
            stats[12] += int(teamstat.pf / len(teamgames))
            stats[13] += int(teamstat.st / len(teamgames))
            stats[14] += int(teamstat.tov / len(teamgames))
            stats[15] += int(teamstat.bs / len(teamgames))
        for i in range(16):
            stats[i] = stats[i] / len(teamstats)
    except Team_stat.DoesNotExist:
        print('team_stat_no data');

    context = {'chart_labels':labels, 'chart_data':stats}

    return JsonResponse(context)

def get_player_information(request):
    player_name = request.GET.get('player_name', None)
    player_obj = Player.objects.get(name=player_name)
    player_position_list = Playerposition.objects.filter(playerid=player_obj)
    try:
        player_team_obj = Playerteam.objects.filter(playerid=player_obj).order_by('seasonid').last()
        player_team = player_team_obj.teamid.name
    except:
        player_team = ""
        print('None odject')

    player_position = []
    for i in player_position_list:
        player_position.append(i.positionid.type)
    player_position = ', '.join(player_position)
    player_obj = model_to_dict(player_obj)

    player_obj['position'] = player_position
    player_obj['team'] = player_team

    return JsonResponse(player_obj)

def get_team_player_list(request):
    team_name = request.GET.get('team_name', None)
    team_obj = Team.objects.get(name=team_name)
    player_team_list = Playerteam.objects.filter(Q(teamid=team_obj)&(Q(seasonid=42)|Q(seasonid=47)))
    team_player_list = [team_obj.imageurl,]
    for list in player_team_list:
        pname = Player.objects.get(playerid=list.playerid.playerid).name
        team_player_list.append(pname)
    # return JsonResponse({'data': player_list})
    return JsonResponse(json.dumps(team_player_list, ensure_ascii=False), safe=False)

def crawl_nba_player(request):
    global IS_CRAWLING
    if IS_CRAWLING:
        return None

    IS_CRAWLING = True
    player_list, error_list = crawl_NBA_players()
    for player in player_list:
        try:
            player_object = Player.objects.get(name=player['name'])
        except Player.DoesNotExist:
            player_object = Player(name=player['name'], height=player['height'], weight=player['weight'], age=player['age'], imageurl=player['img'])
            player_object.save()
        for position in player['position']:
            try:
                position_object = Position.objects.get(type=position)
            except Position.DoesNotExist:
                position_object = Position(type=position)
                position_object.save()
                
            try:
                player_position_object = Playerposition.objects.get(playerid=player_object, positionid=position_object)
            except Playerposition.DoesNotExist:
                player_position_object = Playerposition(playerid=player_object, positionid=position_object)
                player_position_object.save()

    IS_CRAWLING = False
    return render(request, 'basketball/players.html')

def crawl_nba_game_player_stat(request):
    global IS_CRAWLING
    if IS_CRAWLING:
        return None

    IS_CRAWLING = True
    # game_data_list = crawl_NBA_quarter_gamePlayerStat()
    with open('nba_data.txt', 'r') as json_file:
        game_data_list = json.load(json_file)
    '''

    with open('nba_data.txt', 'w') as outfile:
        json.dump(game_data_list, outfile)
    '''
    for game in game_data_list:
        year = int(game['date'][2:4])
        month = int(game['date'][4:6])
        day = int(game['date'][6:])
        if month > 8:
            season = str(year) + str(year + 1)
        else:
            season = str(year - 1) + str(year)
        try:
            season_object = Season.objects.get(year=season, type='NBA')
        except Season.DoesNotExist:
            continue
        
        date = datetime.date(int(game['date'][:4]), month, day)
        home_name = game['home']['team']
        away_name = game['away']['team']
        if home_name == 'Charlotte Bobcats':
            home_name = 'Charlotte Hornets'
        if away_name == 'Charlotte Bobcats':
            away_name = 'Charlotte Hornets'
        home_object = Team.objects.get(name=home_name)
        away_object = Team.objects.get(name=away_name)
        try:
            game_object = Game.objects.get(homeid=home_object, awayid=away_object, seasonid=season_object, date=date)
        except Game.DoesNotExist:
            continue
        for quarter in game['points']['home']:
            try:
                quarter_object = Quarter.objects.get(gameid=game_object, teamid=home_object, quarternumber=quarter[1])
            except Quarter.DoesNotExist:
                quarter_object = Quarter(gameid=game_object, teamid=home_object, quarternumber=quarter[1], score=game['points']['home'][quarter])
                quarter_object.save()
        for quarter in game['points']['away']:
            try:
                quarter_object = Quarter.objects.get(gameid=game_object, teamid=away_object, quarternumber=quarter[1])
            except Quarter.DoesNotExist:
                quarter_object = Quarter(gameid=game_object, teamid=away_object, quarternumber=quarter[1], score=game['points']['away'][quarter])
                quarter_object.save()

        '''
        for player in game['away']['players']:
            if (len(player) < 10):
                continue
            try:
                player_object = Player.objects.get(name=player['name'])
            except Player.DoesNotExist:
                continue
            try:
                playerteam_object = Playerteam.objects.get(seasonid=season_object, teamid=away_object, playerid=player_object)
            except Playerteam.DoesNotExist:
                playerteam_object = Playerteam(seasonid=season_object, teamid=away_object, playerid=player_object)
                playerteam_object.save()
            try:
                gameplayerstat_object = Gameplayerstat.objects.get(gameid=game_object, playerid=player_object)
            except:
                mp = player['mp'].split(':')
                second = int(mp[0]) * 60 + int(mp[1])

                gameplayerstat_object = Gameplayerstat(playerid=player_object, gameid=game_object, mp=str(second), fg=player['fg'], fga=player['fga'], number_3p=player['fg3'], number_3pa=player['fg3a'], ft=player['ft'], fta=player['fta'], orb=player['orb'], drb=player['drb'], ast=player['ast'], pf=player['pf'], st=player['stl'], tov=player['tov'], bs=player['blk'], pts=player['pts'])
                gameplayerstat_object.save()
        '''


    IS_CRAWLING = False
    return render(request, 'basketball/players.html')

def crawl_kbl_player(request):
    global IS_CRAWLING
    if IS_CRAWLING:
        return None

    IS_CRAWLING = True
    player_list = crawl_KBL_players()
    with open('kbl_player_data.txt', 'w') as outfile:
        json.dump(player_list, outfile)
    '''
    for player in player_list:
        try:
            player_object = Player.objects.get(name=player['name'])
        except Player.DoesNotExist:
            player_object = Player(name=player['name'], height=player['height'], weight=0, age=player['age'], imageurl=player['img'])
            player_object.save()
        for position in player['position']:
            try:
                position_object = Position.objects.get(type=position)
            except Position.DoesNotExist:
                position_object = Position(type=position)
                position_object.save()
                
            try:
                player_position_object = Playerposition.objects.get(playerid=player_object, positionid=position_object)
            except Playerposition.DoesNotExist:
                player_position_object = Playerposition(playerid=player_object, positionid=position_object)
                player_position_object.save()
    '''
    IS_CRAWLING = False
    return render(request, 'basketball/players.html')

def crawl_kbl_game_player_stat(request):
    global IS_CRAWLING
    if IS_CRAWLING:
        return None

    IS_CRAWLING = True
    # game_data_list = crawl_KBL_gamePlayerStat()
    # game_data_list = crawl_KBL_quarter_gamePlayerStat()
    with open('kbl_data.txt', 'r') as json_file:
        game_data_list = json.load(json_file)

    '''
    with open('kbl_data.txt', 'w') as outfile:
        json.dump(game_data_list, outfile)
    '''
    for game in game_data_list:
        year = int(game['date'][2:4])
        month = int(game['date'][4:6])
        day = int(game['date'][6:])
        if month > 8:
            season = str(year) + str(year + 1)
        else:
            season = str(year - 1) + str(year)
        try:
            season_object = Season.objects.get(year=season, type='KBL')
        except Season.DoesNotExist:
            continue
            season_object = Season(year=season, type='KBL')
            season_object.save()
        
        date = datetime.date(int(game['date'][:4]), month, day)
        home_name = game['home']['team']
        away_name = game['away']['team']
        home_id = check_kbl_team_name(home_name)
        away_id = check_kbl_team_name(away_name)
        if home_id == None or away_id == None:
            continue

        home_object = Team.objects.get(teamid=home_id)
        away_object = Team.objects.get(teamid=away_id)
        try:
            game_object = Game.objects.get(homeid=home_object, awayid=away_object, seasonid=season_object, date=date)
        except Game.DoesNotExist:
            game_object = Game(homeid=home_object, awayid=away_object, seasonid=season_object, date=date)
            game_object.save()

        '''
        for quarter in game['points']['home']:
            try:
                quarter_object = Quarter.objects.get(gameid=game_object, teamid=home_object, quarternumber=quarter[1])
            except Quarter.DoesNotExist:
                quarter_object = Quarter(gameid=game_object, teamid=home_object, quarternumber=quarter[1], score=game['points']['home'][quarter])
                quarter_object.save()
        for quarter in game['points']['away']:
            try:
                quarter_object = Quarter.objects.get(gameid=game_object, teamid=away_object, quarternumber=quarter[1])
            except Quarter.DoesNotExist:
                quarter_object = Quarter(gameid=game_object, teamid=away_object, quarternumber=quarter[1], score=game['points']['away'][quarter])
                quarter_object.save()
        '''

        for team in ['home', 'away']:
            for player in game[team]['players']:
                if (len(player) < 10):
                    continue
                try:
                    player_object = Player.objects.get(name=player['name'])
                except Player.DoesNotExist:
                    continue
                if team == 'home':
                    team_object = home_object
                else:
                    team_object = away_object
                try:
                    playerteam_object = Playerteam.objects.get(seasonid=season_object, teamid=team_object, playerid=player_object)
                except Playerteam.DoesNotExist:
                    playerteam_object = Playerteam(seasonid=season_object, teamid=team_object, playerid=player_object)
                    playerteam_object.save()
                try:
                    gameplayerstat_object = Gameplayerstat.objects.get(gameid=game_object, playerid=player_object)
                except:
                    mp = player['mp'].split(':')
                    second = int(mp[0]) * 60 + int(mp[1])

                    gameplayerstat_object = Gameplayerstat(playerid=player_object, gameid=game_object, mp=str(second), fg=player['fg'], fga=player['fga'], number_3p=player['fg3'], number_3pa=player['fg3a'], ft=player['ft'], fta=player['fta'], orb=player['orb'], drb=player['drb'], ast=player['ast'], pf=player['pf'], st=player['stl'], tov=player['tov'], bs=player['blk'], pts=player['pts'])
                    gameplayerstat_object.save()

    IS_CRAWLING = False
    return render(request, 'basketball/players.html')
