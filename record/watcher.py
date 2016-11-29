#
import time
import json

from glb import config
from glb.helpers.apis import LoLApi, SpectatorApi
from glb.model import Platforms
from glb.controllers.store import StoreController


def is_playing_game(platform, summoner_id):
    '''
    플레이 여부체크
    '''
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

def record(platform, game_id):
    print('try to record platform : {}, game_id : {}'.format(platform.name, game_id))
    sc = StoreController(platform, game_id)

    # version
    version = SpectatorApi.get_version(platform).text
    sc.set_version(version)
    print("version : {}".format(version))

    meta_data = SpectatorApi.get_meta_data(platform, game_id).json()

    while True:
        chunk = SpectatorApi.get_last_chunk_info(platform, game_id).json()

        chunk_id = int(chunk['chunkId'])
        start_game_chunk_id = int(chunk['startGameChunkId'])
        key_frame_id = int(chunk['keyFrameId'])
        next_chunk_id = int(chunk['nextChunkId'])

        #이제 3분 옵저버 제한타임 지남.
        if chunk_id > meta_data['endStartupChunkId']:
            break

        # 다음 chunk 시간 대기.
        time.sleep(chunk['nextAvailableChunk'] / 1000 + 1)

    # new meta data
    meta_data = SpectatorApi.get_meta_data(platform, game_id).json()
    sc.set_meta_data(meta_data)
    
    #for i in range(meta_data['endStartupChunkId'] + 2):
    #    while True:
    #        chunk = SpectatorApi.get_last_chunk_info(platform, game_id).text

    #        if i > chunk['chunkId']:
    #            time.sleep(chunk['nextAvailableChunk'] / 1000 + 1)
    #            contiune

    first_chunk = 0
    first_key_frame = 0
    last_chunk = 0
    last_key_frame = 0

    while True:
        chunk = SpectatorApi.get_last_chunk_info(platform, game_id).json()

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
            sc.set_chunk_frame(chunk_id, SpectatorApi.get_chunk_frame(platform, game_id, chunk_id).text)
            sc.set_key_frame(key_frame_id, SpectatorApi.get_key_frame(platform, game_id, key_frame_id).text)

        if start_game_chunk_id > first_chunk:
            first_chunk = start_game_chunk_id

        # get all chunk
        if chunk_id > last_chunk:
            for i in range(last_chunk + 1, chunk_id + 1):
                sc.set_chunk_frame(i, SpectatorApi.get_chunk_frame(platform, game_id, i).text)

        # 혹시 모르니.
        if next_chunk_id < chunk_id and next_chunk_id > 0:
            sc.set_chunk_frame(next_chunk_id, SpectatorApi.get_chunk_frame(platform, game_id, next_chunk_id).text)

        # get all key frame data
        if key_frame_id > last_key_frame:
            for i in range(last_key_frame+ 1, key_frame_id + 1):
                sc.set_key_frame(i, SpectatorApi.get_key_frame(platform, game_id, i).text)

        last_chunk = chunk_id
        last_key_frame = key_frame_id

        customChunkInfo = {
            'nextChunkId': first_chunk,
            'chunkId': first_chunk,
            'nextAvailableChunk': 3000,
            'startGameChunkId': chunk["startGameChunkId"],
            'keyFrameId': first_key_frame,
            'endGameChunkId': chunk["chunkId"],
            'availableSince': 0,
            'duration': 3000,
            'endStartupChunkId': chunk["endStartupChunkId"]
        }

        first_chunk_data = customChunkInfo

        customChunkInfo['nextChunkId'] = chunk['chunkId'] - 1
        customChunkInfo['chunkId'] = chunk['chunkId']
        customChunkInfo['keyFrameId'] = chunk['keyFrameId']

        last_chunk_data = customChunkInfo

        # the game is over
        if int(chunk['endGameChunkId']) == chunk_id:
            print('the game is over {}'.format(game_id))
            break

        sc.set_first_chunk(first_chunk_data)
        sc.set_last_chunk(last_chunk_data)

        next_time = int(chunk["nextAvailableChunk"]) / 1000 + 1
        time.sleep(next_time)

