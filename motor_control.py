from time import sleep
from pyfirmata import ArduinoMega #pyfirmata code is on Arduino Mega to run Python through USB serial

EN_IDS = ["d:12:p","d:10:p", "d:8:p"] #PWM outputs for speed
IN_IDS = ["d:40:o","d:41:o","d:44:o","d:45:o", "d:36:o", "d:37:o"] #Digital outputs for direction

CAMERA_WIDTH = 640
CAMERA_HEIGHT = 480
TARGET_X = CAMERA_WIDTH / 2
TARGET_Y = CAMERA_HEIGHT / 2
THRESHOLD = 50
DUTY = 0.33

#Initialize Arduino Mega on COM8
def init_hardware():
    board = ArduinoMega("COM8")
    ens = [board.get_pin(en_id) for en_id in EN_IDS]
    ins = [board.get_pin(in_id) for in_id in IN_IDS]
    motors = [init_motor_config(ens, ins, x) for x in range(0, 3)]
    return (board, motors)

def init_motor_config(ens, ins, x):
    return {
        "en": ens[x],
        "in1": ins[x * 2],
        "in2": ins[x * 2 + 1]
    }

def actuate_motor(motor, value):
    motor.get("in1").write(0 if value > 0 else 1)
    motor.get("in2").write(1 if value > 0 else 0)
    motor.get("en").write(abs(value))

#Motor Control Thread
def motor_control(memory={}):
    board, motors = init_hardware()

    while memory.get("running"):
        centroid = memory.get("centroid") #Centroid from image processing thread
        if centroid is not None:
            #Control in the x direction for centering robot arm on target centroid
            dx = centroid.get("cX") - TARGET_X
            if abs(dx) > THRESHOLD // 2:
                actuate_motor(motors[0], DUTY if dx < 0 else -DUTY)
                board.pass_time(0.1)
                actuate_motor(motors[0], 0)
            else:
                actuate_motor(motors[0], 0)
                if not memory["cut_flag"]:
                    for i in range(2):
                        actuate_motor(motors[2], DUTY)
                        sleep(1.7)
                        actuate_motor(motors[2], -DUTY)
                        sleep(1.4)
                    actuate_motor(motors[2], 0)
                    memory["cut_flag"] = True

                actuate_motor(motors[0], 0)
##          #Control in the y direction - Wires are oriented vertically, NOT USED
##            dy = centroid.get("cY") - TARGET_Y
##            if abs(dy) > THRESHOLD // 2:
##                actuate_motor(motors[1], -DUTY if dy < 0 else DUTY)
##                board.pass_time(0.1)
##                actuate_motor(motors[1], 0)
##            else:
##                actuate_motor(motors[1], 0)
            
        sleep(0.4)

    [actuate_motor(motor, 0) for motor in motors]
    board.exit()
