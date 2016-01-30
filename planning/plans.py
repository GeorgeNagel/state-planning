import json

MAX_PLAN_DEPTH = 100


class ImpossiblePlanException(Exception):
    pass


def plan_search(agent_key, state, action_classes, goal_verify_fn, plan=None):
    """ Return a sequence of actions which satisfies the goal verification function. """
    if goal_verify_fn(state):
        return plan

    if plan is None:
        plan = Plan()
    elif len(plan.actions) >= MAX_PLAN_DEPTH:
        raise ImpossiblePlanException

    for action_cls in action_classes:
        for character_key in state.as_dict()['characters']:
            action = action_cls([agent_key], [character_key])
            next_state = state.apply_action(action)
            possible_plan = plan.add_action(action)
            return plan_search(agent_key, next_state, action_classes, goal_verify_fn, plan=possible_plan)


class Plan(object):
    """ A sequence of actions. """
    actions = None

    def __init__(self, actions=None):
        if actions is None:
            actions = []
        self.actions = actions

    def __str__(self):
        actions = [action.as_dict() for action in self.actions]
        return json.dumps(actions, indent=4, sort_keys=True)

    def add_action(self, action):
        actions = self.actions + [action]
        return Plan(actions)
