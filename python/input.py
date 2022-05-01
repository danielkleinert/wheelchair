from data_types import WheelRotation, Steering


def map_to_steering(wheel_rotation: WheelRotation) -> Steering:
    forward = 0
    rotation_input = wheel_rotation
    if wheel_rotation.left >= 0 and wheel_rotation.right >= 0:
        forward = min(wheel_rotation.left, wheel_rotation.right)
        rotation_input = WheelRotation(wheel_rotation.left - forward, wheel_rotation.right - forward)
    if wheel_rotation.left < 0 and wheel_rotation.right < 0:
        forward = max(wheel_rotation.left, wheel_rotation.right)
        rotation_input = WheelRotation(wheel_rotation.left + forward, wheel_rotation.right + forward)
    right = rotation_input.left - rotation_input.right
    return Steering(forward, right)
