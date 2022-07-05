from __future__ import annotations
from typing import Tuple, Iterator, List, TYPE_CHECKING
import random
import tcod

from gameMap import GameMap
import tileTypes
import factory

if TYPE_CHECKING:
    from engine import Engine

class RectRoom:
    def __init__(self, x: int, y: int, width: int, height: int):
        self.x1 = x
        self.x2 = x + width
        self.y1 = y
        self.y2 = y + height

    @property
    def center(self) -> Tuple[int, int]:
        centerX = int((self.x1 + self.x2) / 2)
        centerY = int((self.y1 + self.y2) / 2)

        return centerX, centerY

    @property
    def inner(self) -> Tuple[slice, slice]:
        return slice(self.x1 + 1, self.x2), slice(self.y1 + 1, self.y2)

    def inters(self, other: RectRoom) -> bool:
        return (
            self.x1 <= other.x2 and self.x2 >= other.x1 and self.y1 <= other.y2 and self.y2 >= other.y1
        )

def hall(
    start: Tuple[int, int], end: Tuple[int, int]
) -> Iterator[Tuple[int, int]]:
    x1, y1 = start
    x2, y2 = end

    if(random.random() < 0.5):
        cornerX, cornerY = x2, y1
    else:
        cornerX, cornerY = x1, y2

    for x, y in tcod.los.bresenham((x1, y1), (cornerX, cornerY)).tolist():
        yield x, y

    for x, y in tcod.los.bresenham((cornerX, cornerY), (x2, y2)).tolist():
        yield x, y

def placeEnts(room: RectRoom, dun: GameMap, maxEnts: int) -> None:
    numEnts = random.randint(0, maxEnts)

    for i in range(numEnts):
        x = random.randint(room.x1 + 1, room.x2 - 1)
        y = random.randint(room.y1 + 1, room.y2 - 1)

        if not any((entity.x == x) and (entity.y == y) for entity in dun.entities):
            if(random.random() < 0.8):
                factory.minion.spawn(dun, x, y)
            else:
                factory.boss.spawn(dun, x, y)

def genDungeon(maxRooms: int, minRoomSize: int, maxRoomSize: int, mapW: int, mapH: int, entRoomMax: int, engine: Engine) -> GameMap:
    player = engine.player
    dun = GameMap(engine, mapW, mapH, entities = [player])

    rooms: List[RectRoom] = []

    for r in range(maxRooms):
        roomH = random.randint(minRoomSize, maxRoomSize)
        roomW = random.randint(minRoomSize, maxRoomSize)
        
        x = random.randint(0, dun.width - roomW - 1)
        y = random.randint(0, dun.height - roomH - 1)

        newRoom = RectRoom(x, y, roomW, roomH)

        if any(newRoom.inters(otherRoom) for otherRoom in rooms):
            continue

        dun.tiles[newRoom.inner] = tileTypes.floor

        if(len(rooms) == 0):
            player.place(*newRoom.center, dun)
        else:
            for x, y in hall(rooms[-1].center, newRoom.center):
                dun.tiles[x, y] = tileTypes.floor

        placeEnts(newRoom, dun, entRoomMax)
        rooms.append(newRoom)
    
    return dun