import board
import time
from digitalio import DigitalInOut, Direction, Pull
import analogio
from adafruit_motor import stepper
from adafruit_motorkit import MotorKit

#Led
ledBlanco = DigitalInOut(board.GP13)
ledBlanco.direction = Direction.OUTPUT


def parpadeo(times):
    for _ in range(times):
        ledBlanco.value = False
        time.sleep(0.1)
        ledBlanco.value = True
        time.sleep(0.1)


#Fotointerruptor
interruptor = DigitalInOut(board.GP14)
interruptor.direction = Direction.INPUT
interruptor.pull = Pull.UP

#Joystick
eje_y = analogio.AnalogIn(board.A1)


def obtener_voltaje(pin):
    return (pin.value * 3.3) / 65535  # ADC 12-bits [0 - 3.3]


# Stepper motor setup
DELAY = 0.01  # el más rápido es 0.004, 0.01 sigue siendo muy suave, se vuelve paso a paso después de eso
STEPS = 64  # con 513 pasos da una vuelta completa

coils = (
    DigitalInOut(board.GP21),  # A1
    DigitalInOut(board.GP20),  # A2
    DigitalInOut(board.GP19),  # B1
    DigitalInOut(board.GP18),  # B2
)

for coil in coils:
    coil.direction = Direction.OUTPUT

stepper_motor = stepper.StepperMotor(
  coils[0],
  coils[1],
  coils[2],
  coils[3],
  microsteps=None
)

def stepper_fwd():
    print("Giro horario")
    for _ in range(STEPS):
        stepper_motor.onestep(direction=stepper.FORWARD)
        time.sleep(DELAY)
    stepper_motor.release()


def stepper_back():
    print("Giro antihorario")
    for _ in range(STEPS):
        stepper_motor.onestep(direction=stepper.BACKWARD)
        time.sleep(DELAY)
    stepper_motor.release()


print("====================")
print("==Iniciando Prueba==")
print("====================")
while True:
    ledBlanco.value = False

    y = obtener_voltaje(eje_y)

    if not interruptor.value:
        if y < 0.3:
            stepper_back()
            print('Dirección: Abajo')
        elif y > 3.0:
            stepper_fwd()
            print('Dirección: Arriba')
    else:
        parpadeo(0.5)
        print('Detención por fin de rango de movimiento')
