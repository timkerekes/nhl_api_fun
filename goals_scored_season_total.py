import requests
import json
import datetime
from urllib.parse import urlencode


def getMostGoalsPerGamePerSeason(gameType=None, goalsPerGame=None, seasonId=None):
    gameType = int(gameType) if gameType else 2
    goalsPerGame = int(goalsPerGame) if goalsPerGame else 3
    # seasonId = seasonId if seasonId else f"{datetime.datetime.now().year-1}{datetime.datetime.now().year}"

    base_url = 'https://records.nhl.com/site/api/team-season-record-and-scoring'
    query_params = {
        'cayenneExp': f'gameTypeId = {gameType} and goalsPerGame >= {goalsPerGame}',
        'sort': '[{"property":"goalsPerGame", "direction":"DESC"}, {"property":"gamesPlayed", "direction":"ASC"}, {"property":"seasonId", "direction":"ASC"}]'
    }

    if seasonId is not None and seasonId != '':
        query_params['cayenneExp'] += f' and seasonId = {seasonId}'

    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
    }

    url = f'{base_url}?{urlencode(query_params)}'

    response = requests.get(url, headers)

    if response.status_code == 200:
        response_dump = json.dumps(response.json(), indent=4)
        data = json.loads(response_dump)

        for record in data['data']:
            goals = record['goals']
            team = record['teamName']
            gamesPlayed = record['gamesPlayed']
            goalsPerGame = record['goalsPerGame']
            print(f'\n{team}:')
            print(f'\tGoals Per Game: {goalsPerGame}')
            print(f'\tGames Played: {gamesPlayed}')
            print(f'\tGoals: {goals}')

    else:
        print('Error', response.status_code)


print('\n---------------------------------------------------------------------')
print("Please fill out the following prompts to specify resulting records.")
print('---------------------------------------------------------------------\n')
gameType = input(
    "Enter Game Type (Season Stats=2, Playoff Stats=3; default=2): ")
goalsPerGame = input(
    "Enter Minimum Goals Per Game (Range from 0-6; default=3): ")
seasonId = input(
    "Enter Season Year (Ex. 20222023; default=All Seasons): ")

print('\nRESULTS: ------------------------------------------------------------\n')

getMostGoalsPerGamePerSeason(gameType, goalsPerGame, seasonId)
