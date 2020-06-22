# Generated by Django 3.0.7 on 2020-06-18 08:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='City',
            fields=[
                ('cityid', models.AutoField(db_column='CityId', primary_key=True, serialize=False)),
                ('name', models.CharField(db_column='Name', max_length=128)),
            ],
            options={
                'db_table': 'city',
            },
        ),
        migrations.CreateModel(
            name='Game',
            fields=[
                ('gameid', models.AutoField(db_column='GameId', primary_key=True, serialize=False)),
                ('date', models.DateField(db_column='Date')),
            ],
            options={
                'db_table': 'game',
            },
        ),
        migrations.CreateModel(
            name='League',
            fields=[
                ('leagueid', models.AutoField(db_column='LeagueId', primary_key=True, serialize=False)),
                ('name', models.CharField(blank=True, db_column='Name', max_length=128, null=True)),
            ],
            options={
                'db_table': 'league',
            },
        ),
        migrations.CreateModel(
            name='Player',
            fields=[
                ('playerid', models.AutoField(db_column='PlayerId', primary_key=True, serialize=False)),
                ('name', models.CharField(db_column='Name', max_length=128)),
                ('height', models.IntegerField(db_column='Height')),
                ('weight', models.IntegerField(db_column='Weight')),
                ('age', models.IntegerField(db_column='Age')),
                ('imageurl', models.CharField(db_column='ImageURL', max_length=2083)),
            ],
            options={
                'db_table': 'player',
            },
        ),
        migrations.CreateModel(
            name='Position',
            fields=[
                ('positionid', models.AutoField(db_column='PositionId', primary_key=True, serialize=False)),
                ('type', models.CharField(db_column='Type', max_length=128)),
            ],
            options={
                'db_table': 'position',
            },
        ),
        migrations.CreateModel(
            name='Season',
            fields=[
                ('seasonid', models.AutoField(db_column='SeasonId', primary_key=True, serialize=False)),
                ('year', models.CharField(db_column='Year', max_length=5)),
                ('type', models.CharField(db_column='Type', max_length=128)),
            ],
            options={
                'db_table': 'season',
            },
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('teamid', models.AutoField(db_column='TeamId', primary_key=True, serialize=False)),
                ('name', models.CharField(db_column='Name', max_length=128, unique=True)),
                ('homestadium', models.CharField(blank=True, db_column='HomeStadium', max_length=128, null=True)),
                ('cityid', models.ForeignKey(blank=True, db_column='CityId', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='basketball.City')),
                ('leagueid', models.ForeignKey(blank=True, db_column='LeagueId', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='basketball.League')),
                ('imageurl', models.CharField(db_column='ImageURL', max_length=2083)),
            ],
            options={
                'db_table': 'team',
            },
        ),
        migrations.CreateModel(
            name='Quarter',
            fields=[
                ('quarterid', models.AutoField(db_column='QuarterId', primary_key=True, serialize=False)),
                ('quarternumber', models.IntegerField(db_column='QuarterNumber')),
                ('score', models.IntegerField(db_column='Score')),
                ('gameid', models.ForeignKey(db_column='GameId', on_delete=django.db.models.deletion.DO_NOTHING, to='basketball.Game')),
                ('teamid', models.ForeignKey(db_column='TeamId', on_delete=django.db.models.deletion.DO_NOTHING, to='basketball.Team')),
            ],
            options={
                'db_table': 'quarter',
            },
        ),
        migrations.CreateModel(
            name='Playerteam',
            fields=[
                ('playerteamid', models.AutoField(db_column='PlayerTeamId', primary_key=True, serialize=False)),
                ('playerid', models.ForeignKey(db_column='PlayerId', on_delete=django.db.models.deletion.DO_NOTHING, to='basketball.Player')),
                ('seasonid', models.ForeignKey(db_column='SeasonId', on_delete=django.db.models.deletion.DO_NOTHING, to='basketball.Season')),
                ('teamid', models.ForeignKey(db_column='TeamId', on_delete=django.db.models.deletion.DO_NOTHING, to='basketball.Team')),
            ],
            options={
                'db_table': 'playerteam',
            },
        ),
        migrations.CreateModel(
            name='Playerposition',
            fields=[
                ('playerpositionid', models.AutoField(db_column='PlayerPositionId', primary_key=True, serialize=False)),
                ('playerid', models.ForeignKey(db_column='PlayerId', on_delete=django.db.models.deletion.DO_NOTHING, to='basketball.Player')),
                ('positionid', models.ForeignKey(db_column='PositionId', on_delete=django.db.models.deletion.DO_NOTHING, to='basketball.Position')),
            ],
            options={
                'db_table': 'playerposition',
            },
        ),
        migrations.CreateModel(
            name='Gameplayerstat',
            fields=[
                ('gameplayerstatid', models.AutoField(db_column='GamePlayerStatId', primary_key=True, serialize=False)),
                ('mp', models.IntegerField(db_column='MP')),
                ('fg', models.IntegerField(db_column='FG')),
                ('fga', models.IntegerField(db_column='FGA')),
                ('number_3p', models.IntegerField(db_column='3P')),
                ('number_3pa', models.IntegerField(db_column='3PA')),
                ('ft', models.IntegerField(db_column='FT')),
                ('fta', models.IntegerField(db_column='FTA')),
                ('orb', models.IntegerField(db_column='ORB')),
                ('drb', models.IntegerField(db_column='DRB')),
                ('ast', models.IntegerField(db_column='AST')),
                ('pf', models.IntegerField(db_column='PF')),
                ('st', models.IntegerField(db_column='ST')),
                ('tov', models.IntegerField(db_column='TOV')),
                ('bs', models.IntegerField(db_column='BS')),
                ('pts', models.IntegerField(db_column='PTS')),
                ('gameid', models.ForeignKey(db_column='GameId', on_delete=django.db.models.deletion.DO_NOTHING, to='basketball.Game')),
                ('playerid', models.ForeignKey(db_column='PlayerId', on_delete=django.db.models.deletion.DO_NOTHING, to='basketball.Player')),
            ],
            options={
                'db_table': 'gameplayerstat',
            },
        ),
        migrations.AddField(
            model_name='game',
            name='awayid',
            field=models.ForeignKey(db_column='AwayId', on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='basketball.Team'),
        ),
        migrations.AddField(
            model_name='game',
            name='homeid',
            field=models.ForeignKey(db_column='HomeId', on_delete=django.db.models.deletion.DO_NOTHING, to='basketball.Team'),
        ),
        migrations.AddField(
            model_name='game',
            name='seasonid',
            field=models.ForeignKey(db_column='SeasonId', on_delete=django.db.models.deletion.DO_NOTHING, to='basketball.Season'),
        ),
        migrations.CreateModel(
            name='Player_stat',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('year', models.CharField(db_column='Year', max_length=5)),
                ('type', models.CharField(db_column='Type', max_length=128)),
                ('player_name', models.CharField(db_column='Player_Name', max_length=128)),
                ('player_imageurl', models.CharField(db_column='Player_ImageURL', max_length=2083)),
                ('team_name', models.CharField(db_column='Team_Name', max_length=128)),
                ('height', models.IntegerField(db_column='Height')),
                ('weight', models.IntegerField(db_column='Weight')),
                ('age', models.IntegerField(db_column='Age')),
                ('mp', models.DecimalField(db_column='MP', decimal_places=0, max_digits=32)),
                ('fg', models.DecimalField(db_column='FG', decimal_places=0, max_digits=32)),
                ('fga', models.DecimalField(db_column='FGA', decimal_places=0, max_digits=32)),
                ('fgp', models.DecimalField(db_column='FGP', decimal_places=4, max_digits=39)),
                ('number_3p', models.DecimalField(db_column='3P', decimal_places=0, max_digits=32)),
                ('number_3pa', models.DecimalField(db_column='3PA', decimal_places=0, max_digits=32)),
                ('number_3pp', models.DecimalField(db_column='3PP', decimal_places=4, max_digits=39)),
                ('ft', models.DecimalField(db_column='FT', decimal_places=0, max_digits=32)),
                ('fta', models.DecimalField(db_column='FTA', decimal_places=0, max_digits=32)),
                ('ftp', models.DecimalField(db_column='FTP', decimal_places=4, max_digits=39)),
                ('orb', models.DecimalField(db_column='ORB', decimal_places=0, max_digits=32)),
                ('drb', models.DecimalField(db_column='DRB', decimal_places=0, max_digits=32)),
                ('ast', models.DecimalField(db_column='AST', decimal_places=0, max_digits=32)),
                ('pf', models.DecimalField(db_column='PF', decimal_places=0, max_digits=32)),
                ('st', models.DecimalField(db_column='ST', decimal_places=0, max_digits=32)),
                ('tov', models.DecimalField(db_column='TOV', decimal_places=0, max_digits=32)),
                ('bs', models.DecimalField(db_column='BS', decimal_places=0, max_digits=32)),
                ('pts', models.DecimalField(db_column='PTS', decimal_places=0, max_digits=32)),
            ],
            options={
                'db_table': 'player_stat',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Team_stat',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('year', models.CharField(db_column='Year', max_length=5)),
                ('team_name', models.CharField(db_column='Team_Name', max_length=128)),
                ('league_name', models.CharField(db_column='League_Name', max_length=128)),
                ('fg', models.DecimalField(db_column='FG', decimal_places=0, max_digits=54)),
                ('fga', models.DecimalField(db_column='FGA', decimal_places=0, max_digits=54)),
                ('fgp', models.DecimalField(db_column='FGP', decimal_places=4, max_digits=61)),
                ('number_3p', models.DecimalField(db_column='3P', decimal_places=0, max_digits=54)),
                ('number_3pa', models.DecimalField(db_column='3PA', decimal_places=0, max_digits=54)),
                ('number_3pp', models.DecimalField(db_column='3PP', decimal_places=4, max_digits=61)),
                ('ft', models.DecimalField(db_column='FT', decimal_places=0, max_digits=54)),
                ('fta', models.DecimalField(db_column='FTA', decimal_places=0, max_digits=54)),
                ('ftp', models.DecimalField(db_column='FTP', decimal_places=4, max_digits=61)),
                ('orb', models.DecimalField(db_column='ORB', decimal_places=0, max_digits=54)),
                ('drb', models.DecimalField(db_column='DRB', decimal_places=0, max_digits=54)),
                ('ast', models.DecimalField(db_column='AST', decimal_places=0, max_digits=54)),
                ('pf', models.DecimalField(db_column='PF', decimal_places=0, max_digits=54)),
                ('st', models.DecimalField(db_column='ST', decimal_places=0, max_digits=54)),
                ('tov', models.DecimalField(db_column='TOV', decimal_places=0, max_digits=54)),
                ('bs', models.DecimalField(db_column='BS', decimal_places=0, max_digits=54)),
            ],
            options={
                'db_table': 'team_stat',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='League_stat',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('year', models.CharField(db_column='Year', max_length=5)),
                ('league_name', models.CharField(db_column='League_Name', max_length=128)),
                ('score', models.DecimalField(db_column='Score', decimal_places=4, max_digits=58)),
                ('fg', models.DecimalField(db_column='FG', decimal_places=4, max_digits=58)),
                ('fga', models.DecimalField(db_column='FGA', decimal_places=4, max_digits=58)),
                ('fgp', models.DecimalField(db_column='FGP', decimal_places=8, max_digits=65)),
                ('number_3p', models.DecimalField(db_column='3P', decimal_places=4, max_digits=58)),
                ('number_3pa', models.DecimalField(db_column='3PA', decimal_places=4, max_digits=58)),
                ('number_3pp', models.DecimalField(db_column='3PP', decimal_places=8, max_digits=65)),
                ('ft', models.DecimalField(db_column='FT', decimal_places=4, max_digits=58)),
                ('fta', models.DecimalField(db_column='FTA', decimal_places=4, max_digits=58)),
                ('ftp', models.DecimalField(db_column='FTP', decimal_places=8, max_digits=65)),
                ('orb', models.DecimalField(db_column='ORB', decimal_places=4, max_digits=58)),
                ('drb', models.DecimalField(db_column='DRB', decimal_places=4, max_digits=58)),
                ('ast', models.DecimalField(db_column='AST', decimal_places=4, max_digits=58)),
                ('pf', models.DecimalField(db_column='PF', decimal_places=4, max_digits=58)),
                ('st', models.DecimalField(db_column='ST', decimal_places=4, max_digits=58)),
                ('tov', models.DecimalField(db_column='TOV', decimal_places=4, max_digits=58)),
                ('bs', models.DecimalField(db_column='BS', decimal_places=4, max_digits=58)),
            ],
            options={
                'db_table': 'league_stat',
                'managed': False,
            },
        ),
    ]
