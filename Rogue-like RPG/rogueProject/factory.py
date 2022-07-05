from entity import Actor
from comps.warrior import Warrior
from comps.ai import Hostile

# Factory Pattern

player = Actor(char = "@", color = (255, 0, 255), name = "Player", ai = Hostile, warrior = Warrior(hp = 30, armor = 2, strength = 5))
minion = Actor(char="e", color = (34, 139, 34), name = "Minion", ai = Hostile, warrior = Warrior(hp = 5, armor = 1, strength = 3))
boss = Actor(char="G", color = (255, 215, 0), name = "Boss", ai = Hostile, warrior = Warrior(hp = 15, armor = 2, strength = 5))