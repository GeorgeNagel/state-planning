from unittest import TestCase

from planning.actions import Kill, Action, ImpossibleActionException
from planning.goals import dead_goal_factory
from planning.plans import plan_search, Plan, ImpossiblePlanException
from planning.state import State


class TestSimplePlan(TestCase):
    def setUp(self):
        self.initial_state_dict = {
            'characters': {
                'alice': {
                    'alive': True
                },
                'bob': {
                    'alive': True
                }
            }
        }
        self.state = State.from_dict(self.initial_state_dict)
        self.goal_fn = dead_goal_factory('bob')

    def test_already_satisfied(self):
        self.initial_state_dict['characters']['bob']['alive'] = False
        state = State.from_dict(self.initial_state_dict)
        plan = plan_search(['alice'], state, [Kill], self.goal_fn)
        self.assertIsNone(plan)

    def test_plan_alice_kill_bob(self):
        plan = plan_search(['alice'], self.state, [Kill], self.goal_fn)
        self.assertEqual(
            str(plan),
            str(Plan(actions=[
                Kill(['alice'], ['bob'])
            ]))
        )

    def test_plan_bob_kill_bob(self):
        plan = plan_search(['bob'], self.state, [Kill], self.goal_fn)
        self.assertEqual(
            str(plan),
            str(Plan(actions=[
                Kill(['bob'], ['bob'])
            ]))
        )


class TestMultiStepPlan(TestCase):
    def setUp(self):
        # Create the initial state
        initial_state_dict = {
            'characters': {
                'alice': {
                    'toes': 10
                }
            }
        }
        state = State.from_dict(initial_state_dict)

        # Create an action
        class AddToes(Action):
            name = 'add toes'

            def apply(self, state_dict):
                for character_key in self.objects:
                    state_dict['characters'][character_key]['toes'] += 1
                return state_dict

        # Create the goal verification function
        def enough_toes(state):
            state_dict = state.as_dict()
            return state_dict['characters']['alice']['toes'] >= 12

        self.goal_fn = enough_toes
        self.action = AddToes
        self.state = state

    def test_multi_step(self):
        plan = plan_search(['alice'], self.state, [self.action], self.goal_fn)
        self.assertEqual(
            str(plan),
            str(Plan(actions=[
                self.action(['alice'], ['alice']),
                self.action(['alice'], ['alice'])
            ]))
        )

    def test_impossible(self):
        """ Test finding a plan to an impossible goal. """
        def too_few_toes(state):
            state_dict = state.as_dict()
            return state_dict['characters']['alice']['toes'] <= 7

        with self.assertRaises(ImpossiblePlanException):
            plan_search(['alice'], self.state, [self.action], too_few_toes)


class TestConvincePlan(TestCase):
    def setUp(self):
        # Create the initial state
        initial_state_dict = {
            'characters': {
                'alice': {
                    'has_money': False
                },
                'bob': {
                    'has_money': True
                },
                'carol': {
                    'has_money': False
                }
            }
        }
        state = State.from_dict(initial_state_dict)

        # Create an action
        class GiveMoney(Action):
            name = 'give money'

            def apply(self, state_dict):
                for character_key in self.objects:
                    if not state_dict['characters'][character_key]['has_money']:
                        raise ImpossibleActionException()
                for character_key in self.objects:
                    state_dict['characters'][character_key]['has_money'] = False
                for character_key in self.subjects:
                    state_dict['characters'][character_key]['has_money'] = True
                return state_dict

        class Convince(Action):
            name = 'convince'

            def apply(self, state_dict):
                return state_dict

        # Create the goal verification function
        def carol_has_money(state):
            state_dict = state.as_dict()
            return state_dict['characters']['carol']['has_money']

        self.goal_fn = carol_has_money
        self.give_money = GiveMoney
        self.convince = Convince
        self.state = state

    def test_convince_plan(self):
        """ Test finding a plan where somebody must be convinced to perform an action. """
        plan = plan_search(['alice'], self.state, [self.give_money, self.convince], self.goal_fn)
        self.assertEqual(
            str(plan),
            str(Plan(actions=[
                self.convince(
                    ['alice'], ['bob'],
                    Plan(actions=[self.give_money(['bob'], ['carol'])])
                ),
            ])),
            str(Plan(actions=[
                self.convince(['alice'], ['bob']),
                self.give_money(['bob'], ['carol']),
                self.end_convince(['alice'], ['bob'])
            ]))
        )
