from worker.celery import app
from record import watcher
from glb.model import Platforms

@app.task
def test():
    return True

@app.task
def track_summoners():
    ok, res = watcher.is_playing_game('2006507', Platforms.KR)
    print("track_summoners ok : {}".format(ok))

    # is not playing summoner
    if not ok:
        return

    record_replay(Platforms.KR, res['gameId'])

@app.task
def record_replay(platform, game_id):
    print('try to record_replay()')
    watcher.record(platform, game_id)
