from worker.celery import app
from record import watcher
from glb.model import Platforms, ReplayData
from glb.controllers.redis import redis

@app.task
def test():
    return True

@app.task
def track_summoners():
    ok, res = watcher.is_playing_game('17140249', Platforms.KR)
    print("track_summoners ok : {}".format(ok))

    # is not playing summoner
    if not ok:
        return
    game_id = res['gameId']
    platform = Platforms.KR

    data_info_key = ReplayData.data_info_key(platform, game_id)
    if not redis.keys(data_info_key):
        record_replay(platform, game_id)

@app.task
def record_replay(platform, game_id):
    print('try to record_replay()')
    watcher.record(platform, game_id)
