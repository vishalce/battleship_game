from battleship import constants
from battleship.observer import Subject


class Ship(Subject):

    def __init__(self, name, size):
        super(Ship, self).__init__()
        self.name = name
        self.size = size
        self.position_occupied = []
        self.position_fired = []
        self.state = 0

    def is_position_occupied(self, position):
        return position in self.position_occupied

    def attack_on_position(self, position):
        if self.is_position_occupied(position):
            self.position_occupied.remove(position)
            self.position_fired.append(position)

            if not self.position_occupied and self.position_fired == self.size:
                self.state = constants.SHIP_DESTROYED
            else:
                self.state = constants.SHIP_ATTAKED

            return True
        return False


class BattleShip(Ship):
    def __init__(self, name):
        super(BattleShip, self).__init__(name=name, size=constants.SHIP_SIZE_BATTLESHIP)


class Carrier(Ship):
    def __init__(self, name):
        super(Carrier, self).__init__(name=name, size=constants.SHIP_SIZE_CARRIER)


class Cruiser(Ship):
    def __init__(self, name):
        super(Cruiser, self).__init__(name=name, size=constants.SHIP_SIZE_CRUISER)


class Destroyer(Ship):
    def __init__(self, name):
        super(Destroyer, self).__init__(name=name, size=constants.SHIP_SIZE_DESTROYER)


class Submarine(Ship):
    def __init__(self, name):
        super(Submarine, self).__init__(name=name, size=constants.SHIP_SIZE_SUBMARINE)
