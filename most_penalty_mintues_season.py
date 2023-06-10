import requests
import json


def getMostPenaltyMinutesPerSeason():
    url = 'https://records.nhl.com/site/api/skater-regular-season-scoring?cayenneExp=penaltyMinutes%20%3E=%20100%20and%20franchiseId=null%20and%20seasonId=20222023&sort=[{%22property%22:%22penaltyMinutes%22,%20%22direction%22:%22DESC%22},{%22property%22:%22gamesPlayed%22,%22direction%22:%22ASC%22},{%22property%22:%22seasonId%22,%22direction%22:%22ASC%22},{%22property%22:%22lastName%22,%22direction%22:%22ASC%22}]'
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
            penalty_minutes = record['penaltyMinutes']
            team = record['teamNames']
            player = f"{record['firstName']} {record['lastName']}"
            print(f'{player} : {team} : {penalty_minutes}')

    else:
        print('Error', response.status_code)


getMostPenaltyMinutesPerSeason()
