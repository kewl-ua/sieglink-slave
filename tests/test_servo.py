import RPi.GPIO as GPIO
import time

SERVO_PIN = 12
DELAY = 0.05
STEP = 5

GPIO.setmode(GPIO.BCM)
GPIO.setup(SERVO_PIN, GPIO.OUT)

pwm = GPIO.PWM(12, 50)
pwm.start(0)

def set_servo_angle(angle):
    """ Set servo angle (0 to 180 degrees)"""
    # Convert angle to duty cycle
    # Typical: 0° = 2.5%, 90° = 7.5%, 180° = 12.5%
    duty = 2.5 + (angle / 180.0) * 10.0

    pwm.ChangeDutyCycle(duty)
    time.sleep(DELAY)

try:
    while True:
        # Sweep servo back and forth
        for angle in range(0, 181, STEP):
            set_servo_angle(angle)
            print(f'Angle: {angle}°')
            time.sleep(DELAY)

        for angle in range(180, -1, -STEP):
            set_servo_angle(angle)
            print(f'Angle: {angle}°')
            time.sleep(DELAY)
except KeyboardInterrupt:
    print('\nStopped by user.')
    pwm.stop()
    GPIO.cleanup()


