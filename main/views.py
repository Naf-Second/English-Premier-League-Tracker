from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from django.shortcuts import render, get_object_or_404
import requests
from .models import Fixture, Statboard, Club, Squad, Standing
from datetime import datetime
import re

def unslugify(slug):
    text = slug.replace('-', ' ').replace('_', ' ')
    return re.sub(r'\b\w', lambda m: m.group().upper(), text)

def fixtureview(request,*args, **kwargs):  

    upcoming_fixtures = '4'
    # Fetch the saved fixtures and group them by gameweek
    grouped_fixtures = Fixture.objects.order_by('gameweek').values('gameweek').distinct()
    clubs = Club.objects.values('club_name','club_logo').distinct()
    
    squads_by_team = {}
    fixtures_by_gameweek = {}
    
    for gameweek in grouped_fixtures:
        fixtures_by_gameweek[gameweek['gameweek']] = Fixture.objects.filter(gameweek=gameweek['gameweek'])
    
    
    #This part very important, filtering through 2 different classes and getting the squad for each club
    for club in clubs:
        cname = club['club_name']
        
        
        #Being rendered at front using basic key-value concept of dictionary. Here Club is the key and squad, logo 
        # are the values
        squads_by_team[cname] = {
            'squad': Squad.objects.filter(club_name__club_name=cname).order_by('?')[:5],
            'logo': club['club_logo']  
        }
        
    #print(squads_by_team)

    return render(request, 'home.html', {'fixtures_by_gameweek': fixtures_by_gameweek, "upcoming": upcoming_fixtures,
                                         'squads_by_team': squads_by_team})

def standing(request):
    table = Standing.objects.all()
    context = {
        'table': table
    } 
    return render(request, 'standings.html', context)


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


def clubs(request):
    clubs = Club.objects.all()
    print(clubs)
    context = {
        'clubs': clubs,
    }
    
    return render(request, 'clubs.html', context)


def club_squad(request, slug):

    c_name = unslugify(slug)


    club = get_object_or_404(Club, club_name=c_name)
    squads = Squad.objects.filter(club_name__club_name=c_name)
    
    #print(squads)

    return render(request, 'club_squad.html', {'club': club, 'squads': squads})


def squadcreate(request):

    club = get_object_or_404(Club, club_name="Tottenham Hotspur")

    player_names = [
       
    ]
    for player in player_names:
        Squad.objects.create(
            player_name=player,
            club_name=club
        )    
    return render(request, 'squadcreate.html')

def updategameweek(request):
    #Use this when the gameweek has already been played but schedule for gameweek is not available 
    #For example 6,8,9 gameweek 7 is missing, just change the gameweek variable and update the url.
    #Also when has already been played and needs updating the results.
    
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run Chrome in headless mode
    chrome_options.add_argument("--disable-gpu")  # Disable GPU acceleration (optional)

    driver = webdriver.Chrome(options=chrome_options)

    # Open the first page
    url = "https://fantasy.premierleague.com/fixtures/7"
    driver.get(url)

    main = driver.find_elements(By.ID, "mainContent")
    lines = []
    for obj1 in main:
        var = obj1.find_elements(By.ID, "root")
        for v in var:
            values = v.text
            lines = values.split('\n')
            lines = [x for x in lines if x != 'Opens in new tab']
            
            break
            

    fetched_data = lines


    def convert_to_standard_date(date_str):
        try:
            return datetime.strptime(date_str, '%A %d %B %Y').strftime('%Y-%m-%d')
        except ValueError:
            return None

    # Identify the dates and store converted dates in a list
    converted_data = []
    dates = []
    for item in fetched_data:
        # Try converting each item to a valid date
        converted_date = convert_to_standard_date(item)
        if converted_date:
            dates.append(converted_date)
            converted_data.append(converted_date)
        else:
            converted_data.append(item)

    # Now split data based on identified dates
    matches_by_date = {}
    current_date = None

    for i in range(len(converted_data)):
        if converted_data[i] in dates:
            current_date = converted_data[i]
            matches_by_date[current_date] = []
        elif current_date:
            # Append the match details to the current date
            matches_by_date[current_date].append(converted_data[i])

    h_team = []
    h_score = []
    a_team = []
    a_score = []
    
    # Now process matches for each date
    for date, match_data in matches_by_date.items():
        #print(f"\nMatches for {date}:\n")
        for i in range(0, len(match_data), 4):
            # Ensure we have enough data for each match (home_team, home_score, away_score, away_team)
            if i + 3 < len(match_data):
                home_team = match_data[i]
                h_team.append(match_data[i])
                home_score = match_data[i + 1]
                h_score.append(match_data[i + 1])
                away_score = match_data[i + 2]
                a_score.append(match_data[i + 2])
                away_team = match_data[i + 3]
                a_team.append(match_data[i + 3])  

             
            #print(f"Fixture created: {home_team} {home_score} vs {away_team} {away_score}, Date: {date}")

    fixtures = Fixture.objects.filter(gameweek=8)
    #Fixture.objects.filter(gameweek=7).delete()
    i=0
   # print(fixtures('home_team'))
    print(f'This is h_team {h_team}')
    for fixture in fixtures:
       fixture.home_team = h_team[i]
       fixture.home_score = h_score[i]
       fixture.away_score = a_score[i]
       fixture.away_team = a_team[i]
       
       fixture.save()
       i+=1

    # Create the Fixture object
    return render(request, 'update.html')     
    
    



def updatefixture(request):
    
    #Use this when the schedules has been changed and needs updating the fixture.
    #Change two variable first the gameweek in url and then gameweek in the fixture
    
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run Chrome in headless mode
    chrome_options.add_argument("--disable-gpu")  # Disable GPU acceleration (optional)

    driver = webdriver.Chrome(options=chrome_options)

    # Open the first page
    url = "https://fantasy.premierleague.com/fixtures/9"
    driver.get(url)

    main = driver.find_elements(By.ID, "mainContent")
    lines = []
    for obj1 in main:
        var = obj1.find_elements(By.ID, "root")
        for v in var:
            values = v.text
            lines = values.split('\n')
            lines = [x for x in lines if x != 'Opens in new tab']
            
            break
            
    fetched_data = lines[13:]

    # Helper function to convert date string into 'YYYY-MM-DD' format
    def convert_to_standard_date(date_str):
        try:
            # Convert 'Saturday 5 October 2024' or similar into '2024-10-05'
            return datetime.strptime(date_str, '%A %d %B %Y').strftime('%Y-%m-%d')
        except ValueError:
            return None

    # Identify the dates and store converted dates in a list
    converted_data = []
    dates = []
    for item in fetched_data:
        # Try converting each item to a valid date
        converted_date = convert_to_standard_date(item)
        if converted_date:
            dates.append(converted_date)
            converted_data.append(converted_date)
        else:
            converted_data.append(item)


    # Now split data based on identified dates
    matches_by_date = {}
    current_date = None

    for i in range(len(converted_data)):
        if converted_data[i] in dates:
            current_date = converted_data[i]
            matches_by_date[current_date] = []
        elif current_date:
            # Append the match details to the current date
            matches_by_date[current_date].append(converted_data[i])

    h_team = []
    a_team = []
    for date, match_data in matches_by_date.items():
        print(f"\nMatches for {date}:\n")
        for i in range(0, len(match_data), 3):

            if i + 2 < len(match_data):
                home_team = match_data[i]
                h_team.append(match_data[i])
                home_score = None
                away_team = match_data[i + 2]
                a_team.append(match_data[i + 2])
                away_score = None
                
   # print(matches_by_date)
    fixtures = Fixture.objects.filter(gameweek=9)
    i=0
   # print(fixtures('home_team'))
    print(f'This is h_team {h_team}')
    for fixture in fixtures:
       fixture.home_team = h_team[i]
       fixture.away_team = a_team[i]
       
       fixture.save()
       i+=1    
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

    return render(request, 'update2.html', context)

def fetch_league_standing(request):
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run Chrome in headless mode
    chrome_options.add_argument("--disable-gpu")  # Disable GPU acceleration (optional)

    driver = webdriver.Chrome(options=chrome_options)

    # Open the first page
    url = "https://www.premierleague.com/tables"
    driver.get(url)

    main = driver.find_elements(By.ID, "mainContent")
    splited_data = []
    for obj1 in main:
        obj1 = obj1.text
        splited_data = obj1.split('\n')
        break
    driver.quit()
    fetched_data = splited_data[15:]
    table_data = []
    Standing.objects.all().delete()
    # Iterate over the fetched data with a step of 9 (since each team's data spans 9 elements)
    for i in range(0, len(fetched_data), 9):

        team_rank = fetched_data[i]
        team_name = fetched_data[i+1]
        stats = fetched_data[i+2].split()  # Splitting the stats string
        next_match = fetched_data[i+8]
        print(f'Team Rank: {team_rank}, Team Name: {team_name}, Stats: {stats}, Next Match: {next_match}')
        clubs = Club.objects.values('club_name','club_logo').distinct()
        if(team_name=='Bournemouth'):
            team_name = 'AFC Bournemouth'
            
        for club in clubs:
            #print("Working1")
            if club['club_name'] == team_name:
                print('Working2')
                club = get_object_or_404(Club, club_name=team_name)
                print(f'{team_rank},{club}')
                Standing.objects.create(
                    team_rank = int(team_rank),
                    club_logo = club, 
                    club_name = club,
                    m_played = int(stats[0]),
                    m_won = int(stats[1]),
                    m_drawn = int(stats[2]),
                    m_lost = int(stats[3]),
                    g_forward = int(stats[4]),
                    g_against = int(stats[5]),
                    g_difference = stats[6],
                    points = int(stats[7]),
                    next_match = next_match
                )

                #table_data.append(team_data)

    return render(request, 'update3.html',)

def testpage(request):
    team_name = "Everton"
    var = get_object_or_404(Club, club_name=team_name)
    logo = var.club_logo
    return render(request, 'testpage.html', {'logo': logo})


    






    


    
    
