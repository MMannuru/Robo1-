from irobot_edu_sdk.backend.bluetooth import Bluetooth
from irobot_edu_sdk.robots import event, Color, Robot, Create3
from irobot_edu_sdk.music import Note

robot = Create3(Bluetooth("ROBOT_NAME"))
bumperPressed = False

@event(robot.when_touched, [True, False])
async def leftPressed(robot):
    global bumperPressed
    bumperPressed = True
    for k in range(10):
        await robot.set_lights_rgb(255, 0, 0)
        await robot.set_wheel_speeds(0, 0)

@event(robot.when_touched, [False, True])
async def rightPressed(robot):
    global bumperPressed
    bumperPressed = True
    for k in range(10):
        await robot.set_lights_rgb(255, 0, 0)
        await robot.set_wheel_speeds(0, 0)

@event(robot.when_bumped, [True, True])
async def handlePressed(robot):
    global bumperPressed
    bumperPressed = True
    for k in range(10):
        await robot.set_lights_rgb(255, 0, 0)
        await robot.set_wheel_speeds(0, 0)

@event(robot.when_play)
async def avoid_collision(robot):
    global bumperPressed
    while not bumperPressed:
        readings = (await robot.get_ir_proximity()).sensors[3]
        proximity = 4095 / (readings + 1)
        if proximity > 100:
            await robot.set_wheel_speeds(7, 7)
            await robot.set_lights(Robot.LIGHT_BLINK, Color(0, 255, 0))
        elif 30 < proximity <= 100:
            await robot.set_wheel_speeds(4, 4)
            await robot.play_note(Note.D5, 0.1)
            await robot.set_lights(Robot.LIGHT_BLINK, Color(255, 255, 0))
        elif 5 < proximity <= 30:
            await robot.set_wheel_speeds(1, 1)
            await robot.play_note(Note.D6, 0.1)
            await robot.set_lights(Robot.LIGHT_BLINK, Color(255, 128, 0))
        else:
            await robot.set_wheel_speeds(0, 0)
            await robot.set_lights_rgb(255, 0, 0)
            await robot.play_note(Note.D7, 1)

robot.play()




