import requests
from datetime import datetime, timedelta

# Define the base URL and API key
url_base = 'https://api.sportradar.com/mlb/trial/v7/en/games/2023/09/{day}/boxscore.json'
api_key = 'SvGLYShuQQ5RuSyFGAGlQqH2eI5w5zUanQ8pizwj'

# Initialize a dictionary to keep track of runs and games for each team
team_stats = {}

# Loop through each day in September 2023
start_date = datetime(2023, 3, 30)
end_date = datetime(2023, 9, 30)

current_date = start_date
while current_date <= end_date:
    day = current_date.strftime('%d')  # Format day as '01', '02', ..., '30'
    url = url_base.format(day=day)  # Insert the day into the URL

    params = {
        'api_key': api_key
    }

    response = requests.get(url, params=params)

    if response.status_code == 200:
        data = response.json()
        #print(f"Data retrieved successfully for {current_date.strftime('%Y-%m-%d')}!")

        # Assuming the games are listed under 'games' within 'league'
        games = data.get('league', {}).get('games', [])

        for game in games:
            game_info = game.get('game', {})
            home_team = game_info.get('home', {})
            away_team = game_info.get('away', {})

            # Fetching names and runs for home and away teams
            home_team_name = home_team.get('name', 'Unknown Home Team')
            away_team_name = away_team.get('name', 'Unknown Away Team')
            home_team_runs = home_team.get('runs', 0)
            away_team_runs = away_team.get('runs', 0)

            # Update the team stats
            if home_team_name not in team_stats:
                team_stats[home_team_name] = {'runs': 0, 'games': 0}
            if away_team_name not in team_stats:
                team_stats[away_team_name] = {'runs': 0, 'games': 0}

            team_stats[home_team_name]['runs'] += home_team_runs
            team_stats[home_team_name]['games'] += 1
            team_stats[away_team_name]['runs'] += away_team_runs
            team_stats[away_team_name]['games'] += 1

    #else:
          #print(f"Failed to retrieve data for {current_date.strftime('%Y-%m-%d')}. Status code:", response.status_code)
    
    # Move to the next day
    current_date += timedelta(days=1)

# After gathering all data, calculate and print the average runs for each team
print("\nAverage Runs Scored Per Game by Each Team:")
for team, stats in team_stats.items():
    if stats['games'] > 0:
        average_runs = stats['runs'] / stats['games']
        print(f"{team}: {average_runs:.2f} runs/game")
    else:
        print(f"{team}: No games played")
