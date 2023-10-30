from irobot_edu_sdk.backend.bluetooth import Bluetooth
from irobot_edu_sdk.robots import event, hand_over, Color, Robot, Root, Create3
from irobot_edu_sdk.music import Note

import math as m

robot = Create3(Bluetooth("MARVIN"))
current_color = "cyan"


@event(robot.when_touched, [True, False])
async def leftTouch(robot):
    global any_button_pressed
    any_button_pressed = True
    for k in range(10):
        await robot.set_wheel_speeds(0, 0)
        await robot.set_lights_rgb(255, 0, 0)


@event(robot.when_touched, [False, True])
async def rightTouch(robot):
    global any_button_pressed
    any_button_pressed = True
    for k in range(10):
        await robot.set_wheel_speeds(0, 0)
        await robot.set_lights_rgb(255, 0, 0)


@event(robot.when_bumped, [True, True])
async def bumpTouch(robot):
    global any_button_pressed
    any_button_pressed = True
    for k in range(10):
        await robot.set_wheel_speeds(0, 0)
        await robot.set_lights_rgb(255, 0, 0)


@event(robot.when_play)
async def robotPong(robot):
    global current_color, any_button_pressed, prox_dist
    await robot.set_lights(Robot.LIGHT_SPIN, Color(0, 255, 255))
    await robot.set_wheel_speeds(15, 15)
    any_button_pressed = False

    while not any_button_pressed:
        angles = [-65.3, -38.0, -20.0, -3.0, 14.25, 34.0, 65.3]
        ir_readings = (await robot.get_ir_proximity()).sensors
        for sensor_value in ir_readings:
            prox_dist = 4095 / (sensor_value + 1)
            if prox_dist <= 20.0:
                approach_angle = get_approach_angle(ir_readings, angles)
                if approach_angle > 0:
                    reflect_angle = 180 - (approach_angle * 2)
                    await robot.turn_right(reflect_angle)
                    await robot.wait(0.2)
                else:
                    reflect_angle = 180 + (approach_angle * 2)
                    await robot.turn_left(reflect_angle)
                    await robot.wait(0.2)

                if current_color == "cyan":
                    await robot.set_wheel_speeds(0, 0)
                    await robot.set_lights(Robot.LIGHT_SPIN, Color(255, 0, 255))
                    await robot.wait(0.2)
                    current_color = "magenta"
                else:
                    await robot.set_wheel_speeds(0, 0)
                    await robot.set_lights(Robot.LIGHT_SPIN, Color(0, 100, 100))
                    await robot.wait(0.2)
                    current_color = "cyan"

        await robot.set_wheel_speeds(15, 15)


def get_approach_angle(sensor_readings, angle_values):
    max_sensor_value = max(sensor_readings)
    for k in range(len(sensor_readings)):
        if sensor_readings[k] == max_sensor_value:
            approach_angle = angle_values[k]
    return approach_angle


robot.play()

