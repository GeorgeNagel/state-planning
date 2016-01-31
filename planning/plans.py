import json

from planning.actions import Convince, EndConvince, ImpossibleActionException

MAX_PLAN_DEPTH = 10


class ImpossiblePlanException(Exception):
    pass

# def plan_search(agent_key_stack, state, action_classes, goal_verify_fn, plan=None, convince=True):
#     """
#     Return a sequence of actions which satisfies the goal verification function.
#     agent_key_stack => A list of character keys with the character of the current frame in front.
#     convince => allow characters to convince each-other.
#     """
#     if goal_verify_fn(state):
#         return plan

#     if plan is None:
#         plan = Plan()
#     elif len(plan.actions) >= MAX_PLAN_DEPTH:
#         raise ImpossiblePlanException

#     if convince:
#         action_classes += [Convince, EndConvince]

#     agent_key = agent_key_stack[-1]
#     for action_cls in action_classes:
#         for character_key in state.as_dict()['characters']:
#             action = action_cls([agent_key], [character_key])
#             next_state = state.apply_action(action)
#             try:
#                 possible_plan = plan.add_action(action)
#             except ImpossibleActionException:
#                 raise ImpossiblePlanException()
#             if action == Convince:
#                 # The selected character becomes the primary agent of future actions
#                 agent_key_stack.push(character_key)
#             elif action == EndConvince:
#                 # The primary agent cedes control over action
#                 agent_key_stack.pop(-1)
#             try:
#                 return plan_search(agent_key_stack, next_state, action_classes, goal_verify_fn, plan=possible_plan)  # noqa
#             except ImpossiblePlanException:
#                 continue


def plan_search(agent_key_stack, initial_state, action_classes, goal_verify_fn, plans=None, convince=True):  # noqa
    """
    Return a sequence of actions which satisfies the goal verification function.
    agent_key_stack => A list of character keys with the character of the current frame in front.
    convince => allow characters to convince each-other.
    """
    # Check if already satisfied:
    if goal_verify_fn(initial_state):
        return None

    if plans is None:
        plans = []
        agent_key = agent_key_stack[-1]
        for action_cls in action_classes:
            for character_key in initial_state.as_dict()['characters']:
                action = action_cls([agent_key], [character_key])
                plan = Plan(actions=[action])
                plans.append(plan)
    elif len(plans[0].actions) >= MAX_PLAN_DEPTH:
        raise ImpossiblePlanException

    # Check if any plans found so far complete the goal
    for plan in plans:
        states = [initial_state]
        for action in plan.actions:
            new_state = states[-1].apply_action(action)
            states.append(new_state)
        final_state = states[-1]
        goal_reached = goal_verify_fn(final_state)
        if goal_reached:
            return plan

    # Create new branches of plans from each plan
    new_plans = []
    for plan in plans:
        # Create new following plans
        agent_key = agent_key_stack[-1]
        for action_cls in action_classes:
            for character_key in initial_state.as_dict()['characters']:
                action = action_cls([agent_key], [character_key])
                new_plan = plan.add_action(action)
                new_plans.append(new_plan)

    return plan_search(agent_key_stack, initial_state, action_classes, goal_verify_fn, plans=new_plans, convince=convince)  # noqa


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
