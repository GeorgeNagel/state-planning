from unittest import TestCase

from planning.actions import Kill
from planning.goals import dead_goal_factory
from planning.plans import plan_search, Plan
from planning.state import State


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
        self.state = State.from_dict(initial_state_dict)
        print "STATE1: %s" % self.state._state_string
        self.goal_fn = dead_goal_factory('bob')

    def test_plan_alice_kill_bob(self):
        plan = plan_search('alice', self.state, [Kill], self.goal_fn)
        self.assertEqual(
            str(plan),
            str(Plan([
                Kill(['alice'], ['bob'])
            ]))
        )

    def test_plan_bob_kill_bob(self):
        plan = plan_search('bob', self.state, [Kill], self.goal_fn)
        self.assertEqual(
            str(plan),
            str(Plan([
                Kill(['bob'], ['bob'])
            ]))
        )
