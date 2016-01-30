import json


class State(object):
    _state_string = ""

    @classmethod
    def from_dict(cls, state_dict):
        return cls(json.dumps(state_dict, sort_keys=True))

    def __init__(self, state_string):
        super(State, self).__setattr__("_state_string", state_string)

    def as_string(self):
        return self._state_string

    def as_dict(self):
        return json.loads(self._state_string)

    def __setattr__(self, name, value):
        raise AttributeError("State cannot be modified.")

    def pretty(self):
        """ A pretty-printable representation of the state. """
        return json.dumps(json.loads(self.state), indent=4, sort_keys=True)

    def __repr__(self):
        return "<State: %s>" % self.__str__()

    def __str__(self):
        return self._state_string

    def __unicode__(self):
        return self.__str__()

    def apply_action(self, action):
        """ Apply an action to this state, return a new State. """
        new_state_dict = action.apply(self.as_dict())
        return State.from_dict(new_state_dict)


class StateHistory(object):
    _history = None

    def __init__(self, initial_state=None):
        self._history = []
        if initial_state:
            self._history.append(initial_state.as_string())

    def pretty(self):
        """ A pretty-printable representation of the state history. """
        # Pretty print each state and action in the history
        history_list = [json.loads(str(el)) for el in self._history]
        return json.dumps(history_list, indent=4, sort_keys=True)

    def __repr__(self):
        return self.__str__()

    def __unicode__(self):
        return self.__str__()

    def __str__(self):
        return str(self._history)

    def set_state(self, new_state):
        self._history.append(new_state)

    def apply_action(self, action):
        # Keep track of the actions as well as the states they transition to/from
        current_state = self._history[-1]
        new_state = action.apply(json.loads(current_state))
        self._history.append(json.dumps(action.as_dict()))
        self._history.append(json.dumps(new_state))
