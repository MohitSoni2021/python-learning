from redis import Redis
from rq import Queue

# creating queue and having the connection with the redis
queue = Queue(
    connection=Redis(
        host="localhost",
        port="6379"
    )
)