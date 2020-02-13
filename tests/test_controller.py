import unittest
from unittest.mock import call
from unittest.mock import patch

from internal import Controller
from model import Command
from model import DataErrorException
from model import Orientation
from model import Position
from model import Rover


class ControllerTestCase(unittest.TestCase):

    def setUp(self):
        self.controller = Controller()
        self.position = Position(3, 3)
        self.northRover = Rover(position=self.position, orientation=Orientation.NORTH)
        self.eastRover = Rover(position=self.position, orientation=Orientation.EAST)
        self.southRover = Rover(position=self.position, orientation=Orientation.SOUTH)
        self.westRover = Rover(position=self.position, orientation=Orientation.WEST)


class TestMoveRovers(ControllerTestCase):

    def setUp(self):
        super().setUp()
        self.instructions = ['5 5\n', '1 2 N\n', 'LMLMLMLMM\n', '3 3 E\n', 'MMRMMRMRRM\n']

    # Check that clean data function is called with the correct arguments
    def test_clean_data_is_called_with_params(self):
        with patch.object(target=Controller, attribute='clean_data') as mocked_clean_data:
            self.controller.move_rovers(instructions=self.instructions)
            mocked_clean_data.assert_called_once_with(instructions=self.instructions)

    # Check that calculate next position function is called when the command is a 'M' with the correct arguments
    def test_calculate_next_position_is_called_with_params(self):
        with patch.object(target=Controller, attribute='clean_data') as mocked_clean_data:
            rover = self.northRover
            cleanInstructions = [Position(4, 4), [rover, 'M']]
            mocked_clean_data.return_value = cleanInstructions
            with patch.object(target=Controller, attribute='calculate_next_position') as mocked_calculate_next_position:
                mocked_calculate_next_position.return_value = Position(5, 4)
                self.controller.move_rovers(instructions=self.instructions)
                mocked_calculate_next_position.assert_called_once_with(rover=rover)

    # Check that rotate rover function is called when the command is a 'L' or 'R' with the correct arguments
    def test_calculate_next_position_is_called_with_params(self):
        with patch.object(target=Controller, attribute='clean_data') as mocked_clean_data:
            rover = self.northRover
            cleanInstructions = [Position(4, 4), [rover, 'LR']]
            mocked_clean_data.return_value = cleanInstructions
            with patch.object(target=Controller, attribute='rotate_rover') as mocked_rotate_rover:
                calls = [call(rover=rover, command='L'), call(rover=rover, command='R')]
                self.controller.move_rovers(instructions=self.instructions)
                mocked_rotate_rover.assert_has_calls(calls=calls)

    # Check that move rovers function returns the rovers in the correct positions:
    def test_move_rovers_return_value(self):
        expectedResult = [Rover(position=Position(1, 3), orientation=Orientation.NORTH), Rover(position=Position(5, 1), orientation=Orientation.EAST)]
        result = self.controller.move_rovers(instructions=self.instructions)
        self.assertEqual(result, expectedResult)


class TestCleanData(ControllerTestCase):

    # Check that when the instructions are correct, the clean instructions are properly returned
    def test_data_is_correctly_cleaned(self):
        instructions = ['5 5\n', '1 2 N\n', 'LMLMLMLMM\n', '3 3 E\n', 'MMRMMRMRRM\n']
        expectedResult = [Position(5, 5), [Rover(position=Position(1, 2), orientation=Orientation.NORTH), 'LMLMLMLMM'], [Rover(position=Position(3, 3), orientation=Orientation.EAST), 'MMRMMRMRRM']]
        result = self.controller.clean_data(instructions=instructions)
        self.assertEqual(result, expectedResult)

    # Check that a data error exception is raised when the top right position is not correct
    def test_data_exception_raised_when_top_right_is_uncorrect(self):
        instructions = [['1 2 N\n', 'LMLMLMLMM\n'], ['5 5 ER\n', '1 2 N\n', 'LMLMLMLMM\n'], ['A 5\n', '1 2 N\n', 'LMLMLMLMM\n'], ['5 E\n', '1 2 N\n', 'LMLMLMLMM\n']]
        for instruction in instructions:
            self.assertRaises(DataErrorException, self.controller.clean_data, instruction)

    # Check that a data error exception is raised when the rover's intial position is not correct
    def test_data_exception_raised_when_initial_position_is_uncorrect(self):
        instructions = [['5 5\n', '1 2 A\n', 'LMLMLMLMM\n'], ['5 5\n', '1 2 3\n', 'LMLMLMLMM\n'], ['5 5\n', '1 N\n', 'LMLMLMLMM\n'], ['5 5\n', 'A 2 N\n', 'LMLMLMLMM\n'], ['5 5\n', '1 A N\n', 'LMLMLMLMM\n']]
        for instruction in instructions:
            self.assertRaises(DataErrorException, self.controller.clean_data, instruction)

    # Check that a data error exception is raised when a command is not correct
    def test_data_exception_raised_when_command_is_uncorrect(self):
        instructions = [['5 5\n', '1 2 N\n', 'LMLMLMLMM1\n'], ['5 5\n', '1 2 N\n', 'LMLMLMLMMP\n'], ['5 5\n', '1 2 N\n', 'LMLMLMLMM\n', '3 3 E\n']]
        for instruction in instructions:
            self.assertRaises(DataErrorException, self.controller.clean_data, instruction)

    # Check that a data error exception is raised when a the file is incomplete
    def test_data_exception_raised_when_file_is_incomplete(self):
        instructions = [[], ['5 5\n'], ['5 5\n', '1 2 N\n']]
        for instruction in instructions:
            self.assertRaises(DataErrorException, self.controller.clean_data, instruction)


class TestRotateRover(ControllerTestCase):

    # Check that the next orientation is correctly calculated when the command is right
    def test_rotation_is_correct_when_right(self):
        command = Command.RIGHT
        expectedResult = [Rover(position=self.position, orientation=Orientation.EAST), Rover(position=self.position, orientation=Orientation.SOUTH), Rover(position=self.position, orientation=Orientation.WEST), Rover(position=self.position, orientation=Orientation.NORTH)]
        result = [self.controller.rotate_rover(rover=self.northRover, command=command), self.controller.rotate_rover(rover=self.eastRover, command=command), self.controller.rotate_rover(rover=self.southRover, command=command), self.controller.rotate_rover(rover=self.westRover, command=command)]
        self.assertEqual(result, expectedResult)

    # Check that the next position is correctly calculated when the command is left
    def test_rotation_is_correct_when_left(self):
        command = Command.LEFT
        expectedResult = [Rover(position=self.position, orientation=Orientation.WEST), Rover(position=self.position, orientation=Orientation.NORTH), Rover(position=self.position, orientation=Orientation.EAST), Rover(position=self.position, orientation=Orientation.SOUTH)]
        result = [self.controller.rotate_rover(rover=self.northRover, command=command), self.controller.rotate_rover(rover=self.eastRover, command=command), self.controller.rotate_rover(rover=self.southRover, command=command), self.controller.rotate_rover(rover=self.westRover, command=command)]
        self.assertEqual(result, expectedResult)


class TestCalculateNextPosition(ControllerTestCase):

    # Check that the next position is correctly calculated
    def test_next_position_is_correct(self):
        expectedResult = [Position(3, 4), Position(4, 3), Position(3, 2), Position(2, 3)]
        result = [self.controller.calculate_next_position(rover=self.northRover), self.controller.calculate_next_position(rover=self.eastRover), self.controller.calculate_next_position(rover=self.southRover), self.controller.calculate_next_position(rover=self.westRover)]
        self.assertEqual(result, expectedResult)


class TestCheckPositionAvailable(ControllerTestCase):

    def setUp(self):
        super().setUp()
        self.occupiedPositions = [self.position]
        self.topSquare = Position(4, 4)

    # Check that check_position_available return True when the next position is not occupied and in the grid
    def test_next_position_is_available(self):
        nextPosition = Position(2, 3)
        self.assertTrue(self.controller.check_position_available(position=nextPosition, occupiedPositions=self.occupiedPositions, topSquare=self.topSquare))

    # Check that check_position_available return False when the next position is already taken by another rover
    def test_next_position_is_already_occupied(self):
        nextPosition = self.position
        self.assertFalse(self.controller.check_position_available(position=nextPosition, occupiedPositions=self.occupiedPositions, topSquare=self.topSquare))

    # Check that check_position_available return False when the next position is outside of the grid
    def test_next_position_is_outside(self):
        nextPosition = Position(7, 1)
        self.assertFalse(self.controller.check_position_available(position=nextPosition, occupiedPositions=self.occupiedPositions, topSquare=self.topSquare))
