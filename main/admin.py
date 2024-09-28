from django.contrib import admin
from . models import Fixture, Statboard, Club, Squad

class fixtureadmin(admin.ModelAdmin):
    list_display = ['home_team',"away_team",'home_score','away_score','gameweek','date']

class statboard(admin.ModelAdmin):
    list_display = ['player_name','goals','assists','clean_sheets', 'team_name']
    
class club(admin.ModelAdmin):
    list_display = ['club_name','club_logo']

class squad(admin.ModelAdmin):
    list_display = ['player_name','club_name']

admin.site.register(Fixture, fixtureadmin)
admin.site.register(Statboard, statboard)
admin.site.register(Club, club)
admin.site.register(Squad, squad)