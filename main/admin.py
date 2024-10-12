from django.contrib import admin
from . models import Fixture, Statboard, Club, Squad, Standing

class fixtureadmin(admin.ModelAdmin):
    list_display = ['home_team',"away_team",'home_score','away_score','gameweek','date']

class statboard(admin.ModelAdmin):
    list_display = ['player_name','goals','assists','clean_sheets', 'team_name']
    
class club(admin.ModelAdmin):
    list_display = ['club_name','slug','club_logo']

class squad(admin.ModelAdmin):
    list_display = ['player_name','club_name']
    
class standing(admin.ModelAdmin):
    list_display = ['team_rank','club_name','club_logo','next_match']

admin.site.register(Fixture, fixtureadmin)
admin.site.register(Statboard, statboard)
admin.site.register(Club, club)
admin.site.register(Squad, squad)
admin.site.register(Standing, standing)