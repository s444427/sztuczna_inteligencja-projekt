from src.dimensions import *
from src.sprites import *
from plant import *


class Tractor(pygame.sprite.Sprite):
    def __init__(self, field, position):
        super(Tractor, self).__init__()
        self.surf = pygame.Surface((WIDTH, HEIGHT))
        self.surf = tractor_img_0
        self.position = position
        self.field = field
        self.rect = self.surf.get_rect(
            topleft=((MARGIN + WIDTH) * self.position[0] + MARGIN, (MARGIN + HEIGHT) * self.position[1] + MARGIN))
        self.direction = [1, 0]
        self.field[self.position[0]][self.position[1]].tractor_there = True

    def move(self):
        self.field[self.position[0]][self.position[1]].tractor_there = False
        self.rect.move_ip(self.direction[0] * (WIDTH + MARGIN), self.direction[1] * (HEIGHT + MARGIN))
        self.position[0] += self.direction[0]
        self.position[1] += self.direction[1]
        if self.position[0] >= GSIZE:
            self.position[0] = GSIZE - 1
        if self.position[1] >= GSIZE:
            self.position[1] = GSIZE - 1
        if self.position[0] < 0:
            self.position[0] = 0
        if self.position[1] < 0:
            self.position[1] = 0

        if self.rect.top <= MARGIN:
            self.rect.top = MARGIN
        if self.rect.bottom >= SCREEN_HEIGHT - MARGIN:
            self.rect.bottom = SCREEN_HEIGHT - MARGIN
        if self.rect.left < MARGIN:
            self.rect.left = MARGIN
        if self.rect.right > SCREEN_WIDTH - MARGIN:
            self.rect.right = SCREEN_WIDTH - MARGIN

        self.field[self.position[0]][self.position[1]].tractor_there = True

    def rotate_right(self):
        if self.direction == [1, 0]:
            self.direction = [0, 1]
            self.surf = tractor_img_2
        elif self.direction == [0, 1]:
            self.direction = [-1, 0]
            self.surf = tractor_img_1
        elif self.direction == [-1, 0]:
            self.direction = [0, -1]
            self.surf = tractor_img_3
        elif self.direction == [0, -1]:
            self.direction = [1, 0]
            self.surf = tractor_img_0

    def rotate_left(self):
        if self.direction == [1, 0]:
            self.direction = [0, -1]
            self.surf = tractor_img_3
        elif self.direction == [0, -1]:
            self.direction = [-1, 0]
            self.surf = tractor_img_1
        elif self.direction == [-1, 0]:
            self.direction = [0, 1]
            self.surf = tractor_img_2
        elif self.direction == [0, 1]:
            self.direction = [1, 0]
            self.surf = tractor_img_0

    def hydrate(self, field):
        field[self.position[0]][self.position[1]].hydrate()

    def cut(self, field, pressed_keys):
        field[self.position[0]][self.position[1]].free()

    def plant(self, plant_map, plants):
        print(plant_map[self.position[0]][self.position[1]])
        plant = Plant(self.field[self.position[0]][self.position[1]], plant_map[self.position[0]][self.position[1]])
        plants.append(plant)

    def fertilize(self, field, plants, type):
        if plants[self.position[0]][self.position[1]].species == type:
            field[self.position[0]][self.position[1]].fertility = 1