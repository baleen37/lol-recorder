import json


class JSONSerializable(object):
    def __repr__(self):
        return json.dumps(self.__dict__)

class _Platform(json.JSONEncoder):

    def __init__(self, name, region, spectator=None):
        self.name = name
        self.region = region
        self.spectator = spectator

    def __str__(self):
        return "<_Platform name: {}>".format(self.name)

    def default(self, o):
        return o.__dict__


class Platforms:
    NA1 = _Platform('NA1', 'na', 'spectator.na.lol.riotgames.com')
    OC1 = _Platform('OC1', 'oce', 'spectator.oc1.lol.riotgames.com')
    EUN1 = _Platform('EUN1', 'eune', 'spectator.eu.lol.riotgames.com:8088')
    EUW1 = _Platform('EUW1', 'euw', 'spectator.euw1.lol.riotgames.com')
    KR = _Platform('KR', 'kr', 'spectator.kr.lol.riotgames.com')
    BR1 = _Platform('BR1', 'br', 'spectator.br.lol.riotgames.com')
    LA1 = _Platform('LA1', 'lan', 'spectator.la1.lol.riotgames.com')
    LA2 = _Platform('LA2', 'las', 'spectator.la2.lol.riotgames.com')
    RU = _Platform('RU', 'ru', 'spectator.ru.lol.riotgames.com')
    TR1 = _Platform('TR1', 'tr', 'spectator.tr.lol.riotgames.com')
    PBE1 = _Platform('PRE1', 'pbe', 'spectator.pbe1.lol.riotgames.com:8088')

    _LIST = [
        NA1,
        OC1,
        EUN1,
        EUW1,
        KR,
        BR1,
        LA1,
        LA2,
        RU,
        TR1,
        PBE1,
    ]


class ReplayData:

    @classmethod
    def data_info_key(cls, platform, game_id):
        return 'replay_data_{}_{}'.format(platform.name, game_id)

    @classmethod
    def chunk_frame_key(cls, chunk_id):
        return 'chunk_frame_{}'.format(chunk_id)

    @classmethod
    def frame_key(cls, key_frame_id):
        return 'frame_{}'.format(key_frame_id)
