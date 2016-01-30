import json


def plan_search(agent_key, state, action_classes, goal_verify_fn):
    # Recursively search through states and actions until the goal is satisfied
    for action_cls in action_classes:
        for character_key in state.as_dict()['characters']:
            action = action_cls([agent_key], [character_key])
            if goal_verify_fn(state.apply_action(action)):
                return Plan([action])


class Plan(object):
    """ A sequence of actions. """
    actions = None

    def __init__(self, actions):
        self.actions = actions

    def __str__(self):
        actions = [action.as_dict() for action in self.actions]
        return json.dumps(actions, indent=4, sort_keys=True)
