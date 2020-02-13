import click

from internal import Controller


# Function which reads and proceeds the different instructions of a given file
# TO RUN IT, EXAMPLE: python mars_rover.py 'examples/example1.txt'
@click.command()
@click.argument('document', type=str)
def run(document):
    controller = Controller()
    # We read the file and call the move rovers function of the Controller class
    with open(document, "r") as f:
        instructions = f.readlines()
        rovers = controller.move_rovers(instructions=instructions)
        # We print the different rovers
        for rover in rovers:
            print(rover)

if __name__ == '__main__':
    run()
