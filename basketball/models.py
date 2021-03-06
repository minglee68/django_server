# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class City(models.Model):
    cityid = models.AutoField(db_column='CityId', primary_key=True)  # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=128)  # Field name made lowercase.

    class Meta:
        db_table = 'city'


class Game(models.Model):
    gameid = models.AutoField(db_column='GameId', primary_key=True)  # Field name made lowercase.
    homeid = models.ForeignKey('Team', models.DO_NOTHING, db_column='HomeId')  # Field name made lowercase.
    awayid = models.ForeignKey('Team', models.DO_NOTHING, db_column='AwayId', related_name='+')  # Field name made lowercase.
    seasonid = models.ForeignKey('Season', models.DO_NOTHING, db_column='SeasonId')  # Field name made lowercase.
    date = models.DateField(db_column='Date')  # Field name made lowercase.

    class Meta:
        db_table = 'game'


class Gameplayerstat(models.Model):
    gameplayerstatid = models.AutoField(db_column='GamePlayerStatId', primary_key=True)  # Field name made lowercase.
    playerid = models.ForeignKey('Player', models.DO_NOTHING, db_column='PlayerId')  # Field name made lowercase.
    gameid = models.ForeignKey(Game, models.DO_NOTHING, db_column='GameId')  # Field name made lowercase.
    mp = models.IntegerField(db_column='MP')  # Field name made lowercase.
    fg = models.IntegerField(db_column='FG')  # Field name made lowercase.
    fga = models.IntegerField(db_column='FGA')  # Field name made lowercase.
    number_3p = models.IntegerField(db_column='3P')  # Field name made lowercase. Field renamed because it wasn't a valid Python identifier.
    number_3pa = models.IntegerField(db_column='3PA')  # Field name made lowercase. Field renamed because it wasn't a valid Python identifier.
    ft = models.IntegerField(db_column='FT')  # Field name made lowercase.
    fta = models.IntegerField(db_column='FTA')  # Field name made lowercase.
    orb = models.IntegerField(db_column='ORB')  # Field name made lowercase.
    drb = models.IntegerField(db_column='DRB')  # Field name made lowercase.
    ast = models.IntegerField(db_column='AST')  # Field name made lowercase.
    pf = models.IntegerField(db_column='PF')  # Field name made lowercase.
    st = models.IntegerField(db_column='ST')  # Field name made lowercase.
    tov = models.IntegerField(db_column='TOV')  # Field name made lowercase.
    bs = models.IntegerField(db_column='BS')  # Field name made lowercase.
    pts = models.IntegerField(db_column='PTS')  # Field name made lowercase.

    class Meta:
        db_table = 'gameplayerstat'


class League(models.Model):
    leagueid = models.AutoField(db_column='LeagueId', primary_key=True)  # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=128, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        db_table = 'league'


class Player(models.Model):
    playerid = models.AutoField(db_column='PlayerId', primary_key=True)  # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=128)  # Field name made lowercase.
    height = models.IntegerField(db_column='Height')  # Field name made lowercase.
    weight = models.IntegerField(db_column='Weight')  # Field name made lowercase.
    age = models.IntegerField(db_column='Age')  # Field name made lowercase.
    imageurl = models.CharField(db_column='ImageURL', max_length=2083)

    class Meta:
        db_table = 'player'


class Playerposition(models.Model):
    playerpositionid = models.AutoField(db_column='PlayerPositionId', primary_key=True)  # Field name made lowercase.
    positionid = models.ForeignKey('Position', models.DO_NOTHING, db_column='PositionId')  # Field name made lowercase.
    playerid = models.ForeignKey(Player, models.DO_NOTHING, db_column='PlayerId')  # Field name made lowercase.

    class Meta:
        db_table = 'playerposition'


class Playerteam(models.Model):
    playerteamid = models.AutoField(db_column='PlayerTeamId', primary_key=True)  # Field name made lowercase.
    seasonid = models.ForeignKey('Season', models.DO_NOTHING, db_column='SeasonId')  # Field name made lowercase.
    teamid = models.ForeignKey('Team', models.DO_NOTHING, db_column='TeamId')  # Field name made lowercase.
    playerid = models.ForeignKey(Player, models.DO_NOTHING, db_column='PlayerId')  # Field name made lowercase.

    class Meta:
        db_table = 'playerteam'


class Position(models.Model):
    positionid = models.AutoField(db_column='PositionId', primary_key=True)  # Field name made lowercase.
    type = models.CharField(db_column='Type', max_length=128)  # Field name made lowercase.

    class Meta:
        db_table = 'position'


class Quarter(models.Model):
    quarterid = models.AutoField(db_column='QuarterId', primary_key=True)  # Field name made lowercase.
    gameid = models.ForeignKey(Game, models.DO_NOTHING, db_column='GameId')  # Field name made lowercase.
    teamid = models.ForeignKey('Team', models.DO_NOTHING, db_column='TeamId')  # Field name made lowercase.
    quarternumber = models.IntegerField(db_column='QuarterNumber')  # Field name made lowercase.
    score = models.IntegerField(db_column='Score')  # Field name made lowercase.

    class Meta:
        db_table = 'quarter'


class Season(models.Model):
    seasonid = models.AutoField(db_column='SeasonId', primary_key=True)  # Field name made lowercase.
    year = models.CharField(db_column='Year', max_length=5)  # Field name made lowercase.
    type = models.CharField(db_column='Type', max_length=128)  # Field name made lowercase.

    class Meta:
        db_table = 'season'


class Team(models.Model):
    teamid = models.AutoField(db_column='TeamId', primary_key=True)  # Field name made lowercase.
    name = models.CharField(db_column='Name', unique=True, max_length=128)  # Field name made lowercase.
    homestadium = models.CharField(db_column='HomeStadium', max_length=128, blank=True, null=True)  # Field name made lowercase.
    cityid = models.ForeignKey(City, models.DO_NOTHING, db_column='CityId', blank=True, null=True)  # Field name made lowercase.
    leagueid = models.ForeignKey(League, models.DO_NOTHING, db_column='LeagueId', blank=True, null=True)  # Field name made lowercase.
    imageurl = models.CharField(db_column='ImageURL', max_length=2083)

    class Meta:
        db_table = 'team'

class Player_stat(models.Model):

    year = models.CharField(db_column='Year', max_length=5)
    type = models.CharField(db_column='Type', max_length=128)
    player_name = models.CharField(db_column='Player_Name', max_length=128)
    player_imageurl = models.CharField(db_column='Player_ImageURL', max_length=2083)
    team_name = models.CharField(db_column='Team_Name', max_length=128)
    height = models.IntegerField(db_column='Height')
    weight = models.IntegerField(db_column='Weight')
    age = models.IntegerField(db_column='Age')
    mp = models.DecimalField(db_column='MP', decimal_places=0, max_digits=32)
    fg = models.DecimalField(db_column='FG', decimal_places=0, max_digits=32)
    fga = models.DecimalField(db_column='FGA', decimal_places=0, max_digits=32)
    fgp = models.DecimalField(db_column='FGP', decimal_places=4, max_digits=39)
    number_3p = models.DecimalField(db_column='3P', decimal_places=0, max_digits=32)
    number_3pa = models.DecimalField(db_column='3PA', decimal_places=0, max_digits=32)
    number_3pp = models.DecimalField(db_column='3PP', decimal_places=4, max_digits=39)
    ft = models.DecimalField(db_column='FT', decimal_places=0, max_digits=32)
    fta = models.DecimalField(db_column='FTA', decimal_places=0, max_digits=32)
    ftp = models.DecimalField(db_column='FTP', decimal_places=4, max_digits=39)
    orb = models.DecimalField(db_column='ORB', decimal_places=0, max_digits=32)
    drb = models.DecimalField(db_column='DRB', decimal_places=0, max_digits=32)
    ast = models.DecimalField(db_column='AST', decimal_places=0, max_digits=32)
    pf = models.DecimalField(db_column='PF', decimal_places=0, max_digits=32)
    st = models.DecimalField(db_column='ST', decimal_places=0, max_digits=32)
    tov = models.DecimalField(db_column='TOV', decimal_places=0, max_digits=32)
    bs = models.DecimalField(db_column='BS', decimal_places=0, max_digits=32)
    pts = models.DecimalField(db_column='PTS', decimal_places=0, max_digits=32)

    class Meta:
        managed = False
        db_table = 'player_stat'

class Team_stat(models.Model):

    year = models.CharField(db_column='Year', max_length=5)
    team_name = models.CharField(db_column='Team_Name', max_length=128)
    league_name = models.CharField(db_column='League_Name', max_length=128)
    fg = models.DecimalField(db_column='FG', decimal_places=0, max_digits=54)
    fga = models.DecimalField(db_column='FGA', decimal_places=0, max_digits=54)
    fgp = models.DecimalField(db_column='FGP', decimal_places=4, max_digits=61)
    number_3p = models.DecimalField(db_column='3P', decimal_places=0, max_digits=54)
    number_3pa = models.DecimalField(db_column='3PA', decimal_places=0, max_digits=54)
    number_3pp = models.DecimalField(db_column='3PP', decimal_places=4, max_digits=61)
    ft = models.DecimalField(db_column='FT', decimal_places=0, max_digits=54)
    fta = models.DecimalField(db_column='FTA', decimal_places=0, max_digits=54)
    ftp = models.DecimalField(db_column='FTP', decimal_places=4, max_digits=61)
    orb = models.DecimalField(db_column='ORB', decimal_places=0, max_digits=54)
    drb = models.DecimalField(db_column='DRB', decimal_places=0, max_digits=54)
    ast = models.DecimalField(db_column='AST', decimal_places=0, max_digits=54)
    pf = models.DecimalField(db_column='PF', decimal_places=0, max_digits=54)
    st = models.DecimalField(db_column='ST', decimal_places=0, max_digits=54)
    tov = models.DecimalField(db_column='TOV', decimal_places=0, max_digits=54)
    bs = models.DecimalField(db_column='BS', decimal_places=0, max_digits=54)

    class Meta:
        managed = False
        db_table = 'team_stat'

class League_stat(models.Model):

    year = models.CharField(db_column='Year', max_length=5)
    league_name = models.CharField(db_column='League_Name', max_length=128)
    score = models.DecimalField(db_column='Score', decimal_places=4, max_digits=58)
    fg = models.DecimalField(db_column='FG', decimal_places=4, max_digits=58)
    fga = models.DecimalField(db_column='FGA', decimal_places=4, max_digits=58)
    fgp = models.DecimalField(db_column='FGP', decimal_places=8, max_digits=65)
    number_3p = models.DecimalField(db_column='3P', decimal_places=4, max_digits=58)
    number_3pa = models.DecimalField(db_column='3PA', decimal_places=4, max_digits=58)
    number_3pp = models.DecimalField(db_column='3PP', decimal_places=8, max_digits=65)
    ft = models.DecimalField(db_column='FT', decimal_places=4, max_digits=58)
    fta = models.DecimalField(db_column='FTA', decimal_places=4, max_digits=58)
    ftp = models.DecimalField(db_column='FTP', decimal_places=8, max_digits=65)
    orb = models.DecimalField(db_column='ORB', decimal_places=4, max_digits=58)
    drb = models.DecimalField(db_column='DRB', decimal_places=4, max_digits=58)
    ast = models.DecimalField(db_column='AST', decimal_places=4, max_digits=58)
    pf = models.DecimalField(db_column='PF', decimal_places=4, max_digits=58)
    st = models.DecimalField(db_column='ST', decimal_places=4, max_digits=58)
    tov = models.DecimalField(db_column='TOV', decimal_places=4, max_digits=58)
    bs = models.DecimalField(db_column='BS', decimal_places=4, max_digits=58)

    class Meta:
        managed = False
        db_table = 'league_stat'

class League_position_stat(models.Model):

    year = models.CharField(db_column='Year', max_length=5)
    league_name = models.CharField(db_column='League_Name', max_length=128)
    position_type = models.CharField(db_column='Position_Type', max_length=128)
    score = models.DecimalField(db_column='Score', decimal_places=4, max_digits=58)
    fg = models.DecimalField(db_column='FG', decimal_places=4, max_digits=58)
    fga = models.DecimalField(db_column='FGA', decimal_places=4, max_digits=58)
    fgp = models.DecimalField(db_column='FGP', decimal_places=8, max_digits=65)
    number_3p = models.DecimalField(db_column='3P', decimal_places=4, max_digits=58)
    number_3pa = models.DecimalField(db_column='3PA', decimal_places=4, max_digits=58)
    number_3pp = models.DecimalField(db_column='3PP', decimal_places=8, max_digits=65)
    ft = models.DecimalField(db_column='FT', decimal_places=4, max_digits=58)
    fta = models.DecimalField(db_column='FTA', decimal_places=4, max_digits=58)
    ftp = models.DecimalField(db_column='FTP', decimal_places=8, max_digits=65)
    orb = models.DecimalField(db_column='ORB', decimal_places=4, max_digits=58)
    drb = models.DecimalField(db_column='DRB', decimal_places=4, max_digits=58)
    ast = models.DecimalField(db_column='AST', decimal_places=4, max_digits=58)
    pf = models.DecimalField(db_column='PF', decimal_places=4, max_digits=58)
    st = models.DecimalField(db_column='ST', decimal_places=4, max_digits=58)
    tov = models.DecimalField(db_column='TOV', decimal_places=4, max_digits=58)
    bs = models.DecimalField(db_column='BS', decimal_places=4, max_digits=58)

    class Meta:
        managed = False
        db_table = 'league_position_stat'

'''
class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'
'''

