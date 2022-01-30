import json
import requests

def get_player_id(url, name):

    r = requests.get(f"{url}/players/?name={name}")

    playerJson = r.json()

    if playerJson['count'] == 0:
        print(f"Couldn't find ID for {name} in {url}/players/?name={name}")
        return -999
    elif playerJson['count'] > 1:
        print(f"Too many IDs for {name} in {url}/players/?name={name}")
        return -999
    else:
        return playerJson['results'][0]['id']


if __name__ == '__main__':
    file = r'C:\Users\Rob\Documents\KQB\bee-awarder\IGL Team Win Awards.csv'

    url = "https://api.beegame.gg"
    headers = ""    # read auth token from file that's not on github

    # read awards spreadsheet
    f = open(file, 'r')

    sheetHeader = f.readline()

    for line in f:
        row = line.split(",")

        # lookup players
        playerID = -999
        if row[7] == "lookup":
            playerID = get_player_id(url, row[6])
        else:
            playerID = row[7]

        circuitID = int(row[3])
        awardID = int(row[1])
        roundID = int(row[5])
        statID = int(row[8].rstrip())

        # get POSTing

        awardUrl = f"{url}/awards/"
        award = {"award_category": awardID, "circuit": circuitID, "round": roundID, "player": playerID, 'stats': [{'stat_category': 14, 'total': 0}]}   # hardcoded 'NA' stat category

        print(f"requests.post({awardUrl}, json={award}, headers={headers})")
        r = requests.post(awardUrl, json=award, headers=headers)
        print(r)
        #print(r.json())





