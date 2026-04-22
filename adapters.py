import sys
from typing import TypedDict

from state import StateFields, make_state


class SiegLinkMessage(TypedDict):
    type: str  # 'sticks' | 'switches'
    data: dict
    timestamp: float


TX16_TO_STATE_MAP = {
    'ABS_RX':       'LEFT_X',
    'ABS_Z':        'LEFT_Y',
    'ABS_X':        'RIGHT_X',
    'ABS_Y':        'RIGHT_Y',
    'ABS_RY':       'AUX_1',
    'ABS_RZ':       'AUX_2',
    'ABS_THROTTLE': 'AUX_3',
    'ABS_RUDDER':   'AUX_4',
    'BTN_SOUTH':    'AUX_5',
}

STICK_FIELDS  = {'LEFT_X', 'LEFT_Y', 'RIGHT_X', 'RIGHT_Y'}
SWITCH_FIELDS = {'AUX_1', 'AUX_2', 'AUX_3', 'AUX_4', 'AUX_5'}


def make_tx16_adapter(update_switch, pwm_handlers):
    state = make_state()

    def handle_message(message: SiegLinkMessage):
        msg_type = message['type']
        data = message['data']

        print('Received message: ', message)

        for hid_key, value in data.items():
            state_key = TX16_TO_STATE_MAP.get(hid_key)

            if state_key is None:
                print(f'[UNMAPPED] {hid_key} = {value}', file=sys.stderr)
                continue

            state[state_key] = value

            if msg_type == 'switches' and state_key in SWITCH_FIELDS:
                aux_index = int(state_key.split('_')[1])
                update_switch(aux_index, bool(value))

            elif msg_type == 'sticks' and state_key in pwm_handlers:
                pwm_handlers[state_key](value)

    def get_state() -> StateFields:
        return state

    return handle_message, get_state


# Test
def test():
    def mock_update_switch(aux_index, state):
        print(f'HAL update_switch({aux_index}, {state})')

    def mock_pwm(label):
        return lambda value: print(f'HAL pwm[{label}]({value})')

    handle_message, get_state = make_tx16_adapter(mock_update_switch, {
        'LEFT_X':  mock_pwm('pin12'),
        'LEFT_Y':  mock_pwm('pin12'),
        'RIGHT_X': mock_pwm('pin13'),
        'RIGHT_Y': mock_pwm('pin13'),
    })

    print('----- Initial state -----')
    print(get_state())

    mock_sticks: SiegLinkMessage = {
        'type': 'sticks',
        'data': {'LEFT_X': 1024, 'timestamp': 1745000000}
    }
    mock_switches: SiegLinkMessage = {
        'type': 'switches',
        'data': {'AUX_1': 1, 'timestamp': 1745000001}
    }

    handle_message(mock_sticks)
    handle_message(mock_switches)

    print('----- Patched state -----')
    print(get_state())


if __name__ == '__main__':
    test()


    print('----- Patched state -----')
    print(get_state())


if __name__ == '__main__':
    test()

