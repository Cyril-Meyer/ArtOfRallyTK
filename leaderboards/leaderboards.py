import time
import requests
import tqdm


def write_data(logfile, setup_comma, data, minrank=None, maxrank=None):
    lastUserID = None
    lastRank = None
    for entry in data['leaderboard']:
        # clean ',' in strings
        for k in entry.keys():
            if type(entry[k]) == str:
                entry[k] = entry[k].replace(',', '')
        if (minrank is None or entry['rank'] > minrank) and (maxrank is None or entry['rank'] <= maxrank):
            logfile.write(setup_comma)
            logfile.write(f'{entry["rank"]},{entry["uniqueID"]},'
                          f'{entry["userName"]},{entry["score"]},'
                          f'{entry["country"]},{entry["carID"]},'
                          f'{entry["replayData"]},{entry["platformID"]}' + '\n')
            '''
            # missing userID when grabbing 5 by 5.
            if not entry['userID'] == '':
                lastUserID = entry['userID']
                lastRank = entry['rank']
            '''
    return lastUserID, lastRank


# LeaderboardsConnection (get url)
baseURL = 'https://www.funselektorfun.com/artofrally/'
getLeaderboard = baseURL + 'leaderboard'
getLeaderboardConnection = 'https://www.funselektorfun.com/absolutedrift/ping'

# BuildLeaderboardString
areas = ['Finland', 'Sardinia', 'Japan', 'Norway', 'Germany', 'Kenya']
stages = ['Stage_1', 'Stage_2', 'Stage_3', 'Stage_4', 'Stage_5', 'Stage_6']
directions = ['Forward', 'Reverse']
# weathers = ['Wet', 'Dry']
weathers = ['Dry']
carClasses = ['60s', '70s', '80s', 'GroupB', 'GroupS', 'GroupA']

headers = {
    'User-Agent': f'UnityPlayer/2019.4.18f1 (UnityWebRequest/1.0, libcurl/7.52.0-DEV)',
    'Accept': '*/*',
    'Accept-Encoding': 'identity',
    'X-Unity-Version': '2019.4.18f1',
}


for carClasse in tqdm.tqdm(carClasses):
    # create logfile
    logfile = open(f'logs/{carClasse}.csv', 'w', encoding='utf-8')
    logfile.write('area,stage,direction,weather,carClasse,')
    logfile.write('rank,uniqueID,userName,score,country,carID,replayData,platformID' + '\n')
    for area in areas:
        for stage in stages:
            for direction in directions:
                for weather in weathers:
                    setup = f'{area}_{stage}_{direction}_{weather}_{carClasse}'
                    setup_comma = f'{area},{stage},{direction},{weather},{carClasse},'

                    # url : Top = /0, AroundMe = /1, Number = /2
                    # top 10
                    url = getLeaderboard + '/' + setup + '/0/2'
                    response = requests.request('GET', url, headers=headers)
                    if response.status_code == 200:
                        data = response.json()
                        lastUserID, lastRank = write_data(logfile, setup_comma, data)
                    else:
                        raise ConnectionError
                    # 10 -> 1000
                    url = getLeaderboard + '/' + setup + f'/2/10'
                    response = requests.request('GET', url, headers=headers)
                    if response.status_code == 200:
                        data = response.json()
                        lastUserID, lastRank = write_data(logfile, setup_comma, data, 10, 1000)
                    else:
                        raise ConnectionError
                    '''
                    # around id
                    while lastUserID is not None and lastRank is not None and lastRank < 25:
                        print(lastUserID, lastRank)
                        url = getLeaderboard + '/' + setup + f'/1/2/{lastUserID}'
                        response = requests.request('GET', url, headers=headers)
                        if response.status_code == 200:
                            data = response.json()
                            lastUserID, lastRank = write_data(logfile, setup_comma, data, lastRank)
                        else:
                            raise ConnectionError
                        # we don't want to overcharge the Funselektor server
                        time.sleep(0.5)
                    '''
                    # we don't want to overcharge the Funselektor server
                    time.sleep(5.0)
    # close logfile
    logfile.close()
