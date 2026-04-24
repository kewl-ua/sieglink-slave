#!/usr/bin/env python3
import sys
import json

from hal import make_hal
from adapters import make_tx16_adapter

# Constants

# Hardware
setup, cleanup, update_switch, set_pwm = make_hal({
    'switches_pins': [17, 27, 22, 23, 26],
    'pwm_pins': [12, 13],
})

# State
handle_tx16_message, get_tx16_state = make_tx16_adapter(update_switch, {
    # 'LEFT_X':  lambda v: set_pwm(0, v),
    # 'LEFT_Y':  lambda v: set_pwm(0, v),
    # 'RIGHT_X': lambda v: set_pwm(1, v),
    'RIGHT_Y': lambda v: set_pwm(0, v),
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

