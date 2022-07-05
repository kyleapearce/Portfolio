from __future__ import annotations
from typing import Tuple, TypeVar, TYPE_CHECKING, Optional, Type
import copy

from render import Render

if TYPE_CHECKING:
    from gameMap import GameMap
    from comps.warrior import Warrior
    from comps.ai import baseAI

T = TypeVar("T", bound = "Entity")

class Entity:
    gameMap: GameMap
    def __init__(self, gameMap: Optional[GameMap] = None, x: int = 0, y: int = 0, char: str = "?", color: Tuple[int, int, int] = (255, 255, 255), name: str = "<Unnamed>", block: bool = False, render: Render = Render.CORPSE):
        self.x = x
        self.y = y
        self.char = char
        self.color = color
        self.name = name
        self.block = block
        self.render = render
        if gameMap:
            self.gameMap = gameMap
            gameMap.entities.add(self)

    def spawn(self: T, gameMap: GameMap, x: int, y: int) -> T:
        clone = copy.deepcopy(self)
        clone.x = x
        clone.y = y
        clone.gameMap = gameMap
        gameMap.entities.add(clone)
        return clone

    def move(self, dx: int, dy: int) -> None:
        self.x += dx
        self.y += dy

    def place(self, x: int, y: int, gameMap: Optional[GameMap] = None) -> None:
        self.x = x
        self.y = y
        if gameMap:
            if hasattr(self, "gameMap"):
                self.gameMap.entities.remove(self)
            self.gameMap = gameMap
            gameMap.entities.add(self)

class Actor(Entity):
    def __init__(self, *, x: int = 0, y: int = 0, char: str = "?", color: Tuple[int, int, int] = (255, 255, 255), name: str = "<Unnamed>", ai: Type[baseAI], warrior: Warrior):
        super().__init__(x = x, y = y, char = char, color = color, name = name, block = True, render = Render.ACTOR)
        self.ai: Optional[baseAI] = ai(self)
        self.warrior = warrior
        self.warrior.entity = self

    @property
    def alive(self) -> bool:
        return bool(self.ai)