from __future__ import annotations
from typing import TYPE_CHECKING, Optional, Tuple

if TYPE_CHECKING:
    from engine import Engine
    from entity import Entity, Actor

class Action:
    def __init__(self, entity: Actor) -> None:
        super().__init__()
        self.entity = entity

    @property
    def engine(self) -> Engine:
        return self.entity.gameMap.engine

    def perform(self) -> None:
        raise NotImplementedError()

# subclasses of Action
class Escape(Action):
    def perform(self) -> None:
        raise SystemExit()

class Direction(Action):
    def __init__(self, entity: Actor, dx: int, dy: int):
        super().__init__(entity)
        self.dx = dx
        self.dy = dy

    def perform(self) -> None:
        raise NotImplementedError()

    @property
    def destXY(self) -> Tuple[int, int]:
        return self.entity.x + self.dx, self.entity.y + self.dy

    @property
    def blockEnt(self) -> Optional[Entity]:
        return self.engine.gameMap.getBlockEnt(*self.destXY)

    @property
    def targetEnt(self) -> Optional[Actor]:
        return self.engine.gameMap.getActorLoc(*self.destXY)

class Movement(Direction):
    def perform(self) -> None:
        destX, destY = self.destXY

        if not self.engine.gameMap.inBounds(destX, destY): #out of bounds
            return
        if not self.engine.gameMap.tiles["walkable"][destX, destY]: #blocked by title
            return
        if self.engine.gameMap.getBlockEnt(destX, destY): # blocked by enemy
            return

        self.entity.move(self.dx, self.dy)

class Attack(Direction):
    def perform(self) -> None:
        target = self.targetEnt
        if not target:
            return

        dmg = self.entity.warrior.strength - target.warrior.armor
        message = f"{self.entity.name.capitalize()} attacks {target.name}"

        if dmg > 0:
            print(f"{message} for {dmg} damage!")
            target.warrior.hp -= dmg
        else:
            print(f"{message} but it does nothing!")

class Bump(Direction):
    def perform(self) -> None:
        if self.targetEnt:
            return Attack(self.entity, self.dx, self.dy).perform()
        else:
            return Movement(self.entity, self.dx, self.dy).perform()

class Wait(Action):
    def perform(self) -> None:
        pass