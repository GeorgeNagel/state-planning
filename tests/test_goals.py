import json
from unittest import TestCase

from planning.state import State
from planning.goals import dead_goal_factory


class TestDeadGoal(TestCase):

    def test_not_yet_satisfied(self):
        state_dict = {
            'characters': {
                'alice': {
                    'alive': True
                },
                'bob': {
                    'alive': True
                }
            }
        }
        state = State(json.dumps(state_dict))
        goal = dead_goal_factory('bob')
        self.assertFalse(goal(state))

    def test_satisfied(self):
        state_dict = {
            'characters': {
                'alice': {
                    'alive': True
                },
                'bob': {
                    'alive': False
                }
            }
        }
        state = State(json.dumps(state_dict))
        goal = dead_goal_factory('bob')
        self.assertTrue(goal(state))
