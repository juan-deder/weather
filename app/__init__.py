import os
from flask import Flask
from flask_caching import Cache

cache = Cache(config={
    'CACHE_DEFAULT_TIMEOUT': int(os.environ.get('CACHE_DEFAULT_TIMEOUT')),
    'CACHE_DIR': os.environ.get('CACHE_DIR'),
    'CACHE_TYPE': os.environ.get('CACHE_TYPE'),
})
config = {
    'api_url': 'http://api.openweathermap.org/data/2.5/weather',
    'api_id': '1508a9a4840a5574c822d70ca2132032'
}


def create_app():
    app = Flask(__name__)

    cache.init_app(app)

    from app.main import main
    app.register_blueprint(main)

    return app
