import requests
import json
import codecs

# Define vars
output_file = 'fantasy.csv'
bootstrap_url = 'https://fantasy.premierleague.com/drf/bootstrap-static'
element_url = 'https://fantasy.premierleague.com/drf/element-summary/'
teams = {
    1: 'Arsenal',
    2: 'Bournemouth',
    3: 'Burnley',
    4: 'Chelsea',
    5: 'Crystal Palace',
    6: 'Everton',
    7: 'Hull',
    8: 'Leicester',
    9: 'Liverpool',
    10: 'Man City',
    11: 'Man Utd',
    12: 'Middlesbrough',
    13: 'Southampton',
    14: 'Stoke',
    15: 'Sunderland',
    16: 'Swansea',
    17: 'Spurs',
    18: 'Watford',
    19: 'West Brom',
    20: 'West Ham',
}
positions = {
    1: 'Goalkeeper',
    2: 'Defender',
    3: 'Midfielder',
    4: 'Forward'
}
header = ['Id', 'WebName', 'FirstName', 'SecondName', 'DreamTeam', 'SelectedBy', 'Position', 'Team', 'GameWeek',
          'Points', 'Cost', 'NetTransfers', 'MinutesPlayed', 'Goals', 'Assists', 'CleanSheet', 'Bonus',
          'YellowCards', 'RedCards', 'GoalsConceded']

# Basic player data
def get_player_list():
    data = requests.get(bootstrap_url)
    data = data.json()['elements']
    player_data = []

    for player in data:
        try:
            summary = [player['id'], player['web_name'].encode('utf-8'), player['first_name'].encode('utf-8'),
                       player['second_name'].encode('utf-8'), player['in_dreamteam'],
                       player['selected_by_percent'].encode('utf-8'), positions[player['element_type']],
                       teams[player['team']]]
        except UnicodeDecodeError:
            summary = [player['id'], player['web_name'], player['first_name'], player['second_name'],
                       player['in_dreamteam'], player['selected_by_percent'],
                       positions[player['element_type']], teams[player['team']]]
        player_data.append(summary)

    return player_data

def get_player_stats(id):
    data = requests.get(element_url + str(id))
    data = data.json()['history']
    player_summary = []

    for fixture in data:
        match_summary = [fixture['round'], fixture['total_points'], fixture['value'], fixture['transfers_balance'],
                        fixture['minutes'], fixture['goals_scored'], fixture['assists'], fixture['clean_sheets'],
                        fixture['bonus'], fixture['yellow_cards'], fixture['red_cards'], fixture['goals_conceded']]

        player_summary.append(match_summary)

    return player_summary

def write_to_csv(file):
    #f = codecs.open(file, "w", encoding="utf-8")
    f = open(file, "w")
    f.write(','.join(header) + '\n')

    player_data = get_player_list()
    for player in player_data:
        id = player[0]
        match_stats = get_player_stats(id)
        for match in match_stats:
            row = [str(x) for x in player + match]
            f.write(','.join(row) + '\n')
    f.close()

##############################
# Main

if __name__ == "__main__":
    test_id = 2

    if test_id == 0:
        data = get_player_list()
        for player in  data:
            print(player)

    if test_id == 1:
        player_id = 2
        data = get_player_stats(player_id)
        for match in data:
            print(match)

    if test_id == 2:
        write_to_csv(output_file)
