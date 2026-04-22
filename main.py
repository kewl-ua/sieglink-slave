#!/usr/bin/env python3
import sys
import json

from hal import make_hal
from adapters import make_tx16_adapter

# Constants

# Hardware
setup, cleanup, update_switch, set_pwm_duty_cycle = make_hal({
    'switches_pins': [17, 27, 22, 23, 26],
    'pwm_pins': [12, 13]
})

def make_pwm_sender(pin_index):
    def send(value):
        duty = max(0.0, min(100.0, value / 2000 * 100))
        set_pwm_duty_cycle(pin_index, duty)
    return send

# State
handle_tx16_message, get_tx16_state = make_tx16_adapter(update_switch, {
    # 'LEFT_X':  make_pwm_sender(0),
    'LEFT_Y':  make_pwm_sender(0),
    # 'RIGHT_X': make_pwm_sender(0),
    # 'RIGHT_Y': make_pwm_sender(1),
})

def loop():
    while True:
        line = sys.stdin.readline()

        if not line:
            break

        line = line.strip()

        if not line:
            continue

        try:
            data = json.loads(line)
        except json.JSONDecodeError:
            print('Invalid JSON: ', line, file=sys.stderr)
            continue

        handle_tx16_message(data)

# Entry point
def main():
    setup()
    loop()
    cleanup()

if __name__ == '__main__':
    main()

