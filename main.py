from pathlib import Path
from arcade.resources import add_resource_handle


from app import run

# RUN THIS SCRIPT TO PLAY GAME

if __name__ == '__main__':
    add_resource_handle("resource", f"{Path(__file__).parent.resolve()}/resources")

    run()
