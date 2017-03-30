from celery import Celery
import time

'''
app = Celery(backend='redis://iris.bi:6379/0', broker='redis://iris.bi:6379/0')
#app = Celery(backend='amqp://admin:00@iris.bi:5672/brand', broker='amqp://admin:00@iris.bi:5672/brand')
#app = Celery(broker='amqp://admin:00@iris.bi:5672/brand')
#app.conf.CELERY_RESULT_BACKEND = 'amqp://admin:00@iris.bi:5672/brand'

@app.task(name="task_redis.add")
def add(x, y):
	time.sleep(2)
	return x + y

'''