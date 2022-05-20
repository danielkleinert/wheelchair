from dataclasses import dataclass
from enum import Enum


@dataclass
class WheelRotation:
    left: int
    right: int


@dataclass
class Steering:
    forward: int
    right: int


class Game(Enum):
    MARIO_KART_WII = 1
    MARIO_KART_64 = 2
    DEBUG_TURTLE = 3
