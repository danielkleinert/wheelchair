from dataclasses import dataclass


@dataclass
class WheelRotation:
    left: int
    right: int


@dataclass
class Steering:
    forward: int
    right: int
