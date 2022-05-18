from data_types import WheelRotation, Steering


def map_to_steering(wheel_rotation: WheelRotation) -> Steering:
    forward = 0
    right = wheel_rotation.left - wheel_rotation.right
    if wheel_rotation.left >= 0 and wheel_rotation.right >= 0:
        forward = min(wheel_rotation.left, wheel_rotation.right)
    elif wheel_rotation.left < 0 and wheel_rotation.right < 0:
        forward = max(wheel_rotation.left, wheel_rotation.right)
        right = -right
    return Steering(forward, right)
