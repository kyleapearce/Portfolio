from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from engine import Engine
    from entity import Entity

class Base:
    entity: Entity

    @property
    def engine(self) -> Engine:
        return self.entity.gameMap.engine