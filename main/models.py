from django.db import models
from django.utils.text import slugify
from django.db.models.signals import pre_save
from django.dispatch import receiver
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
    slug = models.SlugField(blank=True,null=True)
    club_logo = models.ImageField(upload_to='images/logo', null=True)

    def __str__(self):
        return f'{self.club_name}'
    def __str__(self):
        return f'{self.slug}'

class Squad(models.Model):
    player_name = models.CharField(max_length=50)
    club_name = models.ForeignKey(Club, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.player_name} {self.club_name}'
    
class Standing(models.Model):
    team_rank = models.IntegerField()
    club_logo = models.ForeignKey(Club, related_name='standing_logo', on_delete=models.CASCADE)
    club_name = models.ForeignKey(Club, related_name='standing_name', on_delete=models.CASCADE)
    m_played = models.IntegerField()
    m_won = models.IntegerField()
    m_drawn = models.IntegerField()
    m_lost = models.IntegerField()
    g_forward = models.IntegerField()
    g_against = models.IntegerField()
    g_difference = models.CharField(max_length=5)  # +10 or -2, so using CharField
    points = models.IntegerField()
    next_match = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.team_rank} {self.club_name} {self.club_logo}"
    
def add_slug(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = slugify(instance.club_name)
       # instance.slug+= 'shakalaka'
pre_save.connect(add_slug,sender=Club)
    
"""   
class Matchdetails(models.Model):
    match_id = models.ForeignKey(Fixture, on_delete=models.CASCADE)
    home_scorer = models.CharField(max_length=50, null=True)
    away_scorer = models.CharField(max_length=50,null=True)
    scoringtime = models.CharField(max_length=50, null=True)
"""    