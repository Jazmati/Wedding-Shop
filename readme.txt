Hello,

This a short file which explains how to run the test. I tried to put many comments in the files to be explicit about what I am doing in the script.
First you need to install the requirements in requirements.txt file.
Then, you will need to run the command:
python mars_rover.py '{file path}', ex: python mars_rover.py 'examples/example1.txt'
I have put some example files in the examples folder.

This file is declined as followed:

- Examples folder contain some example files

- Internal folder contains a file which contains all the logic for moving and rotating the different rovers.
All of this logic is in a class named Controller.

- Model folder contains four files: one which contains all the constants, one which is a class to describe a position on the grid, one which is a class to describe a rover and one which contains the Exceptions

- Tests folder which contains the tests for the Controller class. All functions in this class are tested.
To run the tests: python -m unittest tests/test_controller.py

- mars_rover.py file which is the main file, which allows us to run the script.
The run function is first reading the file and call the move rovers function of the Controller class.
The move_rovers function is going to call the clean data function to check if there is any error in the file and get the data cleaned if there is no error.
From there, the move_rovers function is going to determine the grid and extract information from each rover (its initial position and the commands).
Then, for each command in each rover, the move_rovers function is going to recognise if it has to move or rotate the rover and call the specific function.
A checking for knowing if the position is available (inside the grid and not occupied by another rover) is done.
I have assumed that when a rover is trying to get to position which is not available, the rover remain at the same position with the same orientation and the next command is executed.
Once the rover reaches its final position, the move_rovers function is saving its position in a list which contains all positions which are occupied by the rovers, so that the next one won't collide with any of them.

I hope you will enjoy this test script
Kind regards,
Sami
