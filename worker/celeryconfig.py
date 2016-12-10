import datetime
from glb import config


CELERY_ACCEPT_CONTENT = ['pickle', 'json', 'msgpack', 'yaml']
# CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'Asia/Seoul'
CELERY_ENABLE_UTC = False

CELERYBEAT_SCHEDULE = {
    "clear_server_info": {
        "task": "worker.tasks.track_summoners",
        'schedule': datetime.timedelta(seconds=10)
    },
}
