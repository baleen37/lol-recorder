import json
import requests
from glb import config


class LoLApi:

    def __init__(self, api_key=None):
        self.api_key = api_key or config.LOL_API_KEY

    def current_game_info(self, summoner_id, platform):
        params = { 'api_key' : self.api_key }
        res = requests.get('https://{}.api.pvp.net/observer-mode/rest/consumer/getSpectatorGameInfo/{}/{}'.format(
            platform.region, platform.name, summoner_id), params = params)

        return res


class SpectatorApi:

    _PREFIX_URL = 'http://{}/observer-mode/rest/consumer'

    @classmethod
    def get_version(cls, platform):
        res = requests.get((SpectatorApi._PREFIX_URL + '/version').format())
        return res

    @classmethod
    def get_meta_data(cls, platform, game_id):
        res = requests.get((SpectatorApi._PREFIX_URL + '/getGameMetaData/{}/{}/0/token').format(
            platform.spectator, platform.name, game_id))
        return res

    @classmethod
    def get_last_chunk_info(cls, platform, game_id):
        res = requests.get((SpectatorApi._PREFIX_URL + '/getLastChunkInfo/{}/{}/0/token').format(
            platform.spectator, platform.name, game_id))
        print("request {} get_last_chunk_info platform : {}, game_id: {}".format(res.ok, platform, game_id))
        return res

    @classmethod
    def get_chunk_frame(cls, platform, game_id, chunk_id):
        res = requests.get((SpectatorApi._PREFIX_URL + '/getGameDataChunk/{}/{}/{}/token').format(
            platform.spectator, platform.name, game_id, chunk_id))
        print("request {} get_chunk_frame platform : {}, game_id: {}, chunk_id: {}".format(res.ok, platform, game_id, chunk_id))
        return res

    @classmethod
    def get_key_frame(cls, platform, game_id, frame_id):
        res = requests.get((SpectatorApi._PREFIX_URL + '/getKeyFrame/{}/{}/{}/token').format(
            platform.spectator, platform.name, game_id, frame_id))
        print("request {} get_key_frame platform : {}, game_id: {}, frame_id: {}".format(res.ok, platform, game_id, frame_id))
        return res
