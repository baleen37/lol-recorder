#
import time
import json

from glb.helpers.apis import LoLApi, SpectatorApi
from glb.model import Platforms, ReplayData
from glb import config
from record.app import redis
from worker import tasks


def is_playing_game(summoner_id, platform):
    res = LoLApi().current_game_info(summoner_id, platform)

    if not res.ok:
        return False, 'is not playing game'

    data = json.loads(res.text)
    if int(data['mapId']) != 11:
        return False, 'mapId is not 11'

    if data['gameMode'] != 'CLASSIC':
        return False, 'gameMode'

    #game_length = res['gameLength']
    #participants = res['participants'] 

    #game_id = res['gameId']
    #encryption_key = res['observer']['encryptionKey']
    #platform_id = res['platformId']

    return True, data

def record(platform, game_id, first_chunk=None, first_key_frame=None, 
           last_chunk=None, last_key_frame=None):

    data_info_key = ReplayData.data_info_key(platform, game_id)

    first_chunk = int(redis.hget(data_info_key, 'first_chunk') or 0)
    first_key_frame = int(redis.hget(data_info_key,'first_chunk') or 0)
    last_chunk = int(redis.hget(data_info_key, 'last_chunk') or 0)
    last_key_frame = int(redis.hget(data_info_key, 'last_key_frame') or 0)

    res = SpectatorApi.get_last_chunk_info(platform, game_id)
    if not res.ok:
        print('fail SpectatorApi.get_last_chunk_info')

    try:
        chunk = res.json()
    except Exception as e:
        print(e)
        print(res.text)

    chunk_id = int(chunk['chunkId'])
    start_game_chunk_id = int(chunk['startGameChunkId'])
    key_frame_id = int(chunk['keyFrameId'])
    next_chunk_id = int(chunk['nextChunkId'])

    #set inital values
    if not first_chunk:
        if chunk_id > start_game_chunk_id:
            first_chunk = chunk_id
        else:
            first_chunk = start_game_chunk_id

        if key_frame_id > 0:
            first_key_frame = key_frame_id
        else:
            first_key_frame = 1

        last_chunk = chunk_id
        last_key_frame = key_frame_id

        # store init chunk and frame
        redis.hset(data_info_key, ReplayData.chunk_frame_key(chunk_id), 
                  SpectatorApi.get_chunk_frame(platform, game_id, chunk_id).text)

        redis.hset(data_info_key, ReplayData.frame_key(key_frame_id),
                  SpectatorApi.get_key_frame(platform, game_id, key_frame_id).text)

    if start_game_chunk_id > first_chunk:
        first_chunk = start_game_chunk_id

    # get all chunk
    if chunk_id > last_chunk:
        for i in range(last_chunk + 1, chunk_id + 1):
            redis.hset(data_info_key, ReplayData.chunk_frame_key(i), 
                      SpectatorApi.get_chunk_frame(platform, game_id, i).text)

    # 혹시 모르니.
    if next_chunk_id < chunk_id and next_chunk_id > 0:
        redis.hset(data_info_key, ReplayData.chunk_frame_key(next_chunk_id), 
                  SpectatorApi.get_chunk_frame(platform, game_id, next_chunk_id).text)

    # get all key frame data
    if key_frame_id > last_key_frame:
        for i in range(last_key_frame+ 1, key_frame_id + 1):
            redis.hset(data_info_key, ReplayData.frame_key(i),
                      SpectatorApi.get_key_frame(platform, game_id, i).text)

    last_chunk = chunk_id
    last_key_frame = key_frame_id

    # the game is over
    if int(chunk['endGameChunkId']) == chunk_id:
        print('the game is over {}'.format(game_id))
        return

    redis.hmset(data_info_key, {
        'first_chunk': first_chunk,
        'first_key_frame': first_key_frame,
        'last_chunk': last_chunk,
        'last_key_frame': last_key_frame
    })

    next_time = int(chunk["nextAvailableChunk"]) / 1000 + 1

    # retry to next
    tasks.record_replay.apply_async(
        args=[platform, game_id], countdown=10)
