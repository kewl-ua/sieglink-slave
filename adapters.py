import sys
from typing import TypedDict

from state import StateFields, make_state


class TX16Event(TypedDict):
    event_type: str
    code: int
    name: str
    value: int


TX16_TO_STATE_MAP = {
    'ABS_RX': 'LEFT_X',
    'ABS_Z': 'LEFT_Y',
    'ABS_X': 'RIGHT_X',
    'ABS_Y': 'RIGHT_Y',
    'ABS_RY': 'AUX_1',
    'ABS_RZ': 'AUX_2',
    'ABS_THROTTLE': 'AUX_3',
    'ABS_RUDDER': 'AUX_4',
    'BTN_SOUTH': 'AUX_5'
}

SWITCH_EVENTS = {'AUX_1', 'AUX_2', 'AUX_3', 'AUX_4', 'AUX_5'}


def make_tx16_adapter(update_switch, pwm_handlers):
    state = make_state()

    def handle_event(event: TX16Event):
        state_key = TX16_TO_STATE_MAP.get(event['name'])

        if state_key is None:
            print(f'[UNMAPPED event] {event["event_type"]} / {event["name"]} = {event["value"]}', file=sys.stderr)
            return

        print(f'[EVENT] {state_key} = {event["value"]}')

        state[state_key] = event['value']

        if state_key in SWITCH_EVENTS:
            aux_index = int(state_key.split('_')[1])
            update_switch(aux_index, bool(event['value']))

        if state_key in pwm_handlers:
            pwm_handlers[state_key](event['value'])

    def get_state() -> StateFields:
        return state

    return handle_event, get_state


# Test
def test():
    def mock_update_switch(aux_index, state):
        print(f'HAL update_switch({aux_index}, {state})')

    def mock_pwm(label):
        return lambda value: print(f'HAL pwm[{label}]({value})')

    handle_event, get_state = make_tx16_adapter(mock_update_switch, {
        'LEFT_X': mock_pwm('pin12'),
        'LEFT_Y': mock_pwm('pin12'),
        'RIGHT_X': mock_pwm('pin13'),
        'RIGHT_Y': mock_pwm('pin13'),
    })

    mock_event: TX16Event = {
        'event_type': 'EV_ABS',
        'code': 2,
        'name': 'ABS_Z',
        'value': 3
    }

    print('----- Initial state -----')
    print(get_state())

    print('---- Simulated event ----')
    print(mock_event)

    handle_event(mock_event)

    print('----- Patched state -----')
    print(get_state())


if __name__ == '__main__':
    test()

    print('----- Initial state -----')
    print(get_state())

    print('---- Simulated event ----')
    print(mock_event)

    handle_event(mock_event)

    print('----- Patched state -----')
    print(get_state())


if __name__ == '__main__':
    test()

