from worker.celery import app
from record import watcher
from glb import config
from glb.model import Platforms
from glb.controllers.store import StoreController

@app.task
def test():
    return True

@app.task
def track_summoners():
    players = config.PLAYERS
    for summoner_id, region in players:
        platform = Platforms.from_region(region)
        ok, res = watcher.is_playing_game(platform, summoner_id)
        print("track_summoners summoner_id {} ok : {}".format(summoner_id, ok))

        # is not playing summoner
        if not ok:
            return
        game_id = res['gameId']

        sc = StoreController(platform, game_id)
        if not sc.version():
            record_replay(platform, game_id)

@app.task
def record_replay(platform, game_id):
    print('try to record_replay()')
    watcher.record(platform, game_id)
