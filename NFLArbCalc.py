import requests

# Functionname , we are just finding moneyline
def find_arbitrage(game):
    odds_dict = {}

    # Loop all the bookmakers from json file and list all the moneyline odds 
    for bookmaker in game['bookmakers']:
        for market in bookmaker['markets']:
            if market['key'] == 'h2h':  # Focus on head-to-head (moneyline) market
                for outcome in market['outcomes']:
                    team = outcome['name']
                    odds = outcome['price']
                    
                    # Store odds and bookmaker
                    if team not in odds_dict:
                        odds_dict[team] = []
                    odds_dict[team].append((bookmaker['title'], odds))

    # Check arbitrage opportunities for both teams in game
    for team, odds_list in odds_dict.items():
        # identify positive and negative odds and track which bookmaker offered them
        positive_odds = [(bookmaker, odds) for bookmaker, odds in odds_list if odds > 0]
        negative_odds = [(bookmaker, odds) for bookmaker, odds in odds_list if odds < 0]

        if positive_odds and negative_odds:
            # Find highest positive odds and the lowest negative odds for team
            highest_positive_bookmaker, highest_positive_odds = max(positive_odds, key=lambda x: x[1])
            lowest_negative_bookmaker, lowest_negative_odds = min(negative_odds, key=lambda x: x[1])

            # If arbitrage opportunity is found (Absolute value of lowest negative favorited odds is lower than highest positive odds)
            if highest_positive_odds > abs(lowest_negative_odds):
                print(f"Arbitrage opportunity for {team}")
                print(f"Positive odds: {highest_positive_odds} at {highest_positive_bookmaker}")
                print(f"Negative odds: {lowest_negative_odds} at {lowest_negative_bookmaker}\n")

url = 'https://api.the-odds-api.com/v4/sports/americanfootball_nfl/odds/'
params = {
    'regions': 'us',              # US bookmakers only 
    'markets': 'h2h',             # Moneyline odds only
    'oddsFormat': 'american',     # list the odds in American format unlike decimal format
    'apiKey': '08b9da96436b1f05032f181ad0c26e41'# This is unique to me unlock yiur own at the odds API
}

response = requests.get(url, params=params)

if response.status_code == 200:
    data = response.json()
    
    # Loop through each game, team and display odds, then check for arbitrage last
    for game in data:
        print(f"Game: {game['home_team']} vs {game['away_team']}")
        
        # Call the arbitrage-checking function
        find_arbitrage(game)
#if code unsuccesful
else:
    print(f"Failed to retrieve data. Status code: {response.status_code}")