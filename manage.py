from rq import Connection, Worker
import redis
from flask_script import Server, Manager
from flask.cli import FlaskGroup
from app import create_app


app = create_app()
cli = FlaskGroup(create_app=create_app)

@cli.command()
def run_worker():
    redis_url = app.config['REDIS_URL']
    # redis_url = 'localhost:6379'
    print(redis_url)
    redis_connection = redis.from_url(redis_url)
    with Connection(redis_connection):
        worker = Worker(app.config['QUEUES'])
        worker.work()

    # with Connection(redis_connection):
    #     worker = Worker('default')
    #     worker.work()

if __name__ == '__main__':
    cli()
