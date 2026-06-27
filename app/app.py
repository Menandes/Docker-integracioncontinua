from flask import Flask
import redis
import os

app = Flask(__name__)
cache = redis.Redis(host=os.getenv('REDIS_HOST', 'redis'), port=6379)

@app.route('/')
def home():
    count = cache.incr('hits')
    return f'¡Hola! Esta página se ha visitado {count} veces.\n'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
