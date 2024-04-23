import requests
from datetime import datetime, timedelta

# Define the base URL and API key
url_base = 'https://api.sportradar.com/mlb/trial/v7/en/games/2023/09/{day}/boxscore.json'
standings_url = 'https://api.sportradar.com/mlb/trial/v7/en/seasons/2023/REG/standings.json'
api_key = 'SvGLYShuQQ5RuSyFGAGlQqH2eI5w5zUanQ8pizwj'

# Initialize a dictionary to keep track of runs, games, win percentage, and average attendance for each team
team_stats = {}

# Fetch standings for win percentage
params = {'api_key': api_key}
response = requests.get(standings_url, params=params)

if response.status_code == 200:
    standings_data = response.json()
    # Extract win percentages from the standings data
    for league in standings_data['league']['season']['leagues']:
        for division in league['divisions']:
            for team in division['teams']:
                team_name = f"{team['market']} {team['name']}"
                team_stats[team_name] = {
                    'runs': 0,
                    'games': 0,
                    'win_percentage': team['win_p'],
                    'total_attendance': 0  # Initialize total attendance
                }

# Loop through each day in the period
start_date = datetime(2023, 3, 30)
end_date = datetime(2023, 9, 30)

current_date = start_date
while current_date <= end_date:
    day = current_date.strftime('%d')  # Format day as '01', '02', ..., '30'
    url = url_base.format(day=day)  # Insert the day into the URL

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
            home_team_name = f"{home_team['market']} {home_team['name']}"
            away_team_name = f"{away_team['market']} {away_team['name']}"
            home_team_runs = home_team.get('runs', 0)
            away_team_runs = away_team.get('runs', 0)
            attendance = game_info.get('attendance', 0)

            # Update the team stats for runs, games, and total attendance
            team_stats[home_team_name]['runs'] += home_team_runs
            team_stats[home_team_name]['games'] += 1
            team_stats[home_team_name]['total_attendance'] += attendance
            team_stats[away_team_name]['runs'] += away_team_runs
            team_stats[away_team_name]['games'] += 1

    #else:
        #print(f"Failed to retrieve data for {current_date.strftime('%Y-%m-%d')}. Status code:", response.status_code)
    
    # Move to the next day
    current_date += timedelta(days=1)

# After gathering all data, calculate and print the average runs, win percentage, and average attendance for each team
print("\nTeam Statistics:")
for team, stats in team_stats.items():
    if stats['games'] > 0:
        average_runs = stats['runs'] / stats['games']
        average_attendance = stats['total_attendance'] / stats['games']
        print(f"{team}: {average_runs:.2f} runs/game, Win Percentage: {stats['win_percentage']:.3f}, Average Attendance: {average_attendance:.0f}")
    else:
        print(f"{team}: No games played")

