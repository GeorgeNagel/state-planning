def dead_goal_factory(character_key):
    def dead_goal_verify(state):
        state_dict = state.as_dict()
        obj = state_dict['characters'][character_key]
        return not obj["alive"]
    return dead_goal_verify
