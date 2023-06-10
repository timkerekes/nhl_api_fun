import requests
import json


def getMostGoalsPerGamePerSeason():
    url = 'https://records.nhl.com/site/api/team-season-record-and-scoring?cayenneExp=gameTypeId%20=%202%20and%20goalsPerGame%20%3E=%203%20and%20seasonId%20=%2020222023&sort=[{%22property%22:%22goalsPerGame%22,%20%22direction%22:%22DESC%22},{%22property%22:%22gamesPlayed%22,%22direction%22:%22ASC%22},{%22property%22:%22seasonId%22,%22direction%22:%22ASC%22}]'
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
    }

    response = requests.get(url, headers)

    if response.status_code == 200:
        response_dump = json.dumps(response.json(), indent=4)
        data = json.loads(response_dump)

        for record in data['data']:
            seasonId = record['seasonId']
            # if seasonId == 20222023:
            goals = record['goals']
            team = record['teamName']
            print(f'{team} : {goals}')

    else:
        print('Error', response.status_code)


getMostGoalsPerGamePerSeason()
