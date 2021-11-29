import pygame
from src.colors import *
from src.dimensions import *

class Field(pygame.sprite.Sprite):
    def __init__(self, row, column, field_type):
        super(Field, self).__init__()
        self.surf = pygame.Surface((WIDTH, HEIGHT))
        self.field_type = field_type
        if self.field_type == "soil":
            self.moveCost = 3
            self.surf.fill(BROWN0)
        elif self.field_type == "rocks":
            self.moveCost = 5
            self.surf.fill(LBROWN)
        elif self.field_type == "road":
            self.moveCost = 1
            self.surf.fill(GREY)
        elif self.field_type == "pond":
            self.moveCost = 1000
            self.surf.fill(BLUE)
        self.rect = self.surf.get_rect(
            topleft=((MARGIN + WIDTH) * row + MARGIN, (MARGIN + HEIGHT) * column + MARGIN))
        self.position = [row, column]
        self.hydration = 0
        self.planted = 0
        self.fertility = 0
        self.tractor_there = False

    def hydrate(self):
        if self.field_type == "soil" and self.hydration <= 5:
                self.hydration += 1
                if self.fertility == 1:
                    if self.hydration == 0:
                        self.surf.fill(REDDISH0)
                        self.fertility = 0
                    if self.hydration == 1:
                        self.surf.fill(REDDISH1)
                    if self.hydration == 2:
                        self.surf.fill(REDDISH2)
                    if self.hydration == 3:
                        self.surf.fill(REDDISH3)
                    if self.hydration == 4 or self.hydration == 5:
                        self.surf.fill(REDDISH4)
                else:
                    if self.hydration == 0:
                        self.surf.fill(BROWN0)
                    if self.hydration == 1:
                        self.surf.fill(BROWN1)
                    if self.hydration == 2:
                        self.surf.fill(BROWN2)
                    if self.hydration == 3:
                        self.surf.fill(BROWN3)
                    if self.hydration == 4 or self.hydration == 5:
                        self.surf.fill(BROWN4)
    
    def dehydrate(self):
            if self.field_type == "soil" and self.hydration > 0:
                self.hydration -= 1
                if self.fertility == 1:
                    if self.hydration == 0:
                        self.surf.fill(REDDISH0)
                        self.fertility = 0
                    if self.hydration == 1:
                        self.surf.fill(REDDISH1)
                    if self.hydration == 2:
                        self.surf.fill(REDDISH2)
                    if self.hydration == 3:
                        self.surf.fill(REDDISH3)
                    if self.hydration == 4 or self.hydration == 5:
                        self.surf.fill(REDDISH4)
                else:
                    if self.hydration == 0:
                        self.surf.fill(BROWN0)
                    if self.hydration == 1:
                        self.surf.fill(BROWN1)
                    if self.hydration == 2:
                        self.surf.fill(BROWN2)
                    if self.hydration == 3:
                        self.surf.fill(BROWN3)
                    if self.hydration == 4 or self.hydration == 5:
                        self.surf.fill(BROWN4)
    
    def free(self):
        self.planted = 0
