from turtle import Turtle
from data_types import Steering

SAMPLING_RATE = 30


class TurtleOutput:

    def __init__(self) -> None:
        self.turtle = Turtle()

    def send_control(self, steering: Steering):
        self.turtle.forward(steering.forward * 1 / SAMPLING_RATE * 0.5)
        self.turtle.right(steering.right * 1 / SAMPLING_RATE * 0.5)






