# Import the pygame module
import pygame
# Import pygame.locals for easier access to key coordinates
from pygame.locals import (
    K_UP,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT
)


# Import other files from project
import field as F
import node as N
import plant as P
import src.colors as C
import src.dimensions as D
import AI.GeneticAlgorithm as ga
import AI.neural_network as nn
import tractor as T
from src import mapschema as maps

if __name__ == "__main__":
    # Initialize pygame
    pygame.init()

    # Name the window
    pygame.display.set_caption("Inteligentny Traktor")

    # Create the screen object
    # The size is determined by the constant SCREEN_WIDTH and SCREEN_HEIGHT
    screen = pygame.display.set_mode((D.SCREEN_WIDTH, D.SCREEN_HEIGHT))

    # Define the map of the field
    mapschema = maps.createField()

    # Create field array
    field = []

    # Populate the field array
    for row in range(D.GSIZE):
        field.append([])
        for column in range(D.GSIZE):
            fieldbit = F.Field(row, column, mapschema[column][row])
            field[row].append(fieldbit)

    # genetic_algorithm_setup(field)
    num_of_plants = 0
    plant_pops = []
    best_plant_pop = []

    goal_gen = 100
    best_plant_pop, plant_pops, num_of_plants, fitness = ga.genetic_algorithm_setup(field, plant_pops, goal_gen)

    net = nn.Net()
    nn.load_network_from_structure(net)
    net.eval()

    # Create Tractor object
    tractor = T.Tractor(field, [0, 0])

    # Define the map of plants
    mapschema = maps.createPlants()

    # Create plants array
    plants = []

    # Populate the plants array
    for row in range(D.GSIZE):
        plants.append([])
        for column in range(D.GSIZE):
            if best_plant_pop[column][row] != "":
                plantbit = P.Plant(field[row][column], best_plant_pop[column][row])
                plants[row].append(plantbit)
            else:
                plants[row].append(0)

    # Create list for tractor instructions
    path = []

    # Variable to keep the main loop running
    RUNNING = True

    # Variable conroling timed eventes
    TICKER = 0

    # Initialize clock
    clock = pygame.time.Clock()

    # Main loop
    while RUNNING:

        for event in pygame.event.get():
            # Did the user hit a key?
            if event.type == KEYDOWN:
                # Was it the Escape key? If so, stop the loop.
                if event.key == K_ESCAPE:
                    RUNNING = False
            # Did the user click the window close button? If so, stop the loop.
            elif event.type == QUIT:
                RUNNING = False

        # Create key Node that will be used to calculate tractor instructions
        processor = N.Node(field, tractor.position, tractor.direction)

        # If path is empty or nonexistent, create new one
        if path is None or len(path) == 0:
            path = processor.findPathToPlant()

        # control tractor by poping instructions from path list
        if path is not None:
            if path[0] == "move":
                tractor.move()
            elif path[0] == "left":
                tractor.rotate_left()
            elif path[0] == "right":
                tractor.rotate_right()
            elif path[0] == "hydrate":
                tractor.hydrate(field)
            elif path[0] == "fertilize":
                if plants[tractor.position[1]][tractor.position[0]]:
                    tractor.fertilize(field, plants, nn.result_from_network(net, plants[tractor.position[0]][tractor.position[1]].testimage))
            path.pop(0)


        # Set the screen background
        screen.fill(C.DBROWN)

        # Draw the field
        for row in range(D.GSIZE):
            for column in range(D.GSIZE):
                screen.blit(field[row][column].surf, field[row][column].rect)

        # Draw the tactor
        screen.blit(tractor.surf, tractor.rect)

        # Plants grow with every 10th tick, then they are drawn
        for row in plants:
            for plant in row:
                if plant != 0:
                    plant.tick()
                    plant.grow()
                    screen.blit(plant.surf, plant.rect)

        # Field are drying with every 100th tick
        if TICKER == 0:
            for row in range(D.GSIZE):
                for column in range(D.GSIZE):
                    field[row][column].dehydrate()

        # Increment ticker
        TICKER = (TICKER + 1) % 100

        # Update the screen
        pygame.display.flip()

        # Ensure program maintains a stable framerate
        clock.tick(35)
