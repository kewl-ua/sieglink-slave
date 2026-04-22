from typing import TypedDict, get_type_hints


class StateFields(TypedDict):
    LEFT_X: int
    LEFT_Y: int
    RIGHT_X: int
    RIGHT_Y: int
    AUX_1: int
    AUX_2: int
    AUX_3: int
    AUX_4: int
    AUX_5: int


def make_state(fields: StateFields = None) -> StateFields:
    keys = list(get_type_hints(StateFields).keys())
    if fields is not None:
        return {k: fields[k] for k in keys}
    return {k: 0 for k in keys}


# Test
def test():
    mock_fields = {
        'LEFT_X': 0,
        'LEFT_Y': 1000,
        'RIGHT_X': 0,
        'RIGHT_Y': 0,
        'AUX_1': 0,
        'AUX_2': 0,
        'AUX_3': 0,
        'AUX_4': 0,
        'AUX_5': 0
    }

    print(make_state(mock_fields))


if __name__ == '__main__':
    test()
