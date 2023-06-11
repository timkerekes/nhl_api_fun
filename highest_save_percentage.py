import requests
import json
import datetime
from urllib.parse import urlencode


def getHighestSavePercentage(gameType=None, percentage=None, gamesPlayed=None, franchiseId=None, seasonId=None):
    gameType = int(gameType) if gameType else 2
    percentage = float(percentage) if percentage else 0
    gamesPlayed = int(gamesPlayed) if gamesPlayed else 25
    franchiseId = franchiseId or 'null'
    seasonId = seasonId if seasonId else f"{datetime.datetime.now().year-1}{datetime.datetime.now().year}"

    base_url = 'https://records.nhl.com/site/api/goalie-season-stats'
    query_params = {
        'cayenneExp': f'gameType = {gameType} and savePctg > {percentage} and gamesPlayed >= {gamesPlayed} and franchiseId={franchiseId} and seasonId={seasonId}',
        'sort': '[{"property":"savePctg","direction":"DESC"},{"property":"gamesPlayed","direction":"DESC"},{"property":"lastName","direction":"ASC"}]'
    }
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
    }

    url = f'{base_url}?{urlencode(query_params)}'

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        response_dump = json.dumps(response.json(), indent=4)
        data = json.loads(response_dump)

        print("Save Percentage :")

        for record in data['data']:
            save_percentage = record['savePctg'] * 100
            player = f"{record['firstName']} {record['lastName']}"
            team = record['teamNames']
            print(f'\t{team} : {player} : {save_percentage}%')

    else:
        print('Error', response.status_code)


print("Please fill out the following prompts to specify resulting records.")
gameType = input(
    "Enter Game Type (Season Stats=2, Playoff Stats=3; default=2): ")
percentage = input(
    "Enter Minimum Save Percentage (Range from 0-1; default=0): ")
gamesPlayed = input("Enter Minimum Games Played (default=25): ")
franchiseId = input("Enter Franchise ID if known (default=null): ")
seasonId = input(
    "Enter Season/Playoff Year (Format='yearyear' Example:20222023 default=Last Completed Season (20222023)): ")


getHighestSavePercentage(gameType, percentage,
                         gamesPlayed, franchiseId, seasonId)
