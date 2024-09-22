from django.contrib import admin
from . models import Fixture, Statboard

class fixtureadmin(admin.ModelAdmin):
    list_display = ['home_team',"away_team",'home_score','away_score','gameweek','date']

class statboard(admin.ModelAdmin):
    list_display = ['player_name','goals','assists','clean_sheets', 'team_name']

admin.site.register(Fixture, fixtureadmin)
admin.site.register(Statboard, statboard)