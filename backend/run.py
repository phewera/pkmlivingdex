from api import app
from utility import read_config
from uvicorn import run

if __name__ == "__main__":
    config = read_config('backend')
    run(
        app=app,
        port=int(config['port']),
        host=config['host']
    )
