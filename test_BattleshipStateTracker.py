from BattleshipStateTracker import BattleshipStateTracker

import unittest

class TestBattleshipStateTrackerMethods(unittest.TestCase):

    def test_init_valid_inputs(self):
        bst = BattleshipStateTracker(10, 10)
        self.assertEqual(bst.height, 10)
        self.assertEqual(bst.width, 10)

    def test_init_invalid_height_and_width(self):
        with self.assertRaises(ValueError) as context:
            BattleshipStateTracker(-1, -1)
        self.assertTrue('Height and width must be positive!' in str(context.exception))

    def test_add_battleship_valid_inputs(self):
        bst = BattleshipStateTracker(10, 10)
        bst.add_battleship(0, 0, 'h', 3)
        # check no. of ship
        self.assertEqual(bst.ship_count, 1)
        # check no. of undamaged sections of the ship
        self.assertEqual(bst.ship_section[1], 3)
        # check ship is properly placed on the board
        self.assertEqual(bst.board[(0, 0)][0], 1)
        self.assertEqual(bst.board[(1, 0)][0], 1)
        self.assertEqual(bst.board[(2, 0)][0], 1)

    def test_add_battleship_invalid_coordinate(self):
        bst = BattleshipStateTracker(10, 10)
        with self.assertRaises(ValueError) as context:
            bst.add_battleship(-1, -1, 'h', 3)
        self.assertTrue('Invalid coordinate!' in str(context.exception))
    
    def test_add_battleship_invalid_orientation(self):
        bst = BattleshipStateTracker(10, 10)
        with self.assertRaises(ValueError) as context:
            bst.add_battleship(0, 0, 'x', 3)
        self.assertTrue('Invalid orientation!' in str(context.exception))
    
    def test_add_battleship_invalid_ship_length(self):
        bst = BattleshipStateTracker(10, 10)
        with self.assertRaises(ValueError) as context:
            bst.add_battleship(0, 0, 'h', 0)
        self.assertTrue('Invalid ship length!' in str(context.exception))
    
    def test_take_attack_valid_inputs(self):
        bst = BattleshipStateTracker(10, 10)
        bst.take_attack(0, 0)
        # check if board is marked correctly
        self.assertTrue(bst.board[(0, 0)][1])
    
    def test_take_attack_invalid_coordinate(self):
        bst = BattleshipStateTracker(10, 10)
        with self.assertRaises(ValueError) as context:
            bst.take_attack(-1, -1)
        self.assertTrue('Invalid coordinate!' in str(context.exception))
    
    def test_take_attack_repeated(self):
        bst = BattleshipStateTracker(10, 10)
        bst.take_attack(0, 0)
        with self.assertRaises(ValueError) as context:
            bst.take_attack(0, 0)
        self.assertTrue('You have already been attacked in this location!' in str(context.exception))

    def test_get_status(self):
        bst = BattleshipStateTracker(10, 10)
        bst.add_battleship(0, 0, 'h', 1)
        bst.add_battleship(2, 2, 'h', 1)
        # make sure player hasn't lost the game
        self.assertGreater(bst.get_status(), 0)
        bst.take_attack(0, 0)
        bst.take_attack(2, 2)
        # make sure player has lost the game
        self.assertEqual(bst.get_status(), 0)

if __name__ == '__main__':
    unittest.main()
