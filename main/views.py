from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from django.shortcuts import render
import requests
from .models import Fixture, Statboard
from datetime import datetime

def fixtureview(request):
    base_url = 'https://apiv3.apifootball.com/?action=get_events&from=2024-08-04&to=2024-09-30&league_id=152&APIkey=6a0d608ae7b62cfb897b3f5ec66a7a467025304cbbf3ec351dcc940b2a99b7e0'
    r = requests.get(base_url).json()
    
    #This variable is shows the upcoming gameweek. Its value is always the upcoming week minus 1 (Zero based indexed). 
    upcoming_fixtures = '3'
    
    """""
    fixtures = []
    i = 0
    gameweek = 0
    for obj in r:

        x = obj["match_hometeam_name"]
        y = obj["match_awayteam_name"]

        if x == "Tottenham":
            x = "Tottenham Hotspur"
        elif x == "Newcastle":
            x = "Newcastle United"
        elif x == "Manchester Utd":
            x = "Manchester United"

        if y == "Tottenham":
            y = "Tottenham Hotspur"
        elif y == "Newcastle":
            y = "Newcastle United"
        elif y == "Manchester Utd":
            y = "Manchester United"
            
        if i%10==0:
            gameweek += 1
            
        fixture.objects.create(
                home_team = x,
                #home_score =obj["match_hometeam_score"],
                home_score = None,
                away_team = y,
                #away_score = obj["match_awayteam_score"],
                away_score = None,
                date = obj["match_date"],
                gameweek = gameweek
            )
        i += 1
    """
    # Fetch the saved fixtures and group them by gameweek
    grouped_fixtures = Fixture.objects.order_by('gameweek').values('gameweek').distinct()
    fixtures_by_gameweek = {}
    
    for gameweek in grouped_fixtures:
        fixtures_by_gameweek[gameweek['gameweek']] = Fixture.objects.filter(gameweek=gameweek['gameweek'])
   
   
   
    return render(request, 'home.html', {'fixtures_by_gameweek': fixtures_by_gameweek, "upcoming": upcoming_fixtures})



def standing(request):
    apikey = '6a0d608ae7b62cfb897b3f5ec66a7a467025304cbbf3ec351dcc940b2a99b7e0'
    
    base_url = f'https://apiv3.apifootball.com/?action=get_standings&league_id=152&APIkey={apikey}'
    r = requests.get(base_url)
    response = r.json()

    for obj in response:
        # added 3 new keys to the response dictionary
        w = int(obj["overall_league_W"])
        l = int(obj["overall_league_L"])
        d = int(obj["overall_league_D"])
        matches_played = w+l+d
        obj['matches_played'] = matches_played
        
        GF = int(obj["overall_league_GF"])
        GA = int(obj["overall_league_GA"])
        goal_difference = GF-GA
        obj['goal_difference'] = goal_difference
        
    return render(request, 'standings.html', {'response':response})



def stats(request):
    top = Statboard.objects.filter(goals__isnull=False)
    top2 = Statboard.objects.filter(assists__isnull=False)
    top3 = Statboard.objects.filter(clean_sheets__isnull=False)
    # Create a list of dictionaries containing player data
    player_stats = []
    player_stats2 = []
    player_stats3 = []
    i=1
    #For Goals Section
    for obj in top:
        player_stats.append({
            'player_name': obj.player_name,
            'goals': obj.goals,
            'team': obj.team_name
        })
    #For Assists Section
    for obj in top2:
        player_stats2.append({
            'player_name': obj.player_name,
            'assists': obj.assists,
            'team': obj.team_name
        })
    #For Clean Sheets Section
    for obj in top3:
        player_stats3.append({
            'player_name': obj.player_name,
            'csheets': obj.clean_sheets,
            'team': obj.team_name
        })
    #these prints are debugger
   # print(player_stats)
   # print(player_stats2)
   
    context = {
        'player_stats': player_stats,
        'player_stats2': player_stats2,
        'player_stats3': player_stats3,

    }
    return render(request, 'stats.html', context)


def updategameweek(request):
    
    #must change the dates to latest gameweek
    
    startdate = '2024-09-14'
    enddate = '2024-09-15'
    apikey = '6a0d608ae7b62cfb897b3f5ec66a7a467025304cbbf3ec351dcc940b2a99b7e0'
    
    base_url = f'https://apiv3.apifootball.com/?action=get_events&from={startdate}&to={enddate}&league_id=152&APIkey={apikey}'
    r = requests.get(base_url).json()

    # Initialize lists to store teams and scores from the API response
    home_team2 = []
    home_score2 = []
    away_team2 = []
    away_score2 = []

    # Populate the lists with data from the API response
    for obj in r:
        x = obj["match_hometeam_name"]
        y = obj["match_awayteam_name"]

        if x == "Tottenham":
            x = "Tottenham Hotspur"
        elif x == "Newcastle":
            x = "Newcastle United"
        elif x == "Manchester Utd":
            x = "Manchester United"
        elif x == "Bournemouth": 
            x = "AFC Bournemouth"
        elif x== "Ipswich":
            x = "Ipswich Town"

        if y == "Tottenham":
            y = "Tottenham Hotspur"
        elif y == "Newcastle":
            y = "Newcastle United"
        elif y == "Manchester Utd":
            y = "Manchester United"
        elif y == "Bournemouth": 
            y = "AFC Bournemouth"
        elif y == "Ipswich":
            y = "Ipswich Town"

        home_team2.append(x)
        home_score2.append(obj["match_hometeam_score"])
        away_team2.append(y)
        away_score2.append(obj["match_awayteam_score"])
    print(f'{away_team2}:{away_score2}')
    # Fetch existing fixtures for gameweek 4 (since gameweek starts from 0)
    fixtures_gameweek_4 = Fixture.objects.filter(gameweek=4)
    # gameweek should be the week youre trying to update, and it is not zero based indexed
    fx = len(fixtures_gameweek_4)
    i = 0
    # Iterate through fixtures and update scores based on matching teams
    for match in fixtures_gameweek_4:
        if match.home_team in home_team2:
           # index_in_api = home_team2.index(match.home_team)
            match.home_score = home_score2[i]
            match.away_score = away_score2[i]
        #elif match.home_team in away_team2:
           # index_in_api = away_team2.index(match.home_team)
         #   match.home_score = away_score2[i]  
          #  match.away_score = home_score2[i]
        #elif match.away_team in home_team2:
         #   #index_in_api = home_team2.index(match.away_team)
          #  match.home_score = home_score2[i]
           # match.away_score = away_score2[i]
        elif match.away_team in away_team2:
            #index_in_api = away_team2.index(match.away_team)
            match.home_score = away_score2[i]  
            match.away_score = home_score2[i]
        i+=1
        # Save updated match
        match.save()

    return render(request, 'update.html')


def fetch_premier_league_stats(request):
    Statboard.objects.all().delete()
    
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")

    driver = webdriver.Chrome(options=chrome_options)

    url = "https://www.premierleague.com/stats"
    driver.get(url)

    player_stats = {'Name': [], 'Goals': [], 'Team Name': []}
    player_stats2 = {'Name': [], 'Assists': [], 'Team Name': []}
    player_stats3 = {'Name': [], 'Clean Sheet': [], 'Team Name': []}
    
    rev = driver.find_elements(By.ID, "mainContent")
    goalstat, assiststat, csstat = [], [], []
    
    for obj1 in rev:
        stat = obj1.find_elements(By.CLASS_NAME, "top-stats__list")
        i = 0
        for obj in stat:
            i += 1
            if i == 1:
                goalstat = obj.text.split('\n')
            if i == 2:
                assiststat = obj.text.split('\n')
            if i == 4:
                csstat = obj.text.split('\n')

    driver.quit()

    # Goals Section
    if len(goalstat) >= 6:
        Statboard.objects.create(
            player_name=goalstat[1] + " " + goalstat[2],
            goals=int(goalstat[4]),
            team_name=goalstat[3]
        )
        player_stats['Name'].append(goalstat[1] + " " + goalstat[2])
        player_stats['Goals'].append(goalstat[4])
        player_stats['Team Name'].append(goalstat[3])

        for i in range(6, len(goalstat), 4):
            Statboard.objects.create(
                player_name=goalstat[i],
                goals=int(goalstat[i + 2]),
                team_name=goalstat[i + 1]
            )
            player_stats['Name'].append(goalstat[i])
            player_stats['Goals'].append(goalstat[i + 2])
            player_stats['Team Name'].append(goalstat[i + 1])

    # Assists Section
    if len(assiststat) >= 6:
        Statboard.objects.create(
            player_name=assiststat[1] + " " + assiststat[2],
            assists=int(assiststat[4]),
            team_name=assiststat[3]
        )
        player_stats2['Name'].append(assiststat[1] + " " + assiststat[2])
        player_stats2['Assists'].append(assiststat[4])
        player_stats2['Team Name'].append(assiststat[3])

        for i in range(6, len(assiststat), 4):
            Statboard.objects.create(
                player_name=assiststat[i],
                assists=int(assiststat[i + 2]),
                team_name=assiststat[i + 1]
            )
            player_stats2['Name'].append(assiststat[i])
            player_stats2['Team Name'].append(assiststat[i + 1])
            player_stats2['Assists'].append(assiststat[i + 2])
            
    # Clean Sheet Section
    if len(csstat) >= 6:
        Statboard.objects.create(
            player_name=csstat[1] + " " + csstat[2],
            clean_sheets=int(csstat[4]),
            team_name=csstat[3]
        )
        player_stats3['Name'].append(csstat[1] + " " + csstat[2])
        player_stats3['Clean Sheet'].append(csstat[4])
        player_stats3['Team Name'].append(csstat[3])

        for i in range(6, len(csstat), 4):
            Statboard.objects.create(
                player_name=csstat[i],
                clean_sheets=int(csstat[i + 2]),
                team_name=csstat[i + 1]
            )
            player_stats3['Name'].append(csstat[i])
            player_stats3['Team Name'].append(csstat[i + 1])
            player_stats3['Clean Sheet'].append(csstat[i + 2])

    context = {
        'player_stats': player_stats,
        'player_stats2': player_stats2,
        'player_stats3': player_stats3,
    }

    return render(request, 'update.html', context)






    


    
    
