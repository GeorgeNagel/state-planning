import json

from planning.state import State, StateHistory
from planning.actions import Kill


def plan_search(actor, state, state_validation_function):
    # actor - main agent in the current planning frame
    pass

if __name__ == "__main__":
    initial_state_json = {
        'characters': [
            {
                'name': 'Steven',
                'alive': True
            },
            {
                'name': 'Hank',
                'alive': True
            },
            {
                'name': 'Harris',
                'alive': True
            }
        ]
    }
    initial_state = State(json.dumps(initial_state_json))
    state_history = StateHistory(initial_state=initial_state)
    state_history.apply_action(Kill(['Harris'], ['Hank']))
    print state_history.pretty()
