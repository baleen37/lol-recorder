from celery import Celery

from worker import celeryconfig

app = Celery('worker', include=['worker.tasks'])
app.config_from_object(celeryconfig)

if __name__ == '__main__':
    app.start()
