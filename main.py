from pathlib import Path
from arcade.resources import add_resource_handle


from app import run

#   |------| COMBAT |------|
# a rhythm game about fighting battleships!
#
#
#
#

if __name__ == '__main__':
    add_resource_handle("resource", f"{Path(__file__).parent.resolve()}/resources")

    run()
