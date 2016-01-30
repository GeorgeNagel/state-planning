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
        for character in state_dict['characters']:
            if character['name'] in self.subjects:
                if character['alive'] is False:
                    raise ImpossibleException('A dead person cannot kill')
        for character in state_dict['characters']:
            if character['name'] in self.objects:
                if character['alive'] is False:
                    raise ImpossibleException('A dead person cannot be killed')
        for character in state_dict['characters']:
            if character['name'] in self.objects:
                character['alive'] = False
        return state_dict


class Convince(Action):
    # Change the planning frame from the action's subject to the action's object
    name = 'convince'

    def apply():
        # changes the planning frame
        pass
