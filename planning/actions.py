import json


class Action(object):
    name = "Generic Action"
    subjects = None
    objects = None

    def apply(self, state_dict):
        raise NotImplementedError

    def __init__(self, subjects, objects):
        if subjects:
            self.subjects = subjects
        else:
            self.subjects = []
        if objects:
            self.objects = objects
        else:
            self.objects = []

    def to_json(self):
        """ Create a json-serializable object representing this action instance. """
        return {
            "name": self.name,
            "subjects": self.subjects,
            "objects": self.objects
        }

    def __repr__(self):
        return "<Action: %s>" % self.__str__()

    def __str__(self):
        return json.dumps(self.to_json(), sort_keys=True)


class ImpossibleException(Exception):
    pass


class Kill(Action):
    name = 'kill'

    def apply(self, state_dict):
        # Check preconditions
        for character_key in self.subjects:
            if not state_dict['characters'][character_key]['alive']:
                raise ImpossibleException('A dead person cannot kill')
        for character_key in self.objects:
            if not state_dict['characters'][character_key]['alive']:
                raise ImpossibleException('A dead person cannot be killed')

        # Modify state
        for character_key in self.objects:
            state_dict['characters'][character_key]['alive'] = False
        return state_dict


class Convince(Action):
    # Change the planning frame from the action's subject to the action's object
    name = 'convince'

    def apply():
        # changes the planning frame
        pass
