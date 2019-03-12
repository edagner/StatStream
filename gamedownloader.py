import os
import json
import requests

if __name__ == '__main__':
    url = 'http://www.nfl.com/liveupdate/game-center/2019020300/2019020300_gtd.json'
    game_json = requests.get(url)
    data = game_json.json()
    filename = "Superbowl_53.json"
    with open(filename, 'w') as fd:
        json.dump(data, fd)
    