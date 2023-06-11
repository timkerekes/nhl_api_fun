import requests
import json
import datetime
from urllib.parse import urlencode


def getMostPenaltyMinutesPerSeason(penaltyMinutes=None, franchiseId=None, seasonId=None):
    penaltyMinutes = int(penaltyMinutes) if penaltyMinutes else 300
    franchiseId = franchiseId or 'null'

    base_url = 'https://records.nhl.com/site/api/skater-regular-season-scoring'
    query_params = {
        'cayenneExp': f'(penaltyMinutes >= {penaltyMinutes} and franchiseId = {franchiseId})',
        'sort': '[{"property":"penaltyMinutes", "direction":"DESC"}, {"property":"gamesPlayed", "direction":"ASC"}, {"property":"seasonId", "direction":"ASC"}, {"property":"lastName", "direction":"ASC"}]'
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
            seasonId = record['seasonId']
            penalty_minutes = record['penaltyMinutes']
            team = record['teamNames']
            player = f"{record['firstName']} {record['lastName']}"
            print(f'{player} : {team} : {penalty_minutes}')

    else:
        print('Error', response.status_code)


print('\n---------------------------------------------------------------------')
print("Please fill out the following prompts to specify resulting records.")
print('---------------------------------------------------------------------\n')
penaltyMinutes = input(
    "Enter Minimum Penalty Minutes (default=300): ")
franchiseId = input("Enter Franchise ID (default=null): ")
seasonId = input(
    "Enter Season Year (Ex.20222023; default=All Seasons): ")

print('\nRESULTS: ------------------------------------------------------------\n')


getMostPenaltyMinutesPerSeason(penaltyMinutes, franchiseId, seasonId)
