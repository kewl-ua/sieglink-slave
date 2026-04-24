#!/usr/bin/env python3
# Hardware Abstraction Layer

import pigpio
import time


def make_hal(pins):
    switch_pins = pins['switches_pins']
    pwm_pins = pins['pwm_pins']

    PWM_FREQUENCY_HZ = 50
    PWM_PERIOD_US = 1_000_000 // PWM_FREQUENCY_HZ  # 20 000 мкс

    pi = pigpio.pi()

    def setup():
        for pin in switch_pins:
            pi.set_mode(pin, pigpio.OUTPUT)
            pi.write(pin, 0)

        for pin in pwm_pins:
            pi.set_mode(pin, pigpio.OUTPUT)
            pi.set_PWM_frequency(pin, PWM_FREQUENCY_HZ)
            pi.set_servo_pulsewidth(pin, 0)

    def cleanup():
        for pin in pwm_pins:
            pi.set_servo_pulsewidth(pin, 0)
        pi.stop()

    def update_switch(switch_index, state):
        pin = switch_pins[switch_index - 1]
        pi.write(pin, 1 if state else 0)

    SERVO_MIN_US = 500
    SERVO_MAX_US = 2500

    def set_pwm(pin_index, pulse_width_us):
        pin = pwm_pins[pin_index]
        pw = max(SERVO_MIN_US, min(SERVO_MAX_US, pulse_width_us + SERVO_MIN_US))
        pi.set_servo_pulsewidth(pin, pw)

    return setup, cleanup, update_switch, set_pwm


# Test
def test():
    setup, cleanup, update_switch, set_pwm = make_hal({
        'switches_pins': [17, 27, 22, 23, 26],
        'pwm_pins': [12, 13],
    })
    setup()

    for i in range(1, 6):
        update_switch(i, True)
        time.sleep(1)
        update_switch(i, False)

    cleanup()


if __name__ == '__main__':
    test()


    cleanup()


if __name__ == '__main__':
    test()
