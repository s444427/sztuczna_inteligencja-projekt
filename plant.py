import os
import random

from AI.decision_tree import *
from src.dimensions import *
from src.sprites import *
from src.colors import *

path = os.path.dirname(__file__) + "\\src\\test\\"

class Plant(pygame.sprite.Sprite):
    def __init__(self, field, species):
        self.species = species
        if self.species == "tomato":
            self.img0 = wheat_img_0
            self.img1 = wheat_img_1
            self.img2 = wheat_img_2
            self.img3 = wheat_img_3
        elif self.species == "potato":
            self.img0 = potato_img_0
            self.img1 = potato_img_1
            self.img2 = potato_img_2
            self.img3 = potato_img_3
        elif self.species == "strawberry":
            self.img0 = strawberry_img_0
            self.img1 = strawberry_img_1
            self.img2 = strawberry_img_2
            self.img3 = strawberry_img_3
        elif self.species == "pepper":
            self.img0 = strawberry_img_0
            self.img1 = strawberry_img_1
            self.img2 = strawberry_img_2
            self.img3 = strawberry_img_3
        self.surf = self.img0
        self.position = field.position
        self.field = field
        self.rect = self.surf.get_rect(
            topleft=((MARGIN + WIDTH) * self.position[0] + MARGIN, (MARGIN + HEIGHT) * self.position[1] + MARGIN))
        self.growth = 0
        self.is_healthy = True
        field.planted = True
        self.tickscount = 0
        self.ticks = 0
        self.path = path + self.species + "\\"
        self.testimage = self.path + random.choice(os.listdir(self.path))

    def dtree(self):
        if self.field.hydration == 4:
            if self.is_healthy == 1:
                if self.field.tractor_there == 0:
                    if self.ticks == 0:
                        return 0
                    elif self.ticks == 1:
                        return 1
                elif self.field.tractor_there == 1:
                    return 0
            elif self.is_healthy == 0:
                return 0
        elif self.field.hydration == 2:
            if self.species == "pepper":
                if self.ticks == 1:
                    if self.is_healthy == 1:
                        return 1
                    elif self.is_healthy == 0:
                        return 0
                elif self.ticks == 0:
                    return 0
            elif self.species == "potato":
                return 0
            elif self.species == "tomato":
                return 0
            elif self.species == "strawberry":
                return 0
        elif self.field.hydration == 1:
            if self.species == "potato":
                return 0
            elif self.species == "strawberry":
                if self.ticks == 1:
                    return -1
                elif self.ticks == 0:
                    return 0
            elif self.species == "tomato":
                return 0
            elif self.species == "pepper":
                if self.is_healthy == 0:
                    return 0
                elif self.is_healthy == 1:
                    if self.field.tractor_there == 0:
                        if self.ticks == 0:
                            return 0
                        elif self.ticks == 1:
                            return 1
                    elif self.field.tractor_there == 1:
                        return 0
        elif self.field.hydration == 3:
            if self.ticks == 1:
                if self.field.tractor_there == 0:
                    if self.is_healthy == 1:
                        if self.species == "potato":
                            if self.field.fertility == 1:
                                return 1
                            elif self.field.fertility == 0:
                                return 0
                        elif self.species == "strawberry":
                            return 1
                        elif self.species == "pepper":
                            return 1
                        elif self.species == "tomato":
                            return 1
                    elif self.is_healthy == 0:
                        return 0
                elif self.field.tractor_there == 1:
                    return 0
            elif self.ticks == 0:
                return 0
        elif self.field.hydration == 5:
            if self.field.tractor_there == 1:
                return 0
            elif self.field.tractor_there == 0:
                if self.is_healthy == 0:
                    return 0
                elif self.is_healthy == 1:
                    if self.ticks == 1:
                        return 1
                    elif self.ticks == 0:
                        return 0
        elif self.field.hydration == 0:
            if self.ticks == 0:
                return 0
            elif self.ticks == 1:
                return -1

    def update(self):
        if self.growth == 0:
            self.surf = self.img0
        if self.growth == 1:
            self.surf = self.img1
        if self.growth == 2:
            self.surf = self.img2
        if self.growth == 3:
            self.surf = self.img3

    def grow(self):
        if self.dtree() == 1:
            self.growth += 1
            self.ticks = 0
        elif self.dtree() == -1:
            self.growth -= 1
            self.ticks = 0
        if self.growth > 4:
            self.growth = 4
        if self.growth < 0:
            self.growth = 0

        self.update()

    def tick(self):
        self.tickscount += 1
        if self.tickscount >= 25:
            self.tickscount = 0
            self.ticks = 1

    def remove(self):
        self.field.planted = False
