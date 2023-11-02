from irobot_edu_sdk.backend.bluetooth import Bluetooth
from irobot_edu_sdk.robots import event, hand_over, Color, Robot, Root, Create3
from irobot_edu_sdk.music import Note

import math as m

robot = Create3(Bluetooth("MARVIN"))
color="cyan"


@event(robot.when_touched, [True, False])  
async def when_left_button_touched(robot):
    global ANY_BUMBUT_PRESSED
    ANY_BUMBUT_PRESSED = True
    for i in range(10):
        await robot.set_wheel_speeds(0,0)
        await robot.set_lights_rgb(255, 0, 0)
        



@event(robot.when_touched, [False, True])  
async def when_right_button_touched(robot):
    global ANY_BUMBUT_PRESSED
    ANY_BUMBUT_PRESSED = True
    for i in range(10):
        await robot.set_wheel_speeds(0,0)
        await robot.set_lights_rgb(255, 0, 0)
    



@event(robot.when_bumped, [True, True])  
async def when_either_bumped(robot):
    global ANY_BUMBUT_PRESSED
    ANY_BUMBUT_PRESSED = True
    for i in range(10):
        await robot.set_wheel_speeds(0,0)
        await robot.set_lights_rgb(255, 0, 0)
        


@event(robot.when_play)
async def robotPong(robot):
    global color, ANY_BUMBUT_PRESSED, proximity
    await robot.set_lights(Robot.LIGHT_SPIN, Color(0,255,255))
    await robot.set_wheel_speeds(15,15)
    ANY_BUMBUT_PRESSED = False
    while ANY_BUMBUT_PRESSED == False:
        angles = [-65.3, -38.0,-20.0,-3.0,14.25,34.0,65.3]
        readings = (await robot.get_ir_proximity()).sensors
        for j in range(len(readings)):
            proximity = 4095/(readings[j]+1)
            if proximity <= 20.0:
                appAng = getApproachAngle(readings, angles)
                if appAng>0:
                    reflect = 180 - (appAng*2)
                    await robot.turn_right(reflect)
                    await robot.wait(0.2)
                else:
                    reflect = 180+ (appAng*2)
                    await robot.turn_left(reflect)
                    await robot.wait(0.2)
                if color == "cyan":
                    await robot.set_wheel_speeds(0,0)
                    await robot.set_lights(Robot.LIGHT_SPIN, Color(255,0,255))
                    await robot.wait(0.2)
                    color = "magenta"
                else:
                    await robot.set_wheel_speeds(0,0)
                    await robot.set_lights(Robot.LIGHT_SPIN,Color(0,100,100))
                    await robot.wait(0.2)
                    color = "cyan"
            await robot.set_wheel_speeds(15,15)
def getApproachAngle(readings, angles):
    maxReading = max(readings)
    for j in range(len(readings)):
        if readings[j] == maxReading:
            appAng = angles[j]
    return appAng

(robot.play())
