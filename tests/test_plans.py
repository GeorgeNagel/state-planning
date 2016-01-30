import json
from unittest import TestCase

from planning.state import State
from planning.goals import dead_goal_factory


class TestPlan(TestCase):
    def setUp(self):
        initial_state_dict = {
            'characters': {
                'alice': {
                    'alive': True
                },
                'bob': {
                    'alive': True
                }
            }
        }
        self.state = State(json.dumps(initial_state_dict))
        self.goal_fn = dead_goal_factory('bob')

    def test_stuff(self):
        self.assertTrue(True)
