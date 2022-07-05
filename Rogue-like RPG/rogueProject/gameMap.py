from __future__ import annotations
import numpy as np
from tcod.console import Console
from typing import Iterable, TYPE_CHECKING, Optional, Iterator

import tileTypes
from entity import Actor

if TYPE_CHECKING:
    from entity import Entity
    from engine import Engine

# State Pattern

class GameMap:
    def __init__(self, engine: Engine, width: int, height: int, entities: Iterable[Entity] = ()):
        self.engine = engine
        self.width, self.height = width, height
        self.tiles = np.full((width, height), fill_value = tileTypes.wall, order = "F")
        self.visible = np.full((width, height), fill_value = False, order = "F")
        self.explored = np.full((width, height), fill_value = False, order = "F")
        self.entities = set(entities)

    def inBounds(self, x: int, y: int) -> bool:
        return 0 <= x < self.width and 0 <= y < self.height

    def getBlockEnt(self, locX: int, locY: int) -> Optional[Entity]:
        for entity in self.entities:
            if (entity.block and entity.x == locX and entity.y == locY):
                return entity
            
        return None

    @property
    def actors(self) -> Iterator[Actor]:
        yield from (entity for entity in self.entities if isinstance(entity, Actor) and entity.alive)

    def getActorLoc(self, x: int, y: int) -> Optional[Actor]:
        for actor in self.actors:
            if ((actor.x == x) and (actor.y == y)):
                return actor

        return None 

    def render(self, console: Console) -> None:
        console.tiles_rgb[0: self.width, 0: self.height] = np.select(condlist = [self.visible, self.explored], choicelist = [self.tiles["light"], self.tiles["dark"]], default = tileTypes.shadow)
        
        sortedEnts = sorted(self.entities, key = lambda x: x.render.value)
        for entity in sortedEnts:
            if(self.visible[entity.x, entity.y]):
                console.print(entity.x, entity.y, entity.char, fg = entity.color)