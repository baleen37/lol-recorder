import redis

from glb import config

redis = redis.StrictRedis(host=config.REDIS_HOST,
                          port=config.REDIS_PORT, db=config.REDIS_DB)

class StoreController:

    def __init__(self, platform, game_id):
        self.platform = platform
        self.game_id = game_id

    @property
    def redis_key(self):
        return 'replay_data_{}_{}'.format(self.platform.name, self.game_id)

    def set_version(self, version):
        return redis.hset(self.redis_key, 'version', version)

    def version(self):
        return redis.hget(self.redis_key, 'version')

    def set_encryption_key(self, encryption_key):
        return redis.hset(self.redis_key, 'encryption_key', encryption_key)

    def encryption_key(self):
        return redis.hget(self.redis_key, 'encryption_key')

    def set_meta_data(self, value):
        return redis.hset(self.redis_key, 'meta_data', value)

    def meta_data(self):
        return redis.hget(self.redis_key, 'meta_data')

    def set_chunk_frame(self, chunk_id, data):
        return redis.hset(self.redis_key, 'chunk_frame_{}'.format(chunk_id), data)

    def chunk_frame(self, chunk_id):
        return redis.hget(self.redis_key, 'chunk_frame_{}'.format(chunk_id))

    def set_key_frame(self, frame_id, data):
        return redis.hset(self.redis_key, 'key_frame_{}'.format(frame_id), data)

    def key_frame(self, frame_id):
        return redis.hget(self.redis_key, 'key_frame_{}'.format(frame_id))

    def set_first_chunk(self, data):
        return redis.hset(self.redis_key, 'first_chunk', data)

    def first_chunk(self):
        return redis.hget(self.redis_key, 'first_chunk')

    def set_last_chunk(self, data):
        return redis.hset(self.redis_key, 'last_chunk', data)

    def last_chunk(self):
        return redis.hget(self.redis_key, 'last_chunk')
