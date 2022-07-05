from __future__ import annotations
from typing import Tuple, List, TYPE_CHECKING
import tcod
import numpy as np

from actions import Action, Wait, Movement, Attack
from comps.base import Base

if TYPE_CHECKING:
    from entity import Actor

class baseAI(Action, Base):
    entity: Actor
    def perform(self) -> None:
        raise NotImplementedError()

    def pathTo(self, destX: int, destY: int) -> List[Tuple[int, int]]:
        steps = np.array(self.entity.gameMap.tiles["walkable"], dtype = np.int8)
        for entity in self.entity.gameMap.entities:
            if(entity.block and steps[entity.x, entity.y]):
                steps[entity.x, entity.y] += 10
        
        graph = tcod.path.SimpleGraph(cost = steps, cardinal = 2, diagonal = 3)

        compass = tcod.path.Pathfinder(graph)
        compass.add_root((self.entity.x, self.entity.y))
        path: List[List[int]] = compass.path_to((destX, destY))[1:].tolist()

        return [(pt[0], pt[1]) for pt in path]

class Hostile(baseAI):
    def __init__(self, entity: Actor):
        super().__init__(entity)
        self.path: List[Tuple[int, int]] = []

    def perform(self) -> None:
        target = self.engine.player
        dx = target.x - self.entity.x
        dy = target.y - self.entity.y
        dist = max(abs(dx), abs(dy))
        
        if self.engine.gameMap.visible[self.entity.x, self.entity.y]:
            if dist <= 1:
                return Attack(self.entity, dx, dy).perform()

            self.path = self.pathTo(target.x, target.y)

        if self.path:
            destX, destY = self.path.pop(0)
            return Movement(self.entity, destX - self.entity.x, destY - self.entity.y).perform()

        return Wait(self.entity).perform()