from irobot_edu_sdk.backend.bluetooth import Bluetooth
from irobot_edu_sdk.robots import event, hand_over, Color, Robot, Root, Create3
from irobot_edu_sdk.music import Note

robot = Create3(Bluetooth("ROBOT_NAME"))

correctPassword = "1234"
userPassword = ""


@event(robot.when_touched, [True, False])
async def leftTouched(robot):
    global buttonTouched, userPassword
    buttonTouched = True
    userPassword += "1"
    await robot.play_note(Note.C5, 0.25)
    await checkUserCode(robot)


@event(robot.when_touched, [False, True])
async def rightTouched(robot):
    global buttonTouched, userPassword
    buttonTouched = True
    userPassword += "2"
    await robot.play_note(Note.D5, 0.25)
    await checkUserCode(robot)


@event(robot.when_bumped, [True, False])
async def leftBumped(robot):
    global buttonTouched, userPassword
    buttonTouched = True
    userPassword += "3"
    await robot.play_note(Note.E5, 0.25)
    checkUserCode(robot)


@event(robot.when_bumped, [False, True])
async def rightBumped(robot):
    global buttonTouched, userPassword
    buttonTouched = True
    userPassword += "4"
    await robot.play_note(Note.F5, 0.25)
    await checkUserCode(robot)


async def checkUserCode(robot):
    global userPassword
    if len(userPassword) == len(correctPassword):
        if userPassword == correctPassword:
            for i in range(4):
                await robot.turn_right(45)
            for i in range(2):
                await robot.set_lights(Robot.LIGHT_SPIN, Color(0, 128, 0))
                await robot.play_note(Note.F4, 0.2)
                await robot.play_note(Note.A4, 0.2)
                await robot.play_note(Note.C5, 0.2)
        else:
            for i in range(1):
                userPassword = ""
                await robot.turn_right(45)
                await robot.turn_left(45)
                await robot.set_lights(Robot.LIGHT_ON, Color(255, 0, 0))
                await robot.play_note(Note.C4, 0.2)
                await robot.play_note(Note.A4, 0.2)
                await robot.play_note(Note.F4, 0.2)


@event(robot.when_play)
async def play(robot):
    await checkUserCode(robot)


robot.play()















