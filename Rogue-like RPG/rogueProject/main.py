import tcod
import copy

from engine import Engine
from mapGen import genDungeon
import factory

def main() -> None:

    screenHeight = 50
    screenWidth = 80

    mapHeight = 45
    mapWidth = 80

    maxRooms = 30
    maxRoomSize = 10
    minRoomSize = 6

    entRoomMax = 2

    tileset = tcod.tileset.load_tilesheet (
        "defaultImage.png", 32, 8, tcod.tileset.CHARMAP_TCOD
    )

    player = copy.deepcopy(factory.player)
    engine = Engine(player = player)
    engine.gameMap = genDungeon(maxRooms = maxRooms, minRoomSize = minRoomSize, maxRoomSize = maxRoomSize, mapW = mapWidth, mapH = mapHeight, entRoomMax = entRoomMax, engine = engine)
    engine.update_fov()

    with tcod.context.new_terminal (

        screenWidth,
        screenHeight,
        tileset = tileset,
        title = "Roguelike RPG",
        vsync = True,

    ) as context:

        root_console = tcod.Console(screenWidth, screenHeight, order="F")
        while True:
            engine.render(console = root_console, context = context)
            engine.eventHandler.handleEvents()

if __name__ == "__main__":
    main()