from model import Command
from model import DataErrorException
from model import Orientation
from model import Position
from model import Rover


class Controller:

    # Function which, given a set of instructions, is going to move all the rovers sequentially, one after another.
    def move_rovers(self, instructions):
        # First we check if the data are correct. If so, we created the list which will contain all the positions which will be occupied by the different rovers and get the top square position.
        cleanedInstructions = self.clean_data(instructions=instructions)
        # We create a list of rovers
        rovers = []
        occupiedPositions = []
        topSquare = cleanedInstructions[0]
        # We iterate through every rover information, getting the initial position and the commands
        for roverInformation in cleanedInstructions[1:]:
            rover = roverInformation[0]
            commands = roverInformation[1]
            # For each command, we check if we need to move or rotate the rover
            for command in commands:
                # If it is a move, we need to calculate the next position and check if this position is still available (not occupied by another rover or outside of the grid)
                # If the next position is not available, the rover stays at its position with the same orientation.
                if command == Command.MOVE:
                    nextPosition = self.calculate_next_position(rover=rover)
                    if self.check_position_available(position=nextPosition, occupiedPositions=occupiedPositions, topSquare=topSquare):
                        rover.position = nextPosition
                # Otherwise, we rotate the rover - we know already that it could only be a rotation at this point since we have checked the correctiveness of the file -.
                else:
                    self.rotate_rover(rover=rover, command=command)
            # When the rover has reached its final position, we add it into our list containing all occupied positions
            occupiedPositions.append(rover.position)
            # We add the rover to the rovers list
            rovers.append(rover)
        return rovers

    # Function which check and clean the instructions
    def clean_data(self, instructions):
        # We check that the file contains at least 3 lines, otherwise it means that it is incomplete
        if len(instructions) < 2:
            raise DataErrorException(message='File in incomplete')
        # We create a list which will contain the top right position as the first element, and then each other elements will a list of 2 elements: the initial position and orientation of each rover
        cleanedInstructions = []
        topSquareData = instructions[0].strip().split(' ')
        # We check that the first line is composed of 2 positive integers separated by a space. If so, we create the top square position and save it in the cleaned instructions list.
        if len(topSquareData) == 2 and topSquareData[0].isdigit() and topSquareData[1].isdigit():
            topSquare = Position(int(topSquareData[0]), int(topSquareData[1]))
            cleanedInstructions.append(topSquare)
            # We look for every two lines, which correspond to each rover initial position and commands.
            # For the first line, we check that the initial position is composed of 2 positive integers and a letter among N, E, S or W, separated by a space.
            # If so, we create a Rover containing its original position and orientation
            for lineNumber in range(1, len(instructions), 2):
                roverData = instructions[lineNumber].strip().split(' ')
                if len(roverData) == 3 and roverData[0].isdigit() and roverData[1].isdigit() and roverData[2] in Orientation.ALL:
                    rover = Rover(Position(int(roverData[0]), int(roverData[1])), roverData[2])
                    # For the second line, we check that the string is composed only of L, M or R.
                    # If so, we save a list containing the initial position of the rover and its commands to be executed.
                    try:
                        commands = instructions[lineNumber + 1].strip()
                    except:
                        raise DataErrorException(message='There is no command for this rover')
                    if set(commands).issubset(Command.ALL):
                        cleanedInstructions.append([rover, commands])
                    else:
                        # We raise an error specifying that there is a mistake in the commands
                        raise DataErrorException(message=f'Rover n°{int((lineNumber + 1) / 2)} commands contain error, please correct it in the file to proceed')
                else:
                    # We raise an error specifying that there is a mistake in the position
                    raise DataErrorException(message=f'Rover n°{int((lineNumber + 1) / 2)} initial position contains error, please correct it in the file to proceed')
            # We return the cleaned instructions list.
            return cleanedInstructions
        # We raise an error specifying that there is a mistake in the top right position
        raise DataErrorException(message='The upper-right coordinates of the plateau contain error, please correct the file to proceed')

    # Function which rotates a rover
    def rotate_rover(self, rover, command):
        # We take the actual rover's orientation and we check the position of it in the list [N, E, S, W]
        orientation = rover.orientation
        orientationPosition = Orientation.ALL.index(orientation)
        # Since going to the right means going to the next position in the list and going to the left means going to the previous position of the list, we add or substract one to the current index.
        if command == Command.RIGHT:
            orientationPosition += 1
        else:
            orientationPosition -= 1
        # We make sure that we don't go out of the list by taking the modulo of the length of the list (here: 4)
        newOrientation = Orientation.ALL[orientationPosition % 4]
        # We update the new orientation in the rover and we return it
        rover.orientation = newOrientation
        return rover

    # Function which determines the next position of the rover
    def calculate_next_position(self, rover):
        # By knowing the current position and orientation of the rover, we increase or decrease of 1 the abcissa or the ordinate of the position, depending of the orientation and we return the new position.
        initialPosition = rover.position
        orientation = rover.orientation
        if orientation == Orientation.NORTH:
            nextPosition = Position(initialPosition.abscissa, initialPosition.ordinate + 1)
        elif orientation == Orientation.EAST:
            nextPosition = Position(initialPosition.abscissa + 1, initialPosition.ordinate)
        elif orientation == Orientation.SOUTH:
            nextPosition = Position(initialPosition.abscissa, initialPosition.ordinate - 1)
        elif orientation == Orientation.WEST:
            nextPosition = Position(initialPosition.abscissa - 1, initialPosition.ordinate)
        return nextPosition

    # Function which checks if the rover can move the next position.
    def check_position_available(self, position, occupiedPositions, topSquare):
        # We check first that the position is not occupied by another rover otherwise we print a message specifying this particular statement.
        if position not in occupiedPositions:
            # We check that the position is not outside of the grid otherwise we print a message specifying this particular statement.
            if 0 <= position.abscissa <= topSquare.abscissa and 0 <= position.ordinate <= topSquare.ordinate:
                # If these two checks pass, we return True otherwise False.
                return True
            else:
                print(f'The rover is trying to go at position ({position.abscissa},{position.ordinate}) which is outside of the grid delimited by (0,0) x ({topSquare.abscissa},{topSquare.ordinate})')
        else:
            print(f'A rover is already in position {position}')
        return False
