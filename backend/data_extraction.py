import requests
from requests import HTTPError
import json
import time as time
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from creds import headers




def save_data(name : str ,data, response_code : int, division : str = None , tier : str = None, page : int = None, user : str = None, match : str = None, tagline : str = None):
    
    if response_code == 200 :
        if name == 'userByLeague':
            try : 
                with open(f'backend/data/{name}_{tier}_{division}_{page}.json', 'w', encoding='utf-8', errors='igonre') as f:
                    json.dump(data.json(), f, indent=4)
            except Exception: raise

        if name == 'matchByUser':
            try :
                with open(f'backend/data/{user}_matches.json', 'w', encoding='utf-8', errors='igonre') as f:
                    json.dump(data.json(), f, indent=4)
            except Exception: raise

        if name == 'statisticByMatch':
            try :
                with open(f'backend/data/{user}_match_stat_{match}.json', 'w', encoding='utf-8', errors='igonre') as f:
                    json.dump(data.json(), f, indent=4)
            except Exception: raise   

        if name == 'getPuuidForPlayer':
            try:
                with open(f'backend/data/{user}_{tagline}.json', 'w', encoding='utf-8', errors='igonre') as f:
                    json.dump(data.json(), f, indent=4)
            except Exception: raise   
        


def raiseError (function : str) :
    if function == 'division' :
        raise Exception('Divisions can only go from 1 to 4')
    
    if function == 'tier' :
        raise Exception('Tier can only be in : IRON, BRONZE, SILVER, GOLD, PLATINUM and DIAMOND')

    if function == 'noUserError' :
        raise Exception('Can not find selected Username')


def userByLeague (tier : str, division_int : int) :
    global page
    page = 1


    def getDivision(division_int : int) -> str:
        if division_int not in (1, 2, 3, 4) : 
            raiseError('division')
        else :
            if division_int == 1 :  
                division = 'I'
                return division
            elif division_int == 2 : 
                division = 'II' 
                return division
            elif division_int == 3 : 
                division = 'III'
                return division
            elif division_int == 4 : 
                division = 'IV'
                return division

    def getTier (tier : str) -> str:
        if tier not in ('IRON', 'BRONZE', 'SILVER', 'GOLD', 'PLATINUM', 'DIAMOND') :
            raiseError('tier')
        else :
            return tier
    
    division = getDivision(division_int)
    tier = getTier(tier)

    def yield_data(tier, division):
        global page
        response = requests.get(f'https://euw1.api.riotgames.com/tft/league/v1/entries/{tier}/{division}?queue=RANKED_TFT&page={page}', headers=headers)
        #print(f'https://euw1.api.riotgames.com/tft/league/v1/entries/{tier}/{division}?queue=RANKED_TFT&page={page}')
        yield response
        page = page + 1
        time.sleep(2) # Limitations to the number of requests is 100 requests every 2 minutes
        yield_data(tier, division)

    try :
        while True:
            for payload in yield_data(tier, division):
                save_data('userByLeague',payload, payload.status_code, division, tier, page)
    except Exception : raise 

    

def matchesByUser(username : str, region :str, match_count : int) -> str:

    def getPuuidForPlayer(userID : str, tagline  : str):
        response = requests.get(f'https://europe.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{userID}/{tagline}', headers=headers)
        save_data("getPuuidForPlayer", response,response.status_code, user = userID, tagline = tagline) 
    
    def puuIDforUsername(username : str, region : str):
        with open(f'backend/data/{username}_{region}.json', 'r', encoding='utf-8', errors='igonre') as loaded_file:    
            content = json.load(loaded_file)   
            # for every_element in content:
            #     if every_element['gameName'] == username:
            #         return every_element['puuid']
            #     else : pass 
            result = content["puuid"]
            return result
        
    getPuuidForPlayer(userID=username, tagline= region)
    user_puuid = puuIDforUsername(username, region)
    response = requests.get(f"https://europe.api.riotgames.com/tft/match/v1/matches/by-puuid/{user_puuid}/ids?start=0&count={match_count}", headers=headers)
    save_data("matchByUser", response, response.status_code, user = username)
    pass

def statisticByMatch(username : str, match_id : str = None, ):
    with open(f'backend/data/{username}_matches.json', 'r', encoding='utf-8', errors='igonre') as loaded_file:    
            content = json.load(loaded_file)
            for match in content:

                response = requests.get(f"https://europe.api.riotgames.com/tft/match/v1/matches/{match}", headers=headers)
                save_data("statisticByMatch", response, response.status_code, user = username, match = match)


def getPuuidForPlayer(userID : str, tagline : str):
    response = requests.get(f'https://europe.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{userID}/{tagline}', headers=headers)
    save_data("getPuuidForPlayer", response,response.status_code, user = userID, tagline = tagline)
    #return response


# matchesByUser() OK
# statisticByMatch() OK
# getPuuidForPlayer() OK







#################### TO DO ####################

## Get the puuid for a player

## Get 