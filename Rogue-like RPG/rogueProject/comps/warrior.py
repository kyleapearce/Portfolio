from __future__ import annotations
from typing import TYPE_CHECKING

from render import Render
from inputHandlers import GameOverHandler
from comps.base import Base

if TYPE_CHECKING:
    from entity import Actor

class Warrior(Base):
    entity: Actor
    def __init__(self, hp: int, armor: int, strength: int):
        self.maxHP = hp
        self._hp = hp
        self.armor = armor
        self.strength = strength

    @property
    def hp(self) -> int:
        return self._hp

    def die(self) -> None:
        if self.engine.player is self.entity:
            dieMsg = "Game Over! You died!"
            self.engine.eventHandler = GameOverHandler(self.engine)
        else:
            dieMsg = f"{self.entity.name} has died!"

        self.entity.char = "X"
        self.entity.color = (255, 0, 0)
        self.entity.block = False
        self.entity.ai = None
        self.entity.name = f"The corpse of {self.entity.name}"
        self.entity.render = Render.CORPSE
        print(dieMsg)

    @hp.setter
    def hp(self, value: int) -> None:
        self._hp = max(0, min(value, self.maxHP))
        if (self._hp == 0 and self.entity.ai):
            self.die()