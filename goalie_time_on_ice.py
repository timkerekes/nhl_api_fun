import requests
import json
from urllib.parse import urlencode


def getGoalieTimeOnIce(gameType=None, timeOnIce=None, franchiseId=None):
    gameType = int(gameType) if gameType else 2
    timeOnIce = int(timeOnIce) if timeOnIce else 300000
    franchiseId = franchiseId or 'null'

    base_url = 'https://records.nhl.com/site/api/goalie-career-stats'
    query_params = {
        'cayenneExp': f'gameTypeId = {gameType} and timeOnIce >= {timeOnIce} and franchiseId={franchiseId}',
        'sort': '[{"property":"timeOnIce","direction":"DESC"},{"property":"gamesPlayed","direction":"ASC"},{"property":"lastName","direction":"ASC"}]'
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

        print("Time On Ice :")

        for record in data['data']:
            timeOnIce = (record['timeOnIce'])
            player = f"{record['firstName']} {record['lastName']}"
            team = record['teamNames']
            print(f'\t{team} : {player}\n\t\tTime in minutes: {timeOnIce}')
            # print(f'\t{team}:')
            # print(f'\t\t{player}')
            # print(f'\t\t{save_percentage}%')

    else:
        print('Error', response.status_code)


print('\n---------------------------------------------------------------------')
print("Please fill out the following prompts to specify resulting records.")
print('---------------------------------------------------------------------\n')
gameType = input(
    "Enter Game Type (Season Stats=2, Playoff Stats=3; default=2): ")
timeOnIce = input("Enter Minimum Time On Ice (default=300000): ")
franchiseId = input("Enter Franchise ID (default=null): ")


print('\nRESULTS: ------------------------------------------------------------\n')

getGoalieTimeOnIce(gameType, timeOnIce, franchiseId)
