#
import time
from glb.helpers.apis import LoLApi, SpectatorApi
from glb.model import Platforms

def watch_game(summoner_id, platform):
    res = LoLApi().currnet_game_info(summoner_id, platform)

    if res['gameMode'] != 'MATCHED_GAME':
        return False

    if res['mapId'] != 11:
        return False

    if res['gameMode'] != 'CLASSIC':
        return False
    game_length = res['gameLength']
    participants = res['participants'] 

    game_id = res['gameId']
    encryption_key = res['observer']['encryptionKey']
    platform_id = res['platformId']

    return res

def record(platform, game_id):
    first_chunk = None
    first_key_frame = None
    last_chunk = None
    last_key_frame = None

    while(True):
        chunk = SpectatorApi.get_last_chunk_info(platform, game_id)

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
            SpectatorApi.get_chunk_frame(platform, game_id, chunk_id)
            SpectatorApi.get_key_frame(platform, game_id, key_frame_id)

        if start_game_chunk_id > first_chunk:
            first_chunk = start_game_chunk_id

        # get all chunk
        if chunk_id > last_chunk:
            for i in range(last_chunk + 1, chunk_id + 1):
                SpectatorApi.get_chunk_frame(platform, game_id, i)

        # 혹시 모르니.
        if next_chunk_id < chunk_id and next_chunk_id > 0:
            SpectatorApi.get_chunk_frame(platform, game_id, next_chunk_id)

        # get all key frame data
        if key_frame_id > last_key_frame:
            for i in range(last_key_frame+ 1, key_frame_id + 1):
                SpectatorApi.get_key_frame(platform, game_id, i)

        last_chunk = chunk_id
        last_key_frame = key_frame_id

        # the game is over
        if int(chunk['endGameChunkId']) == chunk_id:
            print('the game is over {}'.format(game_id))
            break

        time.sleep(int(chunk["nextAvailableChunk"]) / 1000 + 1)
