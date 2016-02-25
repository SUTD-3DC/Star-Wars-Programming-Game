import pygame

class Hole:

    def __init__(self, display, coord=None):
        self.coord = coord
        self.display = display
        self.surface = pygame.Surface((30, 30), 0, display)
        self.surface.fill((0, 0, 0))
        self.make_colliders()

    def make_colliders(self):
        self.psuedo_holes = {}
        self.psuedo_holes['right'] = pygame.Rect(self.coord[0] - 30,
                                                self.coord[1],
                                                30, 30)
        self.psuedo_holes['left'] = pygame.Rect(self.coord[0] + 30,
                                                self.coord[1],
                                                30, 30)
        self.psuedo_holes['down'] = pygame.Rect(self.coord[0],
                                                self.coord[1] - 30,
                                                30, 30)
        self.psuedo_holes['up'] = pygame.Rect(self.coord[0],
                                           self.coord[1] + 30,
                                           30, 30)

    def collides(self, player_rect):
        for direction in self.psuedo_holes:
            print "pseudo hole direction:", direction,
            print self.psuedo_holes[direction]
            if self.psuedo_holes[direction].colliderect(player_rect):
                return direction
        return None

    def draw(self):
        self.display.blit(self.surface, self.coord)
