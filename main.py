import json

from planning.state import State, StateHistory
from planning.actions import Kill
from planning.goals import dead_goal_factory


def plan_search(actor, state, state_validation_function):
    # actor - main agent in the current planning frame
    pass

if __name__ == "__main__":
    initial_state_json = {
        'characters': {
            "steven": {
                'name': 'Steven',
                'alive': True
            },
            "hank": {
                'name': 'Hank',
                'alive': True
            },
            "harris": {
                'name': 'Harris',
                'alive': True
            }
        }
    }
    initial_state = State(json.dumps(initial_state_json))
    dead_goal_verify = dead_goal_factory('harris')
    print "SATISFIED?: %s" % dead_goal_verify(initial_state)
    state_history = StateHistory(initial_state=initial_state)
    state_history.apply_action(Kill(['hank'], ['harris']))
    print state_history.pretty()
    print "SATISFIED?: %s" % dead_goal_verify(State(state_history._history[-1]))
