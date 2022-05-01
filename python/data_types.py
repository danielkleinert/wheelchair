from dataclasses import dataclass


@dataclass
class WheelRotation:
    left: float
    right: float


@dataclass
class Steering:
    forward: float
    right: float
