from django.db import models

# Create your models here.

class Fixture(models.Model):
    home_team = models.CharField(max_length=50)
    away_team = models.CharField(max_length=50)
    home_score = models.CharField(max_length=10, null=True)
    away_score = models.CharField(max_length=10, null=True)
    date = models.CharField(max_length=50)  
    gameweek = models.IntegerField(null=True)
    
    def __str__(self):
        return f'{self.home_team} {self.home_score} vs {self.away_team} {self.away_score}'
    
class Statboard(models.Model):
    player_name = models.CharField(max_length=50)
    goals = models.IntegerField(null=True)
    team_name = models.CharField(max_length=50)
    assists = models.IntegerField(null=True)
    clean_sheets = models.IntegerField(null=True)
    
class Club(models.Model):
    club_name = models.CharField(max_length=50)
    club_logo = models.ImageField(upload_to='images/logo', null=True)

    def __str__(self):
        return f'{self.club_name}'

class Squad(models.Model):
    player_name = models.CharField(max_length=50)
    club_name = models.ForeignKey(Club, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.player_name} {self.club_name}'
    
"""   
class Matchdetails(models.Model):
    match_id = models.ForeignKey(Fixture, on_delete=models.CASCADE)
    home_scorer = models.CharField(max_length=50, null=True)
    away_scorer = models.CharField(max_length=50,null=True)
    scoringtime = models.CharField(max_length=50, null=True)
"""    