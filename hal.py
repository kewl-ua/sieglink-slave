#!/usr/bin/env python3
# Hardware Abstraction Layer

import RPi.GPIO as GPIO
import time


def make_hal(pins):
    switch_pins = pins['switches_pins']
    pwm_pins = pins['pwm_pins']

    pwm_instances = {}

    def setup():
        GPIO.setmode(GPIO.BCM)

        for pin in switch_pins:
            GPIO.setup(pin, GPIO.OUT)

        for pin in pwm_pins:
            GPIO.setup(pin, GPIO.OUT)
            pwm_instances[pin] = GPIO.PWM(pin, 50)
            pwm_instances[pin].start(0)

    def cleanup():
        for pwm in pwm_instances.values():
            pwm.stop()
        GPIO.cleanup()

    def update_switch(switch_index, state):
        pin = switch_pins[switch_index - 1]
        if state:
            print(f'Setting pin {pin} to HIGH')
            GPIO.output(pin, GPIO.HIGH)
        else:
            GPIO.output(pin, GPIO.LOW)

    def set_pwm_duty_cycle(pin_index, value):
        pin = pwm_pins[pin_index]
        pwm_instances[pin].ChangeDutyCycle(value)

    return setup, cleanup, update_switch, set_pwm_duty_cycle


# Test
def test():
    setup, cleanup, update_switch, set_pwm_duty_cycle = make_hal({
        'switches_pins': [17, 27, 22, 23, 26],
        'pwm_pins': [12, 13]
    })
    setup()

    for i in range(1, 6):
        update_switch(i, True)
        time.sleep(1)
        update_switch(i, False)

    cleanup()


if __name__ == '__main__':
    test()
