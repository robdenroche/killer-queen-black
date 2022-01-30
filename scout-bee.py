from os import listdir
from os.path import isfile, join
import json
import requests
import re

def printTeam(stats, t, teamLogos):
    logo = f"../team-logos/none.png"
    if t in teamLogos:
        logo = f"../team-logos/{teamLogos[t]}"

    html = "<br><table class='mainTable'><tr>\n"
    html += f"<td style='width:20%'><img src='{logo}' width='150'></td>\n"
    html += f"<td style='width:60%'><h1>{stats[t]['team name']} ({stats[t]['record']})</h1><td>\n"
    html += f"<td style='width:20%; vertical-align: middle;'><img src='logo_BGL_emblem.png' width=100 style='float:left'><p style='margin-top:33px; color: white; font-family: Verdana'>Silver Season</p></td></tr></table>\n"

    html += "<br><table class='mainTable'><tr>\n"
    html += "<td style='width:45%'>"
    html += "<table style='width:95%; margin-left: auto; margin-right: auto;'>\n"
    html += "<tr><th>Opponent</th><th>Sets</th><th>Maps</th><th>Eco</th><th>Mil</th><th>Snail</th></tr>\n"

    for m in sorted(stats[t]['matches'], key=lambda x: stats[t]['matches'][x]['round']):

        if 'win' in stats[t]['matches'][m]:
            outcome = 'null'
            if stats[t]['matches'][m]['win']:
                outcome = 'winners'
            else:
                outcome = 'losers'

            html += f"<tr><td class='{outcome}' style='width:40%'><p style='margin-block-start:6px; margin-block-end:6px'>{stats[t]['matches'][m]['opponent name']}</p></td>"
            html += f"<td class='{outcome}'>{stats[t]['matches'][m]['set wins']}-{stats[t]['matches'][m]['set losses']}</td>"
            html += f"<td class='{outcome}'>{stats[t]['matches'][m]['map wins']}-{stats[t]['matches'][m]['map losses']}</td>"
            html += f"<td class='{outcome}'>{stats[t]['matches'][m]['eco wins']}-{stats[t]['matches'][m]['eco losses']}</td>"
            html += f"<td class='{outcome}'>{stats[t]['matches'][m]['mil wins']}-{stats[t]['matches'][m]['mil losses']}</td>"
            html += f"<td class='{outcome}'>{stats[t]['matches'][m]['snail wins']}-{stats[t]['matches'][m]['snail losses']}</td></tr>\n"
        else:
            html += f"<tr><td class='{outcome}' style='width:40%'>{stats[t]['matches'][m]['opponent name']}</td>"
            html += f"<td colspan='5' class='{outcome}'>Match was not completed</td></tr>"

    html += "</table></td>\n"

    html += "<td><table style='width:95%; margin-left: auto; margin-right: auto;'>\n"
    html += "<tr><th>Player</th><th>Maps Played</th><th>Queen Kills</th><th>Warrior Kills</th><th>Worker Kills</th><th>Deaths</th><th>Beans</th><th>Glances</th><th>Gates & Snail</th></tr>\n"

    playerColours = {}
    playerCount = 1

    for p in sorted(stats[t]['players'], key=lambda x: stats[t]['players'][x]['name']):
        if p not in playerColours:
            playerColours[p] = f"player{playerCount}"
            playerCount += 1

        if 'q maps' in stats[t]['players'][p]:  # queens first
            html += f"<tr><td class='{playerColours[p]}'><p>{stats[t]['players'][p]['name']}</p></td>"
            html += f"<td>{stats[t]['players'][p]['q maps']}</td>"
            for stat in ['q queen kills', 'q warrior kills', 'q worker kills', 'q deaths', 'q beans', 'q glances']:
                html += f"<td>{stats[t]['players'][p][stat]/stats[t]['players'][p]['q maps']:0.1f}<br>({stats[t]['players'][p][stat]})</td>"
            html += f"<td>{(stats[t]['players'][p]['q gate up time']/(stats[t]['players'][p]['q gate up time']+stats[t]['players'][p]['q gate down time']))*100:0.0f}%</td></tr>\n"

    for p in sorted(stats[t]['players'], key=lambda x: stats[t]['players'][x]['name']):
        if 'maps' in stats[t]['players'][p]:
            html += f"<tr><td class='{playerColours[p]}'><p>{stats[t]['players'][p]['name']}</p></td>"
            html += f"<td>{stats[t]['players'][p]['maps']}</td>"
            for stat in ['queen kills', 'warrior kills', 'worker kills', 'deaths', 'beans', 'glances', 'snail units']:
                html += f"<td>{stats[t]['players'][p][stat]/stats[t]['players'][p]['maps']:0.1f}<br>({stats[t]['players'][p][stat]})</td>"
            html += "</tr>\n"

    html += "</table></td></tr></table>\n"

    mapNames = {
        'BQ': 'BQK',
        'NF': 'Flats',
        'HT': 'Helix',
        'PD': 'Pod',
        'SP': 'Spire',
        'SJ': 'Split',
        'TF': 'Tally',
        'TR': 'Throne'
    }

    html += "<br>\n"
    html += "<table class='mainTable'>\n"
    html += "<tr><th></th><th style='width:5%'>W-L</th><th style='width:5%'>Eco</th><th style='width:5%'>Mil</th><th style='width:5%'>Snail</th>"
    html += "<th style='width:5%'>Avg Time</th><th>Queen K:D</th><th style='width:5%'>Gate Con</th>"
    html += "<th style='width:13%'>Beans</th><th style='width:13%'>Glances</th><th style='width:13%'>Kills by Warriors</th><th style='width:13%'>Snail Distance</th></tr>\n"

    for m in ['BQ', 'NF', 'HT', 'PD', 'SP', 'SJ', 'TF', 'TR']:
        html += f"<tr><td><h2>{mapNames[m]}</h2></td>\n"

        if (stats[t]['maps'][m]['map wins'] + stats[t]['maps'][m]['map losses']) > 0:
            html += f"<td>{stats[t]['maps'][m]['map wins']/(stats[t]['maps'][m]['map wins'] + stats[t]['maps'][m]['map losses'])*100:.0f}%<br>"
            html += f"({stats[t]['maps'][m]['map wins']}-{stats[t]['maps'][m]['map losses']})</td>\n"
        else:
            html += "<td>-</td>"

        if (stats[t]['maps'][m]['eco wins'] + stats[t]['maps'][m]['eco losses']) > 0:
            html += f"<td>{stats[t]['maps'][m]['eco wins']/(stats[t]['maps'][m]['eco wins'] + stats[t]['maps'][m]['eco losses'])*100:.0f}%<br>"
            html += f"({stats[t]['maps'][m]['eco wins']}-{stats[t]['maps'][m]['eco losses']})</td>\n"
        else:
            html += "<td>-</td>"

        if (stats[t]['maps'][m]['mil wins'] + stats[t]['maps'][m]['mil losses']) > 0:
            html += f"<td>{stats[t]['maps'][m]['mil wins']/(stats[t]['maps'][m]['mil wins'] + stats[t]['maps'][m]['mil losses'])*100:.0f}%<br>"
            html += f"({stats[t]['maps'][m]['mil wins']}-{stats[t]['maps'][m]['mil losses']})</td>\n"
        else:
            html += "<td>-</td>"

        if (stats[t]['maps'][m]['snail wins'] + stats[t]['maps'][m]['snail losses']) > 0:
            html += f"<td>{stats[t]['maps'][m]['snail wins']/(stats[t]['maps'][m]['snail wins'] + stats[t]['maps'][m]['snail losses'])*100:.0f}%<br>"
            html += f"({stats[t]['maps'][m]['snail wins']}-{stats[t]['maps'][m]['snail losses']})</td>\n"
        else:
            html += "<td>-</td>"

        if stats[t]['maps'][m]['count'] > 0:
            html += f"<td>{stats[t]['maps'][m]['duration']/stats[t]['maps'][m]['count']:.0f}s"
        else:
            html += "<td></td>"

        html += "<td>"
        for p in sorted(stats[t]['maps'][m]['players'], key=lambda x: stats[t]['maps'][m]['players'][x]['name']):
            if 'q kills' in stats[t]['maps'][m]['players'][p]:
                queenKD = "&#8734"
                if stats[t]['maps'][m]['players'][p]['q deaths'] > 0:
                    queenKD = f"{stats[t]['maps'][m]['players'][p]['q kills']/stats[t]['maps'][m]['players'][p]['q deaths']:0.1f}"
                html += f"<mark class='{playerColours[p]}' style='margin-block-start:0px; margin-block-end:0px;'>{queenKD} ({stats[t]['maps'][m]['players'][p]['q kills']}:{stats[t]['maps'][m]['players'][p]['q deaths']})</mark><br>"
        html += "</td>"

        html += "<td>"
        for p in sorted(stats[t]['maps'][m]['players'], key=lambda x: stats[t]['maps'][m]['players'][x]['name']):
            if 'q gate down time' in stats[t]['maps'][m]['players'][p]:
                html += f"<mark class='{playerColours[p]}' style='margin-block-start:0px; margin-block-end:0px;'>" \
                        f"{(stats[t]['maps'][m]['players'][p]['q gate up time']/(stats[t]['maps'][m]['players'][p]['q gate up time'] + stats[t]['maps'][m]['players'][p]['q gate down time'])) * 100: 0.0f}%</mark><br>"
        html += "</td>"


        for stat in ['beans', 'glances', 'kills', 'snail']:
            html += "<td>"
            if stats[t]['maps'][m]['count'] > 0:
                html += f"{stats[t]['maps'][m]['totals'][stat]/stats[t]['maps'][m]['count']:0.1f} ({stats[t]['maps'][m]['totals'][stat]})<br>"
                if stats[t]['maps'][m]['totals'][stat] > 0:
                    for p in sorted(stats[t]['maps'][m]['players'], key=lambda x: stats[t]['maps'][m]['players'][x][stat], reverse=True):
                        if stats[t]['maps'][m]['players'][p][stat] > 0:
                            html += f"<mark class='{playerColours[p]}'>{(stats[t]['maps'][m]['players'][p][stat]/stats[t]['maps'][m]['totals'][stat])*100:0.0f}%</mark> "
            html += "</td>"

        html += "</tr>\n"

    html += "</table>"

    return html


if __name__ == '__main__':

    circuit = 36

    circuitMap = {
        34: 'Tier 1 West',
        38: 'Tier 2 West',
        39: 'Tier 3 West',
        35: 'Tier 1 East',
        36: 'Tier 2 East',
    }
    title = f"BGL Team Summary - {circuitMap[circuit]}"
    outFile = f"C:\\Users\\Rob\\Documents\\KQB\\scout-bee\\{title} Silver Final"

    matchesURL = f"https://api.beegame.gg/matches?circuit={circuit}&limit=1000" #&team=Penguin&teams=Stack&circuit=32"
    #matchesURL = f"https://api.beegame.gg/matches?circuit=33&team_id=1093&teams=way+too+dank&round=4"
    #https: // api.beegame.gg / matches /?round = 4 & round_is_current = & minutes = & hours = & days = & starts_in_minutes = & home = & away = & team = & team_id = 1093 & teams = way + too + dank & player = & winner = & loser = & scheduled = & awaiting_results = & status = & league = & season = & season_is_active = & circuit = 33 & group = & region = & tier = & dynasty = & dynasties = & primary_caster =
    resultsURL = "https://api.beegame.gg/results"

    stats = {}

    teamLogos = {
        1143: 'bee-ffs.png',
        1094: 'berry_brethren.png',
        1100: 'DESK_Duty.png',
        1116: 'Dr_Robotnik.png',
        1138: 'hivemates.png',
        1129: 'mozzsquad.png',
        1131: 'peachy_pandos.jpeg',
        1104: 'Penguin_Peeps.png',
        1128: 'qp_minibosses.png',
        1108: 'quaranqueen.jpg',
        1095: 'saturday_night_hive.png',
        1092: 'Vitamin_Bee.png',
        1110: 'whiskybees.png',
        1137: 'yeet-the-meat.jpeg',
        1136: '2MB.jpg',
        1091: 'badlands.png',
        1109: 'CREAM.jpg',
        1115: 'Dr_Robotnik.png',
        1096: 'garbagesnailkids.jpg',
        1097: 'hivefives.jpg',
        1141: 'honey-mustard-wings.png',
        1126: 'SLUG$.png',
        1106: 'smurfers.png',
        1093: 'Snail_Team_VI.png',
        1127: 'Soak.jpg',
        1099: 'Tear_Bears.png',
        1098: 'way-too-dank_new.png'
    }

    mapIDs = {
        14: 'SP',
        15: 'SJ',
        7: 'HT',
        2: 'PD',
        17: 'NF',
        11: 'TF',
        4: 'BQ',
        18: 'TR'
    }

    matches = requests.get(matchesURL)
    if matches.status_code != 200:
        print("ruh roh matches")

    matchJson = matches.json()

    for match in matchJson["results"]:
        matchID = match['id']

        if ((match["result"] is not None) and (match["result"]["status"] != "Bye")): #and (match["result"]["id"] != 3621609)):     # skipping Mozz playoff game!!!!



            for team in ["home", "away"]:
                teamID = match[team]["id"]
                teamName = match[team]["name"]

                if teamID not in stats:
                    stats[teamID] = {}
                    stats[teamID]['players'] = {}
                    stats[teamID]['matches'] = {}
                    stats[teamID]['maps'] = {}

                stats[teamID]['team name'] = teamName
                stats[teamID]['tier'] = "None"
                if match[team]['group'] is not None:
                    stats[teamID]['tier'] = match[team]['group']['name']
                stats[teamID]['record'] = f"{match[team]['wins']}-{match[team]['losses']}"

                if matchID not in stats[teamID]['matches']:
                    stats[teamID]['matches'][matchID] = {}


                stats[teamID]['matches'][matchID]['vod'] = match['vod_link']
                stats[teamID]['matches'][matchID]['round'] = int(re.sub('\..*','',match['round']['number']))

                if team == 'home':
                    stats[teamID]['matches'][matchID]['opponent id'] = match['away']['id']
                    stats[teamID]['matches'][matchID]['opponent name'] = match['away']['name']
                else:
                    stats[teamID]['matches'][matchID]['opponent id'] = match['home']['id']
                    stats[teamID]['matches'][matchID]['opponent name'] = match['home']['name']



                for player in match[team]["members"]:
                    pid = player['id']
                    name = player["name"]
                    avatar = player["avatar_url"]

                    if pid not in stats[teamID]['players']:
                        stats[teamID]['players'][pid] = {}

                    stats[teamID]['players'][pid]["name"] = name
                    stats[teamID]['players'][pid]["id"] = player['id']
                    stats[teamID]['players'][pid]["team"] = teamName
                    stats[teamID]['players'][pid]["teamID"] = teamID
                    # stats[teamID]['players'][pid]["avatar"] = avatar
                    #
                    # if (avatar is None) or ("None.png" in avatar):
                    #     stats[teamID]['players'][pid]["avatar"] = "C:\\Users\\Rob\\Documents\\KQB\\emoji\\workerpogblue.png"
                    # elif "embed/avatars/0.png" in avatar:
                    #     stats[teamID]['players'][pid]["avatar"] = "C:\\Users\\Rob\\Documents\\KQB\\emoji\\workerpoggold.png"
            if match["result"] is not None:
                resultID = match["result"]["id"]
                winningTeam = match["result"]["winner"]
                result = requests.get(f"{resultsURL}/{resultID}")



                if result.status_code != 200:
                    print(f"ruh roh result {resultID}")

                resultJson = result.json()

                if resultJson['status'] == 'C':     # avoid SF and DFs

                    stats[resultJson['winner']]['matches'][matchID]['win'] = True
                    stats[resultJson['loser']]['matches'][matchID]['win'] = False

                    for i in ['winner', 'loser']:
                        stats[resultJson[i]]['matches'][matchID]['set wins'] = 0
                        stats[resultJson[i]]['matches'][matchID]['set losses'] = 0
                        stats[resultJson[i]]['matches'][matchID]['map wins'] = 0
                        stats[resultJson[i]]['matches'][matchID]['map losses'] = 0
                        stats[resultJson[i]]['matches'][matchID]['eco wins'] = 0
                        stats[resultJson[i]]['matches'][matchID]['eco losses'] = 0
                        stats[resultJson[i]]['matches'][matchID]['mil wins'] = 0
                        stats[resultJson[i]]['matches'][matchID]['mil losses'] = 0
                        stats[resultJson[i]]['matches'][matchID]['snail wins'] = 0
                        stats[resultJson[i]]['matches'][matchID]['snail losses'] = 0

                        for m in ['HT', 'NF', 'SJ', 'PD', 'SP', 'TF', 'BQ', 'TR', 'players']:
                            if m not in stats[resultJson[i]]['maps']:
                                stats[resultJson[i]]['maps'][m] = {}
                                stats[resultJson[i]]['maps'][m]['players'] = {}
                                stats[resultJson[i]]['maps'][m]['map wins'] = 0
                                stats[resultJson[i]]['maps'][m]['map losses'] = 0
                                stats[resultJson[i]]['maps'][m]['eco wins'] = 0
                                stats[resultJson[i]]['maps'][m]['eco losses'] = 0
                                stats[resultJson[i]]['maps'][m]['mil wins'] = 0
                                stats[resultJson[i]]['maps'][m]['mil losses'] = 0
                                stats[resultJson[i]]['maps'][m]['snail wins'] = 0
                                stats[resultJson[i]]['maps'][m]['snail losses'] = 0
                                stats[resultJson[i]]['maps'][m]['count'] = 0
                                stats[resultJson[i]]['maps'][m]['duration'] = 0

                    pidMap = {}
                    for p in resultJson["player_mappings"]:
                        pidMap[p['nickname']] = p['player']

                    if resultID == 3621709:
                        pidMap['Don Gero'] = 2927

                    teamMap = {}
                    for t in resultJson["team_mappings"]:
                        teamMap[t['color']] = t['team']

                    setNum = 0
                    for s in resultJson["sets"]:
                        setNum += 1
                        stats[s['winner']]['matches'][matchID]['set wins'] += 1
                        stats[s['loser']]['matches'][matchID]['set losses'] += 1

                        for g in s['games']:
                            stats[g['winner']['id']]['matches'][matchID]['map wins'] += 1
                            stats[g['winner']['id']]['maps'][g['map']]['map wins'] += 1
                            stats[g['loser']['id']]['matches'][matchID]['map losses'] += 1
                            stats[g['loser']['id']]['maps'][g['map']]['map losses'] += 1

                            if g['win_condition'] == 'M':
                                stats[g['winner']['id']]['matches'][matchID]['mil wins'] += 1
                                stats[g['winner']['id']]['maps'][g['map']]['mil wins'] += 1
                                stats[g['loser']['id']]['matches'][matchID]['mil losses'] += 1
                                stats[g['loser']['id']]['maps'][g['map']]['mil losses'] += 1

                            if g['win_condition'] == 'E':
                                stats[g['winner']['id']]['matches'][matchID]['eco wins'] += 1
                                stats[g['winner']['id']]['maps'][g['map']]['eco wins'] += 1
                                stats[g['loser']['id']]['matches'][matchID]['eco losses'] += 1
                                stats[g['loser']['id']]['maps'][g['map']]['eco losses'] += 1

                            if g['win_condition'] == 'S':
                                stats[g['winner']['id']]['matches'][matchID]['snail wins'] += 1
                                stats[g['winner']['id']]['maps'][g['map']]['snail wins'] += 1
                                stats[g['loser']['id']]['matches'][matchID]['snail losses'] += 1
                                stats[g['loser']['id']]['maps'][g['map']]['snail losses'] += 1

                        if s["log"] is not None:
                            numMaps = len(s["log"]["body"]["gameWinners"])

                            if "playerMatchStats" in s["log"]["body"]:
                                for p in s["log"]["body"]["playerMatchStats"]:
                                    if p['nickname'] != 'TAAAAAAANK':
                                        #print(f"{resultID}\n")
                                        teamID = teamMap[p['team']]
                                        pKey = pidMap[p['nickname']]
                                        if p['entityType'] == 3:
                                            queen = True
                                        else:
                                            queen = False

                                        if pKey not in stats[teamID]['players']:
                                            print(f"Couldn't map {p['nickname']} in {resultID} set {setNum}")

                                        stats[teamID]['players'][pKey]['nickname'] = p['nickname']
                                        stats[teamID]['players'][pKey]['has_stats'] = True

                                        if queen:
                                            for stat in ['q maps', 'q kills', 'q deaths', 'q glances', 'q beans', 'any maps', 'any glances']:
                                                if stat not in stats[teamID]['players'][pKey]:
                                                    stats[teamID]['players'][pKey][stat] = 0

                                            stats[teamID]['players'][pKey]['q maps'] += numMaps
                                            stats[teamID]['players'][pKey]['any maps'] += numMaps
                                            stats[teamID]['players'][pKey]['q kills'] += p['kills']
                                            stats[teamID]['players'][pKey]['q deaths'] += p['deaths']
                                            stats[teamID]['players'][pKey]['q glances'] += p['glances']
                                            stats[teamID]['players'][pKey]['any glances'] += p['glances']
                                            stats[teamID]['players'][pKey]['q beans'] += p['berries']

                                        if not queen:
                                            for stat in ['maps', 'triple', 'kills', 'warrior qk', 'kill streak', 'deaths',
                                                         'winning deaths', 'beans', 'throwIns', 'glances', 'snail units',
                                                         'snail deaths', 'any maps', 'any glances']:
                                                if stat not in stats[teamID]['players'][pKey]:
                                                    stats[teamID]['players'][pKey][stat] = 0

                                            stats[teamID]['players'][pKey]['maps'] += numMaps
                                            stats[teamID]['players'][pKey]['any maps'] += numMaps
                                            stats[teamID]['players'][pKey]['kills'] += p['kills']
                                            stats[teamID]['players'][pKey]['warrior qk'] += p['queenKills']
                                            stats[teamID]['players'][pKey]['deaths'] += p['deaths']
                                            stats[teamID]['players'][pKey]['beans'] += p['berries']
                                            stats[teamID]['players'][pKey]['throwIns'] += p['berryThrowIns']
                                            stats[teamID]['players'][pKey]['glances'] += p['glances']
                                            stats[teamID]['players'][pKey]['any glances'] += p['glances']
                                            stats[teamID]['players'][pKey]['snail units'] += p['snail']
                                            stats[teamID]['players'][pKey]['snail deaths'] += p['snailDeaths']

                                            if stats[teamID]['players'][pKey]['team'] == winningTeam:
                                                stats[teamID]['players'][pKey]['winning deaths'] += p['deaths']

                                            if p['mostKillsPerLife'] > stats[teamID]['players'][pKey]['kill streak']:
                                                stats[teamID]['players'][pKey]['kill streak'] = p['mostKillsPerLife']

                            if 'games' in s["log"]["body"]:
                                gameCount = 0

                                for g in s['log']['body']['games']:     # need to handle both teams in here

                                    m = mapIDs[s["log"]["body"]['mapPool'][gameCount]]
                                    gameCount += 1

                                    duration = g['duration']

                                    stats[s['winner']]['maps'][m]['duration'] += g['duration']
                                    stats[s['winner']]['maps'][m]['count'] += 1

                                    stats[s['loser']]['maps'][m]['duration'] += g['duration']
                                    stats[s['loser']]['maps'][m]['count'] += 1

                                    gateTime1 = 0   # team 1 is gold, controls "red" gates?
                                    gateTime2 = 0   # team 2 is blue, controls "blue" gates
                                    for gate in g['gateControls']:
                                        gateTime1 += gate['timeAsRed']
                                        gateTime2 += gate['timeAsBlue']

                                    for p in g['playerStats']:
                                        if p['nickname'] != 'TAAAAAAANK':
                                            teamID = teamMap[p['team']]
                                            pKey = pidMap[p['nickname']]

                                            if p['entityType'] == 3:
                                                queen = True
                                            else:
                                                queen = False

                                            if pKey not in stats[teamID]['maps'][m]['players']:
                                                stats[teamID]['maps'][m]['players'][pKey] = {}

                                            if 'totals' not in stats[teamID]['maps'][m]:
                                                stats[teamID]['maps'][m]['totals'] = {}

                                            if queen:
                                                for stat in ['q total time', 'q on last time', 'q queen kills', 'q warrior kills', 'q worker kills', 'q gate up time', 'q gate down time',]:
                                                    if stat not in stats[teamID]['players'][pKey]:
                                                        stats[teamID]['players'][pKey][stat] = 0

                                                for stat in ['q beans', 'glances', 'q kills', 'q deaths', 'q gate up time', 'q gate down time', 'beans', 'kills', 'snail']:
                                                    if stat not in stats[teamID]['maps'][m]['players'][pKey]:
                                                        stats[teamID]['maps'][m]['players'][pKey][stat] = 0
                                                    if stat not in stats[teamID]['maps'][m]['totals']:
                                                        stats[teamID]['maps'][m]['totals'][stat] = 0

                                                stats[teamID]['players'][pKey]['q total time'] += duration
                                                if p['team'] == 2:
                                                    if len(g['blueQueenKillTimes']) > 1:
                                                        stats[teamID]['players'][pKey]['q on last time'] += duration - g['blueQueenKillTimes'][1]
                                                else:
                                                    if len(g['goldQueenKillTimes']) > 1:
                                                        stats[teamID]['players'][pKey]['q on last time'] += duration - g['goldQueenKillTimes'][1]

                                                stats[teamID]['players'][pKey]['q queen kills'] += p['totalQueenKillCount']
                                                stats[teamID]['players'][pKey]['q warrior kills'] += p['totalWarriorKillCount']
                                                stats[teamID]['players'][pKey]['q worker kills'] += p['totalWorkerKillCount']

                                                stats[teamID]['maps'][m]['players'][pKey]['name'] = p['nickname']
                                                stats[teamID]['maps'][m]['players'][pKey]['q beans'] += p['totalBerryDeposits']
                                                stats[teamID]['maps'][m]['players'][pKey]['glances'] += p['totalGlanceCount']
                                                stats[teamID]['maps'][m]['players'][pKey]['q kills'] += p['totalKillCount']
                                                stats[teamID]['maps'][m]['players'][pKey]['q deaths'] += p['totalDeathCount']

                                                if p['team'] == 1:
                                                    stats[teamID]['players'][pKey]['q gate up time'] += gateTime1
                                                    stats[teamID]['players'][pKey]['q gate down time'] += gateTime2
                                                    stats[teamID]['maps'][m]['players'][pKey]['q gate up time'] += gateTime1
                                                    stats[teamID]['maps'][m]['players'][pKey]['q gate down time'] += gateTime2
                                                else:
                                                    stats[teamID]['players'][pKey]['q gate up time'] += gateTime2
                                                    stats[teamID]['players'][pKey]['q gate down time'] += gateTime1
                                                    stats[teamID]['maps'][m]['players'][pKey]['q gate up time'] += gateTime2
                                                    stats[teamID]['maps'][m]['players'][pKey]['q gate down time'] += gateTime1

                                                stats[teamID]['maps'][m]['totals']['q beans'] += p['totalBerryDeposits']
                                                stats[teamID]['maps'][m]['totals']['glances'] += p['totalGlanceCount']
                                                stats[teamID]['maps'][m]['totals']['q kills'] += p['totalKillCount']
                                                stats[teamID]['maps'][m]['totals']['q deaths'] += p['totalDeathCount']

                                            if not queen:
                                                for stat in ['total time', 'warrior up time', 'queen kills', 'warrior kills', 'worker kills']:
                                                    if stat not in stats[teamID]['players'][pKey]:
                                                        stats[teamID]['players'][pKey][stat] = 0

                                                for stat in ['beans', 'glances', 'kills', 'deaths', 'snail']:
                                                    if stat not in stats[teamID]['maps'][m]['players'][pKey]:
                                                        stats[teamID]['maps'][m]['players'][pKey][stat] = 0
                                                    if stat not in stats[teamID]['maps'][m]['totals']:
                                                        stats[teamID]['maps'][m]['totals'][stat] = 0

                                                stats[teamID]['players'][pKey]['total time'] += duration
                                                stats[teamID]['players'][pKey]['warrior up time'] += p['timeSpentAsWarriorSeconds']
                                                stats[teamID]['players'][pKey]['queen kills'] += p['totalQueenKillCount']
                                                stats[teamID]['players'][pKey]['warrior kills'] += p['totalWarriorKillCount']
                                                stats[teamID]['players'][pKey]['worker kills'] += p['totalWorkerKillCount']

                                                stats[teamID]['maps'][m]['players'][pKey]['name'] = p['nickname']
                                                stats[teamID]['maps'][m]['players'][pKey]['beans'] += p['totalBerryDeposits']
                                                stats[teamID]['maps'][m]['players'][pKey]['glances'] += p['totalGlanceCount']
                                                stats[teamID]['maps'][m]['players'][pKey]['kills'] += p['totalKillCount']
                                                stats[teamID]['maps'][m]['players'][pKey]['deaths'] += p['totalDeathCount']
                                                stats[teamID]['maps'][m]['players'][pKey]['snail'] += p['totalSnailDistance']

                                                stats[teamID]['maps'][m]['totals']['beans'] += p['totalBerryDeposits']
                                                stats[teamID]['maps'][m]['totals']['glances'] += p['totalGlanceCount']
                                                stats[teamID]['maps'][m]['totals']['kills'] += p['totalKillCount']
                                                stats[teamID]['maps'][m]['totals']['deaths'] += p['totalDeathCount']
                                                stats[teamID]['maps'][m]['totals']['snail'] += p['totalSnailDistance']




    # print website header
    f = open(f"{outFile}.html", "wt", encoding='utf-8')

    f.write(f"<!DOCTYPE html>\n<html>\n<head>\n<title>{title}</title>\n")

    f.write("<style>\n")
    f.write("img { border-radius: 8px; display: block; margin-left: auto; margin-right: auto; }\n")
    f.write(".mainTable { width:1200px; margin-left: auto; margin-right: auto; }\n")
    f.write("h1 { text-align:center; color: white; font-family: Verdana; font-size: 250%; }\n")
    f.write("h2 { text-align:left; color: white; font-family: Verdana; font-size: 150%; }\n")
    f.write("th { text-align:center; color: white; font-family: Verdana; margin-block-start:12px margin-block-end:12px}\n")
    f.write("td { text-align:center; color: white; font-family: Verdana; }\n")
    f.write(".winners { text-align:center; color: white; font-family: Verdana; background-color:#144543}\n")
    f.write(".player1 { text-align:center; color: white; font-family: Verdana; background-color:#332288}\n")
    f.write(".player2 { text-align:center; color: white; font-family: Verdana; background-color:#0077BB}\n")
    f.write(".player3 { text-align:center; color: white; font-family: Verdana; background-color:#228833}\n")
    f.write(".player4 { text-align:center; color: white; font-family: Verdana; background-color:#999933}\n")
    f.write(".player5 { text-align:center; color: white; font-family: Verdana; background-color:#EE6677}\n")
    f.write(".player6 { text-align:center; color: white; font-family: Verdana; background-color:#AA3377}\n")
    f.write(".player7 { text-align:center; color: white; font-family: Verdana; background-color:#000000}\n")
    f.write("@media print { .pagebreak { page-break-before: always; } }\n")
    f.write("</style>\n")

    f.write("</head>\n<body style='background-color:#212423'>\n")

    for t in sorted(stats, key=lambda x: stats[x]['team name']):
        f.write(printTeam(stats, t, teamLogos))
        f.write(
            f"<br><table class='mainTable'><tr><td style='vertical-align:bottom;color:#e9aa2f;text-align:center;font-family:verdana;font-size:80%'>Stats hacked together by your friend Crankt from the amazing BGL API</td></tr></table>\n")
        f.write("<div class='pagebreak'> </div>")

    f.write("</body>\n</html>\n")
    f.close()



