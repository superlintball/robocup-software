import unittest 
import robocup
import main
import evaluation.shooting
import constants

class Moc_Robot:
	def __init__(self, x, y):
		self.pos = robocup.Point(x, y)
		self.visible = True;

	def set_pos(self, x, y):
		self.pos = robocup.Point(x, y)

class TestShooting(unittest.TestCase):
	def __init__(self, *args, **kwargs):
		super(TestShooting, self).__init__(*args, **kwargs)
		self.system_state = robocup.SystemState()	

	def setUp(self):
		main.set_system_state(self.system_state)

		for robot in main.system_state().their_robots:
			robot.set_vis_for_testing(True)

		self.length = constants.Field.Length
		self.width = constants.Field.Width
		self.botRadius = constants.Robot.Radius

		self.their_robots = main.system_state().their_robots[0:5]
		self.our_robots = main.system_state().our_robots[0:5]

		self.success = 1
		self.failure = 0



	def eval_shot(self, x, y, excluded_robots=[]):
		return evaluation.shooting.eval_shot(robocup.Point(x, y), excluded_robots)


	# Set the location of a robot 
	# We must use this function so that the C++ can act on the robot location
	# 
	# @param a_bot: bot to change position
	# @param x: new x position of bot
	# @param y: new y position of bot
	#
	def set_bot_pos(self, a_bot, x, y):
		a_bot.set_pos_for_testing(robocup.Point(x, y))

	def test_eval_shot_clear_field(self):

		self.assertEqual(self.eval_shot(0, self.length), self.success)
		
		self.assertEqual(self.eval_shot(0, 3 * self.length / 4), self.success)

		self.assertEqual(self.eval_shot(0, self.length / 2 + self.botRadius), self.success)

		self.assertGreater(self.eval_shot(self.width / 4, 3 * self.length / 4), 0.99)
		self.assertGreater(self.eval_shot(self.width / -4, 3 * self.length / 4), 0.99)

		self.assertGreater(self.eval_shot(self.width / 4, self.length / 2 + self.botRadius), 0.95)
		self.assertGreater(self.eval_shot(self.width / -4, self.length / 2 + self.botRadius), 0.95)

	@unittest.skip("demonstrating skipping")
	def test_eval_shot_problem_cases(self):
		# This case return almost 1 when it should fail
		self.assertEqual(self.eval_shot(0, 2 * self.length), self.failure)

		# This case returns 0 when it should return 1
		self.assertEqual(self.eval_shot(0, self.length / 2), self.success)

		# Corner shots do not have 100% chance to hit the goal
		self.assertGreater(self.eval_shot(self.width / 2, self.length), 0.99)

	def test_eval_shot_with_bots_and_exclusion(self):
		their_bot1, their_bot2, their_bot3, their_bot4, their_bot5 = self.their_robots
		our_bot1, our_bot2, our_bot3, our_bot4, our_bot5 = self.our_robots

		shooting_pos = 3 * self.length / 4

		self.set_bot_pos(their_bot1, 0, shooting_pos + self.botRadius)
		self.assertLess(self.eval_shot(0, shooting_pos), 0.05)

		self.assertEqual(self.eval_shot(0, shooting_pos, [their_bot1]), self.success)

		self.set_bot_pos(our_bot1, 0, shooting_pos + self.botRadius)
		self.assertEqual(self.eval_shot(0, shooting_pos, [their_bot1]), 1)
		
		self.set_bot_pos(their_bot1, 0, shooting_pos + self.length / 8)
		self.assertLess(self.eval_shot(0, shooting_pos), self.success)
		self.assertEqual(self.eval_shot(0, shooting_pos, [their_bot1]), self.success)


	def test_eval_shot_excluded_bots(self):
		their_bot1, their_bot2, their_bot3, their_bot4, their_bot5 = self.their_robots
		our_bot1, our_bot2, our_bot3, our_bot4, our_bot5 = self.our_robots

		print("hello 1")
		# self.assertEqual(self.eval_shot(0, 3 * length / 4, [their_bot1]), self.success)

