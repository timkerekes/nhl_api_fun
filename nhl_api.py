import requests
import json


def getNhlTeam(team_id):
    url = f'https://statsapi.web.nhl.com/api/v1/teams/{team_id}'
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        response_dump = json.dumps(response.json(), indent=4)
        data = json.loads(response_dump)

        return data
    else:
        print('Error', response.status_code)


def getNhlTeamId(team_name):
    url = 'https://statsapi.web.nhl.com/api/v1/teams'
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        response_dump = json.dumps(response.json(), indent=4)
        data = json.loads(response_dump)

        # print(data['teams'])
        for team in data['teams']:
            name = team['name']
            teamName = team['teamName']
            if name == team_name or teamName == team_name:
                print(name)
                id = team['id']
                return id

        return ('No team found by that name...')
    else:
        print('Error', response.status_code)


def getNhlStandings(team_name):
    url = 'https://statsapi.web.nhl.com/api/v1/standings'
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        response_dump = json.dumps(response.json(), indent=4)
        data = json.loads(response_dump)

        team_id = getNhlTeamId(team_name)

        for item in data['records']:
            team_records_arrays = [value for key,
                                   value in item.items() if key == "teamRecords"]

            for team_records_array in team_records_arrays:
                for team_record in team_records_array:
                    id = team_record['team']['id']

                    if id == team_id:
                        points = team_record['points']
                        leagueRecord = team_record['leagueRecord']
                        print(f'\tPoints: {points}')
                        print('\tLeague Record:')
                        for key, value in leagueRecord.items():
                            if key == "type":
                                continue
                            print(f'\t\t{key}: {value}')
    else:
        print('Error', response.status_code)


team_name = input("Enter in an NHL team: ")

# getNhlTeam(team_id)
getNhlStandings(team_name)
