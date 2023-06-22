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

            all_team_info = (
                f'Venue: {venue_name}\n'
                f'City: {venue_city}\n'
                f'TimeZone: {venue_tz}\n'
                f'Est.{first_year_play}\n'
                f'\nConference: {conf_name}\n'
                f'Division: {div_name}\n'
                f'\nOfficial Site URL: {team_site_url}'
            )

            # print(f'Venue: {venue_name}')
            # print(f'City: {venue_city}')
            # print(f'TimeZone: {venue_tz}')
            # print(f'Est.{first_year_play}')
            # print(f'\nConference: {conf_name}')
            # print(f'Division: {div_name}')
            # print(f'\nOfficial Site URL: {team_site_url}')

        return all_team_info
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
            name_lowered = name.lower()
            name_abbr = team['abbreviation']
            teamName = team['teamName']
            teamName_lowered = teamName.lower()
            team_name_lowered = team_name.lower()
            if name_lowered == team_name_lowered or teamName_lowered == team_name_lowered:
                # print(f'{name} - {name_abbr}')
                output = f'{name} - {name_abbr}'
                id = team['id']
                return output, id
            
            error_message = 'No Team Found By That Name...\n\nPlease Try Again'
            error_id = -1

        return error_message, error_id
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

        team_name_output, team_id = getNhlTeamId(team_name)
        if team_id == -1:
            return team_name_output
        
        team_info = getNhlTeam(team_id)

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

                        # print(f'\nStandings:')
                        # print(f'\tPoints: {points}')
                        # print(f'\tGoals Scored: {goalsScored}')
                        # print(f'\tGoals Against: {goalsAgainst}')
                        # print('\tLeague Record:')
                        # for key, value in leagueRecord.items():
                        #     if key == "type":
                        #         continue
                        #     print(f'\t\t{key}: {value}')
                        
                        standings = (
                            f'\nStandings:'
                            f'\n\tPoints: {points}'
                            f'\n\tGoals Scored: {goalsScored}'
                            f'\n\tGoals Against: {goalsAgainst}'
                            f'\n\tLeague Record:'
                            + ''.join([f'\n\t\t{key}: {value}' for key, value in leagueRecord.items() if key != 'type'])
                        )

                        return f'{team_name_output}\n{team_info}\n{standings}'

    else:
        print('Error', response.status_code)


# print('\n---------------------------------------------------------------------')
# print("Please fill out the following prompts to specify resulting records.")
# print('---------------------------------------------------------------------\n')
# team_name = input("Enter in an NHL team: ")

# print('\nRESULTS: ------------------------------------------------------------\n')

# # team_id = getNhlTeamId(team_name)

# # getNhlTeam(team_id)

# getNhlStandings(team_name)
