import pygame as pg


class Vector:
    def __init__(self, x=0.0, y=0.0):
        self.x = x
        self.y = y

    def __repr__(self):
        return "Vector({}, {})".format(self.x, self.y)

    def __add__(self, other):
        temp = Vector()
        temp.x = self.x
        temp.y = self.y
        temp.x += other.x
        temp.y += other.y
        return temp

    def __sub__(self, other):
        temp = Vector()
        temp.x = self.x
        temp.y = self.y
        temp.x -= other.x
        temp.y -= other.y
        return temp

    def __rmul__(self, k: float):
        temp = Vector()
        temp.x = self.x
        temp.y = self.y
        temp.x *= k
        temp.y *= k
        return temp

    def __mul__(self, k: float):
        return self.__rmul__(k)

    def __truediv__(self, k: float):
        return self.__mul__(1.0 / k)

    def __neg__(self):
        return self.__mul__(-1.0)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    @staticmethod
    def test():  # feel free to change the test code
        v = Vector(x=5, y=5)
        u = Vector(x=4, y=4)
        print('v is {}'.format(v))
        print('u is {}'.format(u))
        print('u plus v is {}'.format(u + v))
        print('u minus v is {}'.format(u - v))
        print('k = 3 times u is {}'.format(3 * u))
        print('u times k = 3 is {}'.format(u * 3))
        print('negative u is {}'.format(-u))
        print('u divided by k = 3 is {}'.format(u/3))


class Laser(pg.sprite.Sprite):
    # this is included so that ship makes more sense, and because I mostly remember it
    def __init__(self, width, height, color, ship, velocity, image=None):
        super().__init__()
        self.width = width
        self.height = height
        self.color = color
        self.velocity = velocity
        self.ship = ship
        if image:
            self.image = image
            self.rect = self.image.get_rect()
        else:
            self.rect = (self.width, self.height, 0, 0)
        self.rect.midbottom = self.ship.midtop

    def move(self):
        self.rect.y += self.velocity.y
        # if two dimensional lasers
        self.rect.x += self.velocity.x
        # limiting to screen logic could be placed here, or handled by Ship or Game class

    def draw(self):
        if not image:
            pg.draw.Rect(self.ship.screen, self.color, self.rect)
        else:
            self.ship.screen.blit(self.image, self.rect)

    def update(self):
        self.move()
        self.draw()


class Game:
    # this is included to make ship make more sense, though only relevant member variables to ship
    # are included specifically
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((1200, 800))
        self.ship = Ship(self)
        # Key Press Loop
        # Event loop
        #   Update members
        #   pg.display.update()


class Ship(pg.sprite.Sprite):
    def __init__(self, game, velocity=Vector()):
        super().__init__()
        self.game = game
        self.screen = self.game.screen
        self.image = pg.image.load('someshipimage.png')
        self.rect = self.image.get_rect()
        self.rect.midbottom = self.screen.get_rect().midbottom
        self.velocity = velocity
        self.lasers = pg.sprite.Group()

    def __repr__(self):
        return 'Ship located at ({}, {}), with a velocity of {}'.format(self.rect.left, self.rect.top, self.velocity)

    def center_ship(self):
        self.rect.midbottom = self.screen.get_rect().midbottom

    def fire(self):
        templaser = Laser(ship=self, width=5, height=5, color=(255, 0, 0), velocity=Vector(0, -5), image=False)
        self.lasers.add(templaser)

    def remove_lasers(self, particularlaser=False):
        if particularlaser:
            self.lasers.remove(particularlaser)
        else:
            self.lasers.remove()

    def move(self):
        self.rect.x += self.velocity.x
        # if two dimensional ship movement
        self.rect.y += self.velocity.y
        # limiting to screen logic could be placed here, but I think the game would be better at coordinating that

    def draw(self):
        self.screen.blit(self.image, self.rect)

    def update(self):
        self.move()
        self.draw()


def main():
    Vector.test()
    

if __name__ == "__main__":
    main()
