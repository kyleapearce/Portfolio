from __future__ import annotations
import tcod.event

from typing import Optional, TYPE_CHECKING
from actions import Action, Escape, Bump, Wait

if TYPE_CHECKING:
    from engine import Engine

# Command Pattern

class EventHandler(tcod.event.EventDispatch[Action]):
    def __init__(self, engine: Engine):
        self.engine = engine

    def handleEvents(self) -> None:
        raise NotImplementedError()

    def ev_quit(self, event: tcod.event.Quit) -> Optional[Action]:
        raise SystemExit()

class MainHandler(EventHandler):
    def handleEvents(self) -> None:
        for event in tcod.event.wait():
            action = self.dispatch(event)

            if action is None:
                continue

            action.perform()

            self.engine.simEntTurns()
            self.engine.update_fov()

    def ev_keydown(self, event: tcod.event.KeyDown) -> Optional[Action]:
        action: Optional[Action] = None
        key = event.sym
        player = self.engine.player

        if key == tcod.event.K_UP:
            action = Bump(player, dx = 0, dy = -1)
        elif key == tcod.event.K_DOWN:
            action = Bump(player, dx = 0, dy = 1)
        elif key == tcod.event.K_LEFT:
            action = Bump(player, dx = -1, dy = 0)
        elif key == tcod.event.K_RIGHT:
            action = Bump(player, dx = 1, dy = 0)
        elif key == tcod.event.K_PERIOD:
            action = Wait(player)
        elif key == tcod.event.K_ESCAPE:
            action = Escape(player)

        return action

class GameOverHandler(EventHandler):
    def handleEvents(self) -> None:
        for event in tcod.event.wait():
            action = self.dispatch(event)

            if action is None:
                continue

            action.perform()

    def ev_keydown(self, event: tcod.event.KeyDown) -> Optional[Action]:
        action: Optional[Action] = None
        key = event.sym

        if key == tcod.event.K_ESCAPE:
            action = Escape(self.engine.player)

        return