import redis

from glb import config

redis = redis.StrictRedis(host=config.REDIS_HOST,
                          port=config.REDIS_PORT, db=config.REDIS_DB)
