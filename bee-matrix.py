from os import listdir
from os.path import isfile, join
import json
import requests


if __name__ == '__main__':

    outDir = f"."
    queenFile = f"{outDir}\\queenMatrix.tsv"
    workerFile = f"{outDir}\\workerMatrix.tsv"
    teamFile = f"{outDir}\\teamMatrix.tsv"


    # matchesURL = f"https://api.beegame.gg/matches?limit=100&round={week}&group={group}"   # https://api.beegame.gg/matches?circuit={circuit}&limit=100&round={week}
    # matchesURL = f"https://api.beegame.gg/matches?limit=100&group={group}"     # only returns playoff matches
    # matchesURL = f"https://api.beegame.gg/matches?limit=1000&circuit={circuit}"
    matchesURL = f"https://api.beegame.gg/matches?limit=1000&season=Silver"
    resultsURL = "https://api.beegame.gg/results"

    stats = {}

    circuitMap = {
        32: 'East',
        33: 'West',
        34: 'Tier 1 West',
        38: 'Tier 2 West',
        39: 'Tier 3 West',
        35: 'Tier 1 East',
        36: 'Tier 2 East',
    }


    groupMap = {
        1: 'Tier 1',
        2: 'Tier 2',
        3: 'Tier 3',
        4: 'Tier 4',
        9: 'Tier 1',
        6: 'Tier 2',
        7: 'Tier 3',
        8: 'Tier 4'
    }

    matches = requests.get(matchesURL)
    if matches.status_code != 200:
        print("ruh roh matches")

    matchJson = matches.json()

    for match in matchJson["results"]:
        matchID = match['id']

        if (match["result"] is not None) and (match["result"]["status"] != "Bye"):

            for team in ["home", "away"]:
                teamID = match[team]["id"]
                teamName = match[team]["name"]
                for player in match[team]["members"]:
                    pid = f"{player['id']}_{teamID}"
                    name = player["name"]

                    if pid not in stats:
                        stats[pid] = {}
                        stats[pid]['matches'] = {}
                        stats[pid]['sets'] = 0
                        stats[pid]['q matches'] = {}
                        stats[pid]['q sets'] = 0

                    stats[pid]["name"] = name
                    stats[pid]["id"] = player['id']
                    stats[pid]["team"] = teamName
                    stats[pid]["teamID"] = teamID

                    stats[pid]["circuit"] = circuitMap[match["circuit"]["id"]]

                    if (match["group"] is not None):
                        stats[pid]["tier"] = groupMap[match["group"]["id"]]

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
                                    # print(f"{resultID}\n")
                                    if resultID == 3621709:
                                        pidMap['Don Gero'] = 2927

                                    pKey = f"{pidMap[p['nickname']]}_{teamMap[p['team']]}"
                                    if p['entityType'] == 3:
                                        queen = True
                                    else:
                                        queen = False

                                    if pKey not in stats:
                                        print(f"Couldn't map {p['nickname']} in {resultID}")

                                    stats[pKey]['nickname'] = p['nickname']
                                    stats[pKey]['has_stats'] = True

                                    setKey += p['kills'] + p['glances'] + p['berries'] + p['berryThrowIns'] + p[
                                        'deaths'] \
                                              + p['queenKills'] + p['mostKillsPerLife'] + p['snail'] + p['snailDeaths']

                                    if queen:
                                        stats[pKey]['q matches'][matchID] = 1
                                        for stat in ['q maps', 'q kills', 'q deaths', 'q glances', 'q beans',
                                                     'any maps', 'any glances', 'q kill streak', 'q winning deaths']:
                                            if stat not in stats[pKey]:
                                                stats[pKey][stat] = 0

                                        stats[pKey]['q maps'] += numMaps
                                        stats[pKey]['any maps'] += numMaps
                                        stats[pKey]['q sets'] += 1
                                        stats[pKey]['q kills'] += p['kills']
                                        stats[pKey]['q deaths'] += p['deaths']
                                        stats[pKey]['q glances'] += p['glances']
                                        stats[pKey]['any glances'] += p['glances']
                                        stats[pKey]['q beans'] += p['berries']

                                        if stats[pKey]['team'] == winningTeam:
                                            stats[pKey]['q winning deaths'] += p['deaths']

                                        if p['mostKillsPerLife'] > stats[pKey]['q kill streak']:
                                            stats[pKey]['q kill streak'] = p['mostKillsPerLife']

                                    if not queen:
                                        stats[pKey]['matches'][matchID] = 1
                                        for stat in ['maps', 'triple', 'kills', 'warrior qk', 'kill streak', 'deaths',
                                                     'winning deaths', 'beans', 'throwIns', 'glances', 'snail units',
                                                     'snail deaths', 'any maps', 'any glances']:
                                            if stat not in stats[pKey]:
                                                stats[pKey][stat] = 0

                                        stats[pKey]['maps'] += numMaps
                                        stats[pKey]['any maps'] += numMaps
                                        stats[pKey]['sets'] += 1
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

                                gateTime1 = 0  # team 1 is gold, controls "red" gates?
                                gateTime2 = 0  # team 2 is blue, controls "blue" gates
                                for gate in g['gateControls']:
                                    gateTime1 += gate['timeAsRed']
                                    gateTime2 += gate['timeAsBlue']

                                for p in g['playerStats']:
                                    if p['nickname'] != 'TAAAAAAANK':
                                        pKey = f"{pidMap[p['nickname']]}_{teamMap[p['team']]}"

                                        if p['entityType'] == 3:
                                            queen = True
                                        else:
                                            queen = False

                                        if queen:
                                            for stat in ['q total time', 'q on last time', 'q queen kills', 'q warrior kills', 'q worker kills',
                                                         'q gate up time', 'q gate down time']:
                                                if stat not in stats[pKey]:
                                                    stats[pKey][stat] = 0

                                            stats[pKey]['q total time'] += duration
                                            if p['team'] == 2:
                                                if len(g['blueQueenKillTimes']) > 1:
                                                    stats[pKey]['q on last time'] += duration - g['blueQueenKillTimes'][
                                                        1]
                                            else:
                                                if len(g['goldQueenKillTimes']) > 1:
                                                    stats[pKey]['q on last time'] += duration - g['goldQueenKillTimes'][
                                                        1]

                                            stats[pKey]['q queen kills'] += p['totalQueenKillCount']
                                            stats[pKey]['q warrior kills'] += p['totalWarriorKillCount']
                                            stats[pKey]['q worker kills'] += p['totalWorkerKillCount']

                                            if p['team'] == 1:
                                                stats[pKey]['q gate up time'] += gateTime1
                                                stats[pKey]['q gate down time'] += gateTime2
                                            else:
                                                stats[pKey]['q gate up time'] += gateTime2
                                                stats[pKey]['q gate down time'] += gateTime1


                                        if not queen:
                                            for stat in ['total time', 'warrior up time', 'queen kills', 'warrior kills', 'worker kills', 'warrior deaths', 'worker deaths']:
                                                if stat not in stats[pKey]:
                                                    stats[pKey][stat] = 0

                                            stats[pKey]['total time'] += duration
                                            stats[pKey]['warrior up time'] += p['timeSpentAsWarriorSeconds']

                                            stats[pKey]['queen kills'] += p['totalQueenKillCount']
                                            stats[pKey]['warrior kills'] += p['totalWarriorKillCount']
                                            stats[pKey]['worker kills'] += p['totalWorkerKillCount']

                                            stats[pKey]['warrior deaths'] += p['warriorAndQueenDeathCount']
                                            stats[pKey]['worker deaths'] += p['workerDeathCount']


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
            if 'tier' not in stats[p]:
                stats[p]['tier'] = "None"

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
    f = open(f"{queenFile}", "wt", encoding='utf-8')

    f.write(
        f"Player	Team	Circuit	Tier	Matches	Sets	Maps	Match Time (s)	Queen Kills	Warrior Kills	"
        f"Worker Kills	Kill Streak	Deaths	Deaths (Map win)	Queen Beans	Glances	"
        f"Gate Control (%)	Time on Last Life (s)\n")

    for p in sorted(queenStats, key=lambda x: queenStats[x]['name']):
        gateCon = (queenStats[p]['q gate up time'] / (queenStats[p]['q gate up time'] + queenStats[p]['q gate down time'])) * 100
        matches = len(queenStats[p]['q matches'].keys())

        f.write(f"{queenStats[p]['name']}\t{queenStats[p]['team']}\t{queenStats[p]['circuit']}\t{queenStats[p]['tier']}\t")
        f.write(f"{matches}\t{queenStats[p]['q sets']}\t{queenStats[p]['q maps']}\t{queenStats[p]['q total time']:.0f}\t")
        f.write(f"{queenStats[p]['q queen kills']}\t{queenStats[p]['q warrior kills']}\t{queenStats[p]['q worker kills']}\t{queenStats[p]['q kill streak']}\t")
        f.write(f"{queenStats[p]['q deaths']}\t{queenStats[p]['q winning deaths']}\t{queenStats[p]['q beans']}\t{queenStats[p]['q glances']}\t")
        f.write(f"{gateCon:.1f}\t{queenStats[p]['q on last time']:.0f}")

        f.write("\n")
    f.close()


    f = open(f"{workerFile}", "wt", encoding='utf-8')
    f.write(
        f"Player	Team	Circuit	Tier	Matches	Sets	Maps	Match Time (s)\t"
        f"Queen Kills	Warrior Kills	Worker Kills	Kill Streak\tWarrior Uptime (s)\t"
        f"Warrior Deaths\tWorker Deaths	Deaths (on maps you won)\tSnackrifices (death by snail)\tSnail Distance\t"
        f"Berries (thrown in)\tBerries (dunked and other deposits)\tGlances (bumps, clashes and berry stuns received)\t"
        f"\n")

    for p in sorted(droneStats, key=lambda x: droneStats[x]['name']):
        matches = len(droneStats[p]['matches'].keys())

        f.write(f"{droneStats[p]['name']}\t{droneStats[p]['team']}\t{droneStats[p]['circuit']}\t{droneStats[p]['tier']}\t")
        f.write(f"{matches}\t{droneStats[p]['sets']}\t{droneStats[p]['maps']}\t{droneStats[p]['total time']:.0f}\t")
        f.write(f"{droneStats[p]['queen kills']}\t{droneStats[p]['warrior kills']}\t{droneStats[p]['worker kills']}\t{droneStats[p]['kill streak']}\t")
        f.write(f"{droneStats[p]['warrior up time']:.0f}\t")
        f.write(f"{droneStats[p]['warrior deaths']}\t{droneStats[p]['worker deaths']}\t{droneStats[p]['winning deaths']}")
        f.write(f"\t{droneStats[p]['snail deaths']}\t{droneStats[p]['snail units']}\t")
        f.write(f"{droneStats[p]['throwIns']}\t{droneStats[p]['beans'] - droneStats[p]['throwIns']}\t{droneStats[p]['glances']}\t")

        f.write("\n")
    f.close()

