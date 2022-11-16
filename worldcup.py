#This script was created by Danish Siddiqui for MTA's Python Event.
from typing import List, Dict
import requests
import json
import csv


def getapiurl(endpoint: str, parameters: dict) -> str:

  #The base url is the url of the api which will return the specified requested data
  token = "uaHKOLCbUA35mY7wLI97jgXsmaS0xDohDasg0OwQ26Cfo29xJ3PtYmj9NbVK"
  base_url = f"https://soccer.sportmonks.com/api/v2.0/{endpoint}?api_token={token}"

  #Adds all the parameters into the base url
  if len(parameters) != 0:
    for key in parameters:
      base_url = base_url + f"&{key}={parameters[key]}"
  return base_url


def datatodict(url: "str") -> dict:
  #sends an HTTP request, retrives the data and converts it into a dict
  return json.loads(requests.get(url).text)


def searchteam(team_name: str) -> int:
  #searches for a team with the name team_name and outputs the team_id of the closest match
  url = getapiurl(f"teams/search/{team_name}", {})
  data = datatodict(url)['data']
  if data == []:
    print("Could not find team. Please try again.")
    return None
  else:
    return data[0]['id']


def getseason_id(year: int):
  #Gets the season_id for a specific world cup year.
  url = getapiurl("leagues/732", {"include": "seasons"})
  data = datatodict(url)['data']['seasons']['data']
  for i in range(len(data)):
    if str(year) == data[i]['name']:
      return data[i]['id']
  print("Please enter a valid world cup year from 2006-2022")
  return None


def matchgoals(fixture_id: int) -> dict:
  #gets all of the goals scored in a specific fixture
  url = getapiurl(f"fixtures/{fixture_id}", {"include": "goals"})
  data = datatodict(url)
  return data


def teamgoals(team_name: str, year: int) -> List[Dict]:
  #gets all the goals scored by all the players in a specified team (team_id) in a specified year (season_id)
  team_id = searchteam(team_name)
  season_id = getseason_id(year)
  if season_id == None:
    return {}
  else:
    url = getapiurl(f"teams/{team_id}", {
      "include": "goalscorers",
      "seasons": season_id
    })
    data = datatodict(url)
    return data['data']['goalscorers']['data']


def player(player_id: int) -> List[Dict]:
  #gets info on players based on player_id
  url = getapiurl(f"players/{player_id}", {})
  data = datatodict(url)
  if 'meta' in data:
    data.pop('meta')
    data_list = []
    data_list.append(data["data"])
  else:
    data = {}
  return data_list


def topscorers(year: int) -> List[Dict]:
  #gets top 25 scorers for the world cup season (season_id)
  season_id = getseason_id(year)
  if season_id == None:
    return {}
  else:
    url = getapiurl(f"topscorers/season/{season_id}",
                    {"include": "goalscorers.player.team"})
    data = datatodict(url)
    if 'data' not in data:
      data = {}
    else:
      data = data['data']['goalscorers']['data']
      for player in range(len(data)):
        if 'player' in data[player]:
          data[player]['player_id'] = data[player]['player']['player_id']
          data[player].pop('player')
          data[player].pop('type')
    return data


def topassist(year: int) -> List[Dict]:
  #gets top 25 assisters for the world cup season (season_id)
  season_id = getseason_id(year)
  if season_id == None:
    return {}
  else:
    url = getapiurl(f"topscorers/season/{season_id}",
                    {"include": "assistscorers.player.team"})
    data = datatodict(url)
    if 'data' not in data:
      data = {}
    else:
      data = data['data']['assistscorers']['data']
      for player in range(len(data)):
        if 'player' in data[player]:
          data[player]['player_id'] = data[player]['player_id']
          data[player].pop('player')
          data[player].pop('type')
    return data


def squad(team: str, year: int) -> List[Dict]:
  season_id = getseason_id(year)
  team_id = searchteam(team)
  if season_id == None:
    print("No Team Found")
    return {}
  else:
    url = getapiurl(f"teams/{team_id}", {"include": "squad.player"})
    data = datatodict(url)
    if 'data' not in data:
      data = {}
    else:
      data = data['data']['squad']['data']
      for i in range(len(data)):
        data[i].pop("player")
      return data


def results(year: int) -> List[Dict]:
  season_id = getseason_id(year)
  if season_id == None:
    return {}
  else:
    url = getapiurl(f"seasons/{season_id}", {"include": "results"})
    data = datatodict(url)['data']['results']['data']
    print(data[0])
    return data


def fields(data: dict) -> list:
  #gets all of the fields for a specific dict
  fields = []
  for key in data[0]:
    fields.append(key)
  return fields


def datatocsv(data: list, filename: str) -> None:
  #converts the dict data to a csv with name filename
  columns = fields(data)
  try:
    with open(filename, 'w') as csvfile:
      writer = csv.DictWriter(csvfile, fieldnames=columns)
      writer.writeheader()
      writer.writerows(data)
  except IOError:
    print("I/O error")
