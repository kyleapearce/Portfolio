from __future__ import annotations
from typing import TYPE_CHECKING

from tcod.context import Context
from tcod.console import Console
from tcod.map import compute_fov

from inputHandlers import MainHandler

if TYPE_CHECKING:
    from entity import Actor
    from gameMap import GameMap
    from inputHandlers import EventHandler

class Engine:
    gameMap: GameMap

    def __init__(self, player: Actor):
        self.eventHandler: EventHandler = MainHandler(self)
        self.player = player

    def simEntTurns(self) -> None:
        for entity in set(self.gameMap.actors) - {self.player}:
            if entity.ai:
                entity.ai.perform()

    def update_fov(self) -> None:
        self.gameMap.visible[:] = compute_fov(
            self.gameMap.tiles["transparent"], (self.player.x, self.player.y), radius = 8
        )
        self.gameMap.explored |= self.gameMap.visible

    # State Pattern
    def render(self, console: Console, context: Context) -> None:
        self.gameMap.render(console)
        console.print(x = 1, y = 47, string = f"HP: {self.player.warrior.hp}/{self.player.warrior.maxHP}")
        context.present(console)
        console.clear()