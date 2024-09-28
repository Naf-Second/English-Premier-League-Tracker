from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

chrome_options = Options()
chrome_options.add_argument("--headless")  # Run Chrome in headless mode
chrome_options.add_argument("--disable-gpu")  # Disable GPU acceleration (optional)

driver = webdriver.Chrome(options=chrome_options)

# Open the first page
url = "https://www.premierleague.com/stats"
driver.get(url)

# Initialize the dictionary
player_stats = {'Name': [], 'Goals': [], 'Team Name': [], 'Assists': [], 'Clean Sheet': []}

# Find the main content element
rev = driver.find_elements(By.ID, "mainContent")
for obj1 in rev:

    stat = obj1.find_elements(By.CLASS_NAME, "top-stats__list")
    i = 0
    for obj in stat:
        i+=1
        if i == 1:
            goalstat = obj.text
            goalstat = goalstat.split('\n')
        if i == 2:
            assiststat = obj.text
            assiststat = assiststat.split('\n')
        if i == 4:
            csstat = obj.text
            csstat = csstat.split('\n')
        
        # Split the text data by newline
    # Now we have a list of player data in 'goalstat'
#print(assiststat)    


# Close the browser
#driver.quit()
player_stats['Name'].append(goalstat[1] + " " + goalstat[2])
player_stats['Goals'].append(goalstat[4])
player_stats['Team Name'].append(goalstat[3])


for i in range(6, len(goalstat), 4):
    player_stats['Name'].append(goalstat[i])
    player_stats['Team Name'].append(goalstat[i+1])
    player_stats['Goals'].append(goalstat[i+2])

player_stats['Name'].append(assiststat[1] + " " + assiststat[2])
player_stats['Assists'].append(assiststat[4])
player_stats['Team Name'].append(assiststat[3])


for i in range(6, len(assiststat), 4):
    player_stats['Name'].append(assiststat[i])
    player_stats['Team Name'].append(assiststat[i+1])
    player_stats['Assists'].append(assiststat[i+2])
    
player_stats['Name'].append(csstat[1] + " " + csstat[2])
player_stats['Clean Sheet'].append(csstat[4])
player_stats['Team Name'].append(csstat[3])


for i in range(6, len(csstat), 4):
    player_stats['Name'].append(csstat[i])
    player_stats['Team Name'].append(csstat[i+1])
    player_stats['Clean Sheet'].append(csstat[i+2])
    

print(player_stats)






def fetch_premier_league_stats(request):
    Statboard.objects.all().delete()
    # Set up Chrome options to run in headless mode
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")

    driver = webdriver.Chrome(options=chrome_options)

    # Open the stats page
    url = "https://www.premierleague.com/stats"
    driver.get(url)

    # Initialize the dictionary to store player stats
    player_stats = {'Name': [], 'Goals': [], 'Team Name': []}
    goalstat = []
    # Find the main content element
    rev = driver.find_elements(By.ID, "mainContent")
    for obj1 in rev:
        stat = obj1.find_element(By.CLASS_NAME, "top-stats__list")
        goalstat = stat.text.split('\n')  # Split the text data by newline

    # Close the browser
    driver.quit()

    Statboard.objects.create(
            player_name=goalstat[1] + " " + goalstat[2],
            goals=goalstat[4],
            team_name=goalstat[3]
        )
    player_stats['Name'].append(goalstat[1] + " " + goalstat[2])
    player_stats['Goals'].append(goalstat[4])
    player_stats['Team Name'].append(goalstat[3])

    # Loop through remaining players and save to the database
    for i in range(6, len(goalstat), 4):
        Statboard.objects.create(
            player_name=goalstat[i],
            goals=goalstat[i + 2],
            team_name=goalstat[i + 1]
        )
        player_stats['Name'].append(goalstat[i])
        player_stats['Team Name'].append(goalstat[i + 1])
        player_stats['Goals'].append(goalstat[i + 2])

    # Pass the player stats to the template
    context = {
        'player_stats': player_stats
    }

    return render(request, 'update.html', context)
