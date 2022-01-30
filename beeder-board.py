from os import listdir
from os.path import isfile, join
import json
import requests


def printLeaderBox(category, leaders, content, colour):
    html = f"<h2 style='text-align:center;margin-bottom:10px;font-size:170%;font-family:verdana;color:{colour}'>{content[category]['name']}</h2>\n"
    html += f"<p style='text-align:center;margin:10px;font-family:verdana;color:white'>{content[category]['desc']}</p>\n"
    html += f"<img src='{leaders['top avatar'][category]}' width='128' height='128'>\n"
    # html += f"<table style='margin-left:auto; margin-right:auto;'>\n"
    html += f"<table style='width:100%'>\n"

    count = 0
    for p in leaders[category]:
        if count == 0:
            html += f"<tr><th style='text-align:right; font-family:verdana;font-size:130%; width:50%; color:{colour}'>{p}</th><th style='text-align:left;font-family:verdana;color:{colour};font-size:130%;padding-left:10px'>{leaders[category][p]}</th></tr>\n"
            count += 1
        else:
            html += f"<tr><td style='text-align:right;font-family:verdana;color:white'>{p}</td><td style='text-align:left;padding-left:10px;font-family:verdana;color:white'>{leaders[category][p]}</td></tr>\n"
    html += "</table>\n"

    return html


if __name__ == '__main__':

    week = 11
    circuit = 34

    circuitMap = {
        34: 'Tier 1 West',
        38: 'Tier 2 West',
        39: 'Tier 3 West',
        35: 'Tier 1 East',
        36: 'Tier 2 East',
    }

    group = 6

    groupMap = {
        1: 'Tier 1 West',
        2: 'Tier 2 West',
        3: 'Tier 3 West',
        4: 'Tier 4 West',
        9: 'Tier 1 East',
        6: 'Tier 2 East',
        7: 'Tier 3 East',
        8: 'Tier 4 East'
    }

    coast = "East"
    if circuit == 33:
        coast = "West"

    #title = f"BGL Beeder-board - {groupMap[group]} Week {week}"
    #title = f"BGL Beeder-board - Everybody"
    #title = f"BGL Beeder-board - {circuitMap[circuit]} - Week {week}"
    title = f"BGL Beeder-board - {circuitMap[circuit]} - Final"
    outFile = f".\\{title}"

    matchesURL = f"https://api.beegame.gg/matches?circuit={circuit}&limit=1000"
    #matchesURL = f"https://api.beegame.gg/matches?circuit={circuit}&limit=1000&round={week}"
    #matchesURL = f"https://api.beegame.gg/matches?limit=100&group={group}"     # only returns playoff matches
    #matchesURL = f"https://api.beegame.gg/matches?limit=1000&circuit={circuit}"
    #matchesURL = f"https://api.beegame.gg/matches?limit=1000&season=Bronze"
    resultsURL = "https://api.beegame.gg/results"

    shootingPerBeanMin = 50
    #mapMinimum = 6
    mapMinimum = 10

    stats = {}

    content = {}
    content['beans pm'] = {}
    content['beans pm']['name'] = "Berry Bonanza"
    #content['beans pm']['desc'] = "Worker with the most berries/map<br>Two set minimum<br>"
    content['beans pm']['desc'] = "Worker with the most berries/map<br>Ten map minimum<br>"

    content['triple'] = {}
    content['triple']['name'] = "Triple Threat"
    content['triple']['desc'] = "Most kills, berries and snail distance/map<br><br>"

    content['q kd ratio'] = {}
    content['q kd ratio']['name'] = "Queen of the Hive"
    #content['q kd ratio']['desc'] = "Queen with the most kills/death<br>Two set minimum<br>"
    content['q kd ratio']['desc'] = "Queen with the most kills/death<br>Ten map minimum<br>"

    content['snail upm'] = {}
    content['snail upm']['name'] = "Snail Whisperer"
    #content['snail upm']['desc'] = "Worker with the highest average <br>snail distance/map (2 set min)"
    content['snail upm']['desc'] = "Worker with the highest average <br>snail distance/map (10 map min)"

    content['deaths pm'] = {}
    content['deaths pm']['name'] = "Purple Heart"
    #content['deaths pm']['desc'] = "Worker with the highest deaths/map<br>on a winning team (2 set min)"
    content['deaths pm']['desc'] = "Worker with the highest deaths/map<br>on a winning team (10 map min)"

    content['kills pm'] = {}
    content['kills pm']['name'] = "Eternal Warrior"
    #content['kills pm']['desc'] = "Warrior with the most kills/map<br>Two set minimum<br>"
    content['kills pm']['desc'] = "Warrior with the most kills/map<br>Ten map minimum<br>"


    content['shooting per'] = {}
    content['shooting per']['name'] = "From Downtown!"
    content['shooting per'][
        'desc'] = f"Worker with the highest throw-ins/berry<br>({shootingPerBeanMin} berry minimum)<br>"

    content['glances pm'] = {}
    content['glances pm']['name'] = "\"Glances\""
    content['glances pm'][
        'desc'] = "Bumps? Berries? Clashes?<br>Whatever a glance is, you did it a bunch/map!"

    content['any glances pm'] = {}
    content['any glances pm']['name'] = "\"Glances\""
    content['any glances pm']['desc'] = "Bumps? Berries? Clashes?<br>Whatever a glance is, you did it a bunch/map!"

    content['snail dpm'] = {}
    content['snail dpm']['name'] = "Snackrifices"
    content['snail dpm']['desc'] = "Deaths by snail per map<br><br>"

    content['warrior qkpm'] = {}
    content['warrior qkpm']['name'] = "Regicide"
    content['warrior qkpm']['desc'] = "Warrior with the most queen kills/map<br><br>"

    content['kill streak'] = {}
    content['kill streak']['name'] = "Kill Streak"
    content['kill streak']['desc'] = "Warrior with the most kills in one life<br><br>"

    content['q glances pm'] = {}
    content['q glances pm']['name'] = "Stunned"
    content['q glances pm']['desc'] = "I really hope you were ledging for these!<br>Queen berry glances/map"

    content['q beans pm'] = {}
    content['q beans pm']['name'] = "Queen Beans"
    content['q beans pm']['desc'] = "The most important statistic/map<br><br>"

    content['q on last percent'] = {}
    content['q on last percent']['name'] = "On the Edge"
    content['q on last percent']['desc'] = "Most time spent on final queen life<br><br>"

    content['up percent'] = {}
    content['up percent']['name'] = "Warrior Uptime"
    content['up percent']['desc'] = "Most time spent with a warrior upgrade<br><br>"

    matches = requests.get(matchesURL)
    if matches.status_code != 200:
        print("ruh roh matches")

    matchJson = matches.json()

    for match in matchJson["results"]:
        matchID = match['id']

        if (match["result"] is not None) and (match["result"]["status"] != "Bye"):# and ((match["round"]["name"] == "Round 11") or (match["round"]["name"] == "Round 12"))):

            for team in ["home", "away"]:
                teamID = match[team]["id"]
                teamName = match[team]["name"]
                for player in match[team]["members"]:
                    pid = f"{player['id']}_{teamID}"
                    name = player["name"]
                    avatar = player["avatar_url"]

                    if pid not in stats:
                        stats[pid] = {}
                    stats[pid]["name"] = name
                    stats[pid]["id"] = player['id']
                    stats[pid]["team"] = teamName
                    stats[pid]["teamID"] = teamID
                    stats[pid]["avatar"] = avatar



                    if (avatar is None) or ("None.png" in avatar):
                        stats[pid]["avatar"] = "C:\\Users\\Rob\\Documents\\KQB\\emoji\\workerpogblue.png"
                    elif "embed/avatars/0.png" in avatar:
                        stats[pid]["avatar"] = "C:\\Users\\Rob\\Documents\\KQB\\emoji\\workerpoggold.png"
            if match["result"] is not None:
                resultID = match["result"]["id"]
                winningTeam = match["result"]["winner"]
                result = requests.get(f"{resultsURL}/{resultID}")

                if result.status_code != 200:
                    print(f"ruh roh result {resultID}")

                resultJson = result.json()

                pidMap = {}
                for p in resultJson["player_mappings"]:
                    pidMap[p['nickname']] = p['player']

                if resultID == 3621709:
                    pidMap['Don Gero'] = 2927

                teamMap = {}
                for t in resultJson["team_mappings"]:
                    teamMap[t['color']] = t['team']

                setHash = {}


                for s in resultJson["sets"]:
                    if s["log"] is not None:
                        numMaps = len(s["log"]["body"]["gameWinners"])

                        setKey = 0
                        setKey += numMaps

                        if "playerMatchStats" in s["log"]["body"]:
                            for p in s["log"]["body"]["playerMatchStats"]:
                                if p['nickname'] != 'TAAAAAAANK':
                                    #print(f"{resultID}\n")
                                    pKey = f"{pidMap[p['nickname']]}_{teamMap[p['team']]}"
                                    if p['entityType'] == 3:
                                        queen = True
                                    else:
                                        queen = False

                                    if pKey not in stats:
                                        print(f"Couldn't map {p['nickname']} in {resultID}")

                                    stats[pKey]['nickname'] = p['nickname']
                                    stats[pKey]['has_stats'] = True

                                    setKey += p['kills'] + p['glances'] + p['berries'] + p['berryThrowIns'] + p['deaths'] \
                                              + p['queenKills'] + p['mostKillsPerLife'] + p['snail'] + p['snailDeaths']

                                    if queen:
                                        for stat in ['q maps', 'q kills', 'q deaths', 'q glances', 'q beans', 'any maps', 'any glances']:
                                            if stat not in stats[pKey]:
                                                stats[pKey][stat] = 0

                                        stats[pKey]['q maps'] += numMaps
                                        stats[pKey]['any maps'] += numMaps
                                        stats[pKey]['q kills'] += p['kills']
                                        stats[pKey]['q deaths'] += p['deaths']
                                        stats[pKey]['q glances'] += p['glances']
                                        stats[pKey]['any glances'] += p['glances']
                                        stats[pKey]['q beans'] += p['berries']

                                    if not queen:
                                        for stat in ['maps', 'triple', 'kills', 'warrior qk', 'kill streak', 'deaths',
                                                     'winning deaths', 'beans', 'throwIns', 'glances', 'snail units',
                                                     'snail deaths', 'any maps', 'any glances']:
                                            if stat not in stats[pKey]:
                                                stats[pKey][stat] = 0

                                        stats[pKey]['maps'] += numMaps
                                        stats[pKey]['any maps'] += numMaps
                                        stats[pKey]['kills'] += p['kills']
                                        stats[pKey]['warrior qk'] += p['queenKills']
                                        stats[pKey]['deaths'] += p['deaths']
                                        stats[pKey]['beans'] += p['berries']
                                        stats[pKey]['throwIns'] += p['berryThrowIns']
                                        stats[pKey]['glances'] += p['glances']
                                        stats[pKey]['any glances'] += p['glances']
                                        stats[pKey]['snail units'] += p['snail']
                                        stats[pKey]['snail deaths'] += p['snailDeaths']

                                        if stats[pKey]['team'] == winningTeam:
                                            stats[pKey]['winning deaths'] += p['deaths']

                                        if p['mostKillsPerLife'] > stats[pKey]['kill streak']:
                                            stats[pKey]['kill streak'] = p['mostKillsPerLife']

                        if 'games' in s["log"]["body"]:
                            for g in s["log"]["body"]['games']:
                                duration = g['duration']

                                for p in g['playerStats']:
                                    if p['nickname'] != 'TAAAAAAANK':
                                        pKey = f"{pidMap[p['nickname']]}_{teamMap[p['team']]}"

                                        if p['entityType'] == 3:
                                            queen = True
                                        else:
                                            queen = False

                                        if queen:
                                            for stat in ['q total time', 'q on last time']:
                                                if stat not in stats[pKey]:
                                                    stats[pKey][stat] = 0

                                            stats[pKey]['q total time'] += duration
                                            if p['team'] == 2:
                                                if len(g['blueQueenKillTimes']) > 1:
                                                    stats[pKey]['q on last time'] += duration - g['blueQueenKillTimes'][1]
                                            else:
                                                if len(g['goldQueenKillTimes']) > 1:
                                                    stats[pKey]['q on last time'] += duration - g['goldQueenKillTimes'][1]

                                        if not queen:
                                            for stat in ['total time', 'warrior up time']:
                                                if stat not in stats[pKey]:
                                                    stats[pKey][stat] = 0

                                            stats[pKey]['total time'] += duration
                                            stats[pKey]['warrior up time'] += p['timeSpentAsWarriorSeconds']


                        if setKey in setHash:
                            print(f"Potential duplicate set in result {resultID}, match {matchID} (hash: {setKey})!!")
                        else:
                            setHash[setKey] = True

    # compute additional stats
    queenStats = {}
    droneStats = {}
    bothStats = {}
    for p in stats:
        if 'has_stats' in stats[p]:
            if 'q kills' in stats[p]:
                queenStats[p] = stats[p]
            if 'kills' in stats[p]:
                droneStats[p] = stats[p]

            bothStats[p] = stats[p]

    for p in bothStats:
        combinedGlancesPerMap = bothStats[p]['any glances'] / bothStats[p]['any maps']
        bothStats[p]['any glances pm'] = combinedGlancesPerMap

    for p in droneStats:
        # if droneStats[p]['deaths'] > 0:
        #     ratio = droneStats[p]["kills"] / droneStats[p]['deaths']
        # elif droneStats[p]["kills"] > 0:
        #     ratio = 999999 + droneStats[p]["kills"]   # add kills for secondary sort
        # else:
        #     ratio = 0
        killsPerMap = droneStats[p]["kills"] / droneStats[p]['maps']
        droneStats[p]['kills pm'] = killsPerMap

        upPercent = droneStats[p]['warrior up time'] / droneStats[p]['total time']
        droneStats[p]['up percent'] = upPercent

        beansPerMap = droneStats[p]['beans'] / droneStats[p]['maps']
        droneStats[p]['beans pm'] = beansPerMap

        if droneStats[p]['beans'] >= shootingPerBeanMin:
            shootingPer = droneStats[p]['throwIns'] / droneStats[p]['beans']
            if shootingPer == 1:
                droneStats[p]['shooting per'] = shootingPer + (
                            droneStats[p]['beans'] / 10000)  # tiny fudge to secondary sort by total beans
            else:
                droneStats[p]['shooting per'] = shootingPer
        else:
            droneStats[p]['shooting per'] = 0

        glancesPerMap = droneStats[p]['glances'] / droneStats[p]['maps']
        droneStats[p]['glances pm'] = glancesPerMap

        snailPerMap = droneStats[p]['snail units'] / droneStats[p]['maps']
        droneStats[p]['snail upm'] = snailPerMap

        snailDeathPerMap = droneStats[p]['snail deaths'] / droneStats[p]['maps']
        droneStats[p]['snail dpm'] = snailDeathPerMap + (
                    droneStats[p]['snail deaths'] / 10000)  # tiny fudge to secondary sort by total deaths

        deathPerMap = droneStats[p]['winning deaths'] / droneStats[p]['maps']
        droneStats[p]['deaths pm'] = deathPerMap

        qkPerMap = droneStats[p]['warrior qk'] / droneStats[p]['maps']
        droneStats[p]['warrior qkpm'] = qkPerMap + (droneStats[p]['warrior qk'] / 10000)  # tiny fudge for sorting

    for p in queenStats:
        if queenStats[p]['q deaths'] > 0:
            ratio = queenStats[p]["q kills"] / queenStats[p]['q deaths']
        elif queenStats[p]["q kills"] > 0:
            ratio = 999999 + queenStats[p]["q kills"]  # add kills for secondary sort
        else:
            ratio = 0
        queenStats[p]['q kd ratio'] = ratio

        glancesPerMap = queenStats[p]['q glances'] / queenStats[p]['q maps']
        queenStats[p]['q glances pm'] = glancesPerMap

        onLastPercent = queenStats[p]['q on last time'] / queenStats[p]['q total time']
        queenStats[p]['q on last percent'] = onLastPercent

        beansPerMap = queenStats[p]['q beans'] / queenStats[p]['q maps']
        queenStats[p]['q beans pm'] = beansPerMap + (
                    queenStats[p]['q beans'] / 10000)  # tiny fudge to secondary sort by total beans

    # print tables
    queenFile = f"C:\\Users\\Rob\\Documents\\KQB\\beeder-board\\queenMatrix.tsv"
    f = open(f"{queenFile}", "wt", encoding='utf-8')

    f.write(f"Player	Team	Circuit	Tier	Matches	Sets	Maps	Match Time (s)	Queen Kills	Warrior Kills	"
            f"Worker Kills	Kill Streak	Deaths	Deaths (Map win)	Berries (Thrown)	Berries (Other)	Glances	"
            f"Gate Control (%)	Time on Last Life (s)\n")
    for p in queenStats:
        f.write(f"{queenStats[p]['name']}   {queenStats[p]['team']} ")
        f.write("\n")
    f.close()

    # collect stats for categories
    tripleDepth = 0

    leaders = {}
    leaders['top avatar'] = {}
    count = 0
    leaders['kills pm'] = {}
    for p in sorted(droneStats, key=lambda x: droneStats[x]['kills pm'], reverse=True):
        if droneStats[p]['maps'] < mapMinimum:
            continue  # two set minimum

        if count == 0:
            leaders['top avatar']['kills pm'] = droneStats[p]['avatar']

        if count < 6:
            leaders['kills pm'][droneStats[p][
                'name']] = f"{droneStats[p]['kills pm']:.1f} ({droneStats[p]['kills']}/{droneStats[p]['maps']})"
            count += 1
        else:
            break

    count = 0
    for p in sorted(droneStats, key=lambda x: droneStats[x]['kills pm'], reverse=True):
        droneStats[p]['triple'] += count + (droneStats[p]['kills pm'] / 10000)  # tiny fudge for tie breaking
        if droneStats[p]['kills pm'] > 0:
            count += 1      # stop increasing rank once everybody's at zero
        #print(f"#{count} kills - {droneStats[p]['name']}: {droneStats[p]['kills pm']:.1f} ({droneStats[p]['kills']}/{droneStats[p]['maps']})")

    count = 0
    leaders['snail upm'] = {}
    for p in sorted(droneStats, key=lambda x: droneStats[x]['snail upm'], reverse=True):
        if droneStats[p]['maps'] < mapMinimum:
            continue  # two set minimum

        if count == 0:
            leaders['top avatar']['snail upm'] = droneStats[p]['avatar']

        if count < 6:
            leaders['snail upm'][droneStats[p][
                'name']] = f"{droneStats[p]['snail upm']:.0f} ({droneStats[p]['snail units']}/{droneStats[p]['maps']})"
            count += 1
        else:
            break

    count = 0
    for p in sorted(droneStats, key=lambda x: droneStats[x]['snail upm'], reverse=True):
        droneStats[p]['triple'] += count + (
                    droneStats[p]['snail upm'] / (50 * 10000))  # tiny fudge for tie breaking (snail upm/50)
        if droneStats[p]['snail upm'] > 0:
            count += 1      # stop increasing rank once everybody's at zero
        #print(f"#{count} snail - {droneStats[p]['name']}: {droneStats[p]['snail upm']:.1f} ({droneStats[p]['snail units']}/{droneStats[p]['maps']})")

    count = 0
    leaders['snail dpm'] = {}
    for p in sorted(droneStats, key=lambda x: droneStats[x]['snail dpm'], reverse=True):
        if count == 0:
            leaders['top avatar']['snail dpm'] = droneStats[p]['avatar']
        if count < 6:
            leaders['snail dpm'][droneStats[p][
                'name']] = f"{droneStats[p]['snail dpm']:.1f} ({droneStats[p]['snail deaths']}/{droneStats[p]['maps']})"
            #print(f"#{count} - {droneStats[p]['name']}: {droneStats[p]['snail upm']:.1f} ({droneStats[p]['snail units']}/{droneStats[p]['maps']})")
            count += 1
        else:
            break

    count = 0
    leaders['deaths pm'] = {}
    for p in sorted(droneStats, key=lambda x: droneStats[x]['deaths pm'], reverse=True):
        if droneStats[p]['maps'] < mapMinimum:
            continue  # two set minimum

        if count == 0:
            leaders['top avatar']['deaths pm'] = droneStats[p]['avatar']
        if count < 6:
            leaders['deaths pm'][droneStats[p][
                'name']] = f"{droneStats[p]['deaths pm']:.1f} ({droneStats[p]['winning deaths']}/{droneStats[p]['maps']})"
            # print(f"{droneStats[p]['name']}: {droneStats[p]['snail upm']:.1f} ({droneStats[p]['snail units']}/{droneStats[p]['maps']})")
            count += 1
        else:
            break

    count = 0
    leaders['beans pm'] = {}
    for p in sorted(droneStats, key=lambda x: droneStats[x]['beans pm'], reverse=True):
        if droneStats[p]['maps'] < mapMinimum:
            continue  # two set minimum

        if count == 0:
            leaders['top avatar']['beans pm'] = droneStats[p]['avatar']

        if count < 6:
            leaders['beans pm'][droneStats[p][
                'name']] = f"{droneStats[p]['beans pm']:.1f} ({droneStats[p]['beans']}/{droneStats[p]['maps']})"
            count += 1
        else:
            break

    count = 0
    for p in sorted(droneStats, key=lambda x: droneStats[x]['beans pm'], reverse=True):
        droneStats[p]['triple'] += count + (droneStats[p]['beans pm'] / 10000)  # tiny fudge for tie breaking
        if droneStats[p]['beans pm'] > 0:
            count += 1      # stop increasing rank once everybody's at zero
        #print(f"#{count} beans - {droneStats[p]['name']}: {droneStats[p]['beans pm']:.1f} ({droneStats[p]['beans']}/{droneStats[p]['maps']})")

    count = 0
    leaders['triple'] = {}
    for p in sorted(droneStats, key=lambda x: droneStats[x]['triple'], reverse=False):
        if count == 0:
            leaders['top avatar']['triple'] = droneStats[p]['avatar']
        if count < 6:
            leaders['triple'][droneStats[p][
                'name']] = f"{droneStats[p]['kills pm']:.1f}/{droneStats[p]['beans pm']:.1f}/{droneStats[p]['snail upm']:.1f}"
            print(f"#{count} - {droneStats[p]['name']}: {droneStats[p]['triple'] / 3:.1f} - {droneStats[p]['kills pm']:.1f}/{droneStats[p]['beans pm']:.1f}/{droneStats[p]['snail upm'] / 50:.1f}")
            count += 1
        else:
            #print(f"#{count} - {droneStats[p]['name']}: {droneStats[p]['triple'] / 3:.1f} - {droneStats[p]['kills pm']:.1f}/{droneStats[p]['beans pm']:.1f}/{droneStats[p]['snail upm'] / 50:.1f}")
            #count += 1
            break

    count = 0
    leaders['shooting per'] = {}
    for p in sorted(droneStats, key=lambda x: droneStats[x]['shooting per'], reverse=True):
        if count == 0:
            leaders['top avatar']['shooting per'] = droneStats[p]['avatar']
        if count < 6:
            leaders['shooting per'][droneStats[p][
                'name']] = f"{droneStats[p]['shooting per'] * 100:.0f}% ({droneStats[p]['throwIns']}/{droneStats[p]['beans']})"
            # print(f"{droneStats[p]['name']}: {droneStats[p]['beans pm']:.1f} ({droneStats[p]['beans']}/{droneStats[p]['maps']})")
            count += 1
        else:
            break

    count = 0
    leaders['glances pm'] = {}
    for p in sorted(droneStats, key=lambda x: droneStats[x]['glances pm'], reverse=True):
        if count == 0:
            leaders['top avatar']['glances pm'] = droneStats[p]['avatar']
        if count < 6:
            leaders['glances pm'][droneStats[p][
                'name']] = f"{droneStats[p]['glances pm']:.1f} ({droneStats[p]['glances']}/{droneStats[p]['maps']})"
            # print(f"{droneStats[p]['name']}: {droneStats[p]['beans pm']:.1f} ({droneStats[p]['beans']}/{droneStats[p]['maps']})")
            count += 1
        else:
            break

    count = 0
    leaders['any glances pm'] = {}
    for p in sorted(bothStats, key=lambda x: bothStats[x]['any glances pm'], reverse=True):
        if count == 0:
            leaders['top avatar']['any glances pm'] = bothStats[p]['avatar']
        if count < 6:
            leaders['any glances pm'][bothStats[p][
                'name']] = f"{bothStats[p]['any glances pm']:.1f} ({bothStats[p]['any glances']}/{bothStats[p]['any maps']})"
            # print(f"{droneStats[p]['name']}: {droneStats[p]['beans pm']:.1f} ({droneStats[p]['beans']}/{droneStats[p]['maps']})")
            count += 1
        else:
            break

    count = 0
    leaders['warrior qkpm'] = {}
    for p in sorted(droneStats, key=lambda x: droneStats[x]['warrior qkpm'], reverse=True):
        if count == 0:
            leaders['top avatar']['warrior qkpm'] = droneStats[p]['avatar']
        if count < 6:
            leaders['warrior qkpm'][droneStats[p][
                'name']] = f"{droneStats[p]['warrior qkpm']:.1f} ({droneStats[p]['warrior qk']}/{droneStats[p]['maps']})"
            # print(f"{droneStats[p]['name']}: {droneStats[p]['beans pm']:.1f} ({droneStats[p]['beans']}/{droneStats[p]['maps']})")
            count += 1
        else:
            break

    count = 0
    leaders['kill streak'] = {}
    for p in sorted(droneStats, key=lambda x: droneStats[x]['kill streak'], reverse=True):
        if count == 0:
            leaders['top avatar']['kill streak'] = droneStats[p]['avatar']
        if count < 6:
            leaders['kill streak'][droneStats[p][
                'name']] = f"{droneStats[p]['kill streak']}"
            # print(f"{droneStats[p]['name']}: {droneStats[p]['beans pm']:.1f} ({droneStats[p]['beans']}/{droneStats[p]['maps']})")
            count += 1
        else:
            break

    count = 0
    leaders['up percent'] = {}
    for p in sorted(droneStats, key=lambda x: droneStats[x]['up percent'], reverse=True):
        if count == 0:
            leaders['top avatar']['up percent'] = droneStats[p]['avatar']
        if count < 6:
            leaders['up percent'][droneStats[p][
                'name']] = f"{droneStats[p]['up percent'] * 100:.0f}% ({droneStats[p]['warrior up time']:.0f}s)" #/{droneStats[p]['total time']:.0f}s)"
            count += 1
        else:
            break

    count = 0
    leaders['q kd ratio'] = {}
    for p in sorted(queenStats, key=lambda x: queenStats[x]['q kd ratio'], reverse=True):
        if queenStats[p]['q maps'] < mapMinimum:
            continue

        if count == 0:
            leaders['top avatar']['q kd ratio'] = queenStats[p]['avatar']
        if count < 6:
            if queenStats[p]['q kd ratio'] > 999999:
                leaders['q kd ratio'][
                    queenStats[p]['name']] = f"&#8734!?! ({queenStats[p]['q kills']}/{queenStats[p]['q deaths']})"
            else:
                leaders['q kd ratio'][queenStats[p][
                    'name']] = f"{queenStats[p]['q kd ratio']:.1f} ({queenStats[p]['q kills']}/{queenStats[p]['q deaths']})"
            # print(f"{queenStats[p]['name']}: {queenStats[p]['q kd ratio']:.1f} ({queenStats[p]['q kills']}/{queenStats[p]['q deaths']})")
            count += 1
        else:
            break

    count = 0
    leaders['q glances pm'] = {}
    for p in sorted(queenStats, key=lambda x: queenStats[x]['q glances pm'], reverse=True):
        if count == 0:
            leaders['top avatar']['q glances pm'] = queenStats[p]['avatar']
        if count < 6:
            leaders['q glances pm'][queenStats[p][
                'name']] = f"{queenStats[p]['q glances pm']:.1f} ({queenStats[p]['q glances']}/{queenStats[p]['q maps']})"
            count += 1
        else:
            break

    count = 0
    leaders['q on last percent'] = {}
    for p in sorted(queenStats, key=lambda x: queenStats[x]['q on last percent'], reverse=True):
        if count == 0:
            leaders['top avatar']['q on last percent'] = queenStats[p]['avatar']
        if count < 6:
            leaders['q on last percent'][queenStats[p][
                'name']] = f"{queenStats[p]['q on last percent'] * 100:.0f}% ({queenStats[p]['q on last time']:.0f}s)" #/{queenStats[p]['q total time']:.0f}s)"
            count += 1
        else:
            break

    count = 0
    leaders['q beans pm'] = {}
    for p in sorted(queenStats, key=lambda x: queenStats[x]['q beans pm'], reverse=True):
        if count == 0:
            leaders['top avatar']['q beans pm'] = queenStats[p]['avatar']
        if count < 6:
            leaders['q beans pm'][queenStats[p][
                'name']] = f"{queenStats[p]['q beans pm']:.1f} ({queenStats[p]['q beans']}/{queenStats[p]['q maps']})"
            count += 1
        else:
            break

    # print website header
    f = open(f"{outFile}.html", "wt", encoding='utf-8')

    f.write(f"<!DOCTYPE html>\n<html>\n<head>\n<title>{title}</title>\n")

    f.write("<style>\n")
    f.write("img { border-radius: 8px; display: block; margin-left: auto; margin-right: auto; }\n")
    f.write("</style>\n")

    f.write("</head>\n<body style='background-color:#212423'>")
    mainTableStyle = "'width:1200px; margin-left:auto; margin-right:auto'"

    f.write(f"<table style={mainTableStyle}><tr>\n")

    bglLogo = f"<img src='C:\\Users\\Rob\\Documents\\KQB\\beeder-board\\logo_BGL_emblem.png' style='height:80px;width:80px;float:right'>"
    f.write(f"<td style='width:20%;vertical-align:center'>{bglLogo}</td>\n")
    f.write(
        f"<td style='vertical-align:center;text-align:center;font-family:verdana;color:white;font-size:190%'><b>{title}</b></td>\n")
    f.write(f"<td style='width:20%;vertical-align:center'></td>\n")

    # print categories
    mainTableStyle = "'width:1200px; margin-left:auto; margin-right:auto'"
    f.write(f"<table style={mainTableStyle}><tr>\n")
    f.write(
        f"<td style='width:33%;vertical-align:top'>{printLeaderBox('q kd ratio', leaders, content, '#e9aa2f')}</td>\n")
    f.write(
        f"<td style='width:33%;vertical-align:top'>{printLeaderBox('kills pm', leaders, content, '#e9aa2f')}</td>\n")
    f.write(f"<td style='vertical-align:top'>{printLeaderBox('deaths pm', leaders, content, '#e9aa2f')}</td>\n")
    f.write(f"</tr></table>\n")

    f.write(f"<br>\n")

    f.write(f"<table style={mainTableStyle}><tr>\n")
    f.write(
        f"<td style='width:33%;vertical-align:top'>{printLeaderBox('beans pm', leaders, content, '#5490cc')}</td>\n")
    f.write(
        f"<td style='width:33%;vertical-align:top'>{printLeaderBox('snail upm', leaders, content, '#5490cc')}</td>\n")
    f.write(f"<td style='vertical-align:top'>{printLeaderBox('triple', leaders, content, '#5490cc')}</td>\n")
    f.write(f"</tr></table>\n")

    f.write(f"<br>\n")

    f.write(
        f"<table style={mainTableStyle}><tr><td style='vertical-align:bottom;color:#e9aa2f;text-align:center;font-family:verdana;font-size:80%'>Stats hacked together by your friend Crankt from the amazing BGL API!</td></tr></table>\n")

    f.write("</body>\n</html>\n")
    f.close()


    # print website header
    f = open(f"{outFile} new awards.html", "wt", encoding='utf-8')

    f.write(f"<!DOCTYPE html>\n<html>\n<head>\n<title>{title} new awards</title>\n")

    f.write("<style>\n")
    f.write("img { border-radius: 8px; display: block; margin-left: auto; margin-right: auto; }\n")
    f.write("</style>\n")

    f.write("</head>\n<body style='background-color:#212423'>")
    mainTableStyle = "'width:1600px; margin-left:auto; margin-right:auto'"

    f.write(f"<table style={mainTableStyle}><tr>\n")

    bglLogo = f"<img src='C:\\Users\\Rob\\Documents\\KQB\\beeder-board\\logo_BGL_emblem.png' style='height:80px;width:80px;float:right'>"
    f.write(f"<td style='width:20%;vertical-align:center'>{bglLogo}</td>\n")
    f.write(
        f"<td style='vertical-align:center;text-align:center;font-family:verdana;color:white;font-size:200%'><b>{title}</b></td>\n")
    f.write(f"<td style='width:20%;vertical-align:center'></td>\n")

    f.write(f"<table style={mainTableStyle}><tr>\n")
    f.write(f"<td style='width:25%;vertical-align:top'>{printLeaderBox('shooting per', leaders, content,'#e9aa2f')}</td>\n")
    f.write(f"<td style='width:25%;vertical-align:top'>{printLeaderBox('any glances pm', leaders, content,'#e9aa2f')}</td>\n")
    f.write(f"<td style='width:25%;vertical-align:top'>{printLeaderBox('snail dpm', leaders, content,'#e9aa2f')}</td>\n")
    f.write(f"<td style='vertical-align:top'>{printLeaderBox('warrior qkpm', leaders, content,'#e9aa2f')}</td>\n")
    f.write(f"</tr></table>\n")

    f.write(f"<br>\n")

    f.write(f"<table style={mainTableStyle}><tr>\n")
    f.write(f"<td style='width:25%;vertical-align:top'>{printLeaderBox('kill streak', leaders, content,'#5490cc')}</td>\n")
    f.write(f"<td style='width:25%;vertical-align:top'>{printLeaderBox('up percent', leaders, content,'#5490cc')}</td>\n")
    f.write(f"<td style='width:25%;vertical-align:top'>{printLeaderBox('q on last percent', leaders, content,'#5490cc')}</td>\n")
    f.write(f"<td style='vertical-align:top'>{printLeaderBox('q beans pm', leaders, content,'#5490cc')}</td>\n")
    f.write(f"</tr></table>\n")

    f.write(f"<br>\n")

    f.write(
        f"<table style={mainTableStyle}><tr><td style='vertical-align:bottom;color:#e9aa2f;text-align:center;font-family:verdana;font-size:80%'>Stats hacked together by your friend Crankt from the amazing BGL API!</td></tr></table>\n")

    f.write("</body>\n</html>\n")
    f.close()
