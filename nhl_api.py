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
        team_info = json.loads(response_dump)

        for team in team_info['teams']:
            venue_name = team['venue']['name']
            venue_city = team['venue']['city']
            venue_tz = team['venue']['timeZone']['tz']
            first_year_play = team['firstYearOfPlay']
            conf_name = team['conference']['name']
            div_name = team['division']['name']
            team_site_url = team['officialSiteUrl']

            print(f'Venue: {venue_name}')
            print(f'City: {venue_city}')
            print(f'TimeZone: {venue_tz}')
            print(f'Est.{first_year_play}')
            print(f'\nConference: {conf_name}')
            print(f'Division: {div_name}')
            print(f'\nOfficial Site URL: {team_site_url}')

        return team_info
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

        for team in data['teams']:
            name = team['name']
            name_abbr = team['abbreviation']
            teamName = team['teamName']
            if name == team_name or teamName == team_name:
                print(f'\n{name} - {name_abbr}')
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
        getNhlTeam(team_id)

        for item in data['records']:
            team_records_arrays = [value for key,
                                   value in item.items() if key == "teamRecords"]

            for team_records_array in team_records_arrays:
                for team_record in team_records_array:
                    id = team_record['team']['id']

                    if id == team_id:
                        points = team_record['points']
                        leagueRecord = team_record['leagueRecord']
                        goalsScored = team_record['goalsScored']
                        goalsAgainst = team_record['goalsAgainst']
                        print(f'\nStandings:')
                        print(f'\tPoints: {points}')
                        print(f'\tGoals Scored: {goalsScored}')
                        print(f'\tGoals Against: {goalsAgainst}')
                        print('\tLeague Record:')
                        for key, value in leagueRecord.items():
                            if key == "type":
                                continue
                            print(f'\t\t{key}: {value}')
    else:
        print('Error', response.status_code)


team_name = input("Enter in an NHL team: ")

# team_id = getNhlTeamId(team_name)

# getNhlTeam(team_id)

getNhlStandings(team_name)
