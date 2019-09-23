import random

from battleship import constants
from battleship.factories import ShipFactory
from battleship.observer import Observer
from battleship.observer import Subject
from battleship.position import Position
from battleship.ship import Ship


class Board(Subject, Observer):

    def __init__(self):
        super(Board, self).__init__()
        self.ships = []
        self.positions = []
        self.positions_visited = []
        self.ships_available = 0
        self.draw_board()
        self.create_ships()
        self.put_ships_in_board()

    def draw_board(self):
        for x in range(0, constants.BOARD_WIDTH):
            for y in range(0, constants.BOARD_HEIGHT):
                self.positions.append(Position(x, y))

    def create_ships(self):
        self.ships.append(ShipFactory.create_ship(constants.SHIP_BATTLESHIP))
        self.ships.append(ShipFactory.create_ship(constants.SHIP_DESTROYER))
        self.ships.append(ShipFactory.create_ship(constants.SHIP_CRUISER))
        self.ships.append(ShipFactory.create_ship(constants.SHIP_CARRIER))
        self.ships.append(ShipFactory.create_ship(constants.SHIP_SUBMARINE))

        for ship in self.ships:
            ship.attach(self)
        self.ships_available = len(self.ships)

    def put_ships_in_board(self):
        positions_occupied = []

        for ship in self.ships:

            allocated = False
            possible_positions = []

            while not allocated:
                random_position = random.randint(0, 1)
                x = random.randint(0, constants.BOARD_WIDTH)
                y = random.randint(0, constants.BOARD_HEIGHT)

                for i in range(ship.size):
                    position = None
                    if random_position == constants.BOARD_DIRECTION_HORIZONTAL:
                        position = Position(x + i, y)
                    elif random_position == constants.BOARD_DIRECTION_VERTICAL:
                        position = Position(x, y + i)

                    if position in self.positions and position not in positions_occupied:
                        possible_positions.append(position)
                        allocated = True
                    else:
                        possible_positions = []
                        allocated = False
                positions_occupied.extend(possible_positions)
                ship.position_occupied = possible_positions

    def is_position_occupied(self, position):
        for ship in self.ships:
            if ship.is_position_occupied(position):
                return True
        return False

    def get_available_position(self):
        index = random.randint(0, len(self.positions))
        position = self.positions[index]
        return Position(position.x, position.y)

    def validate_position(self, position):
        return position in self.positions and position not in self.positions_visited

    def validate_shoot_position(self, position):
        if self.validate_position(position):
            self.positions.remove(position)
            self.positions_visited.append(position)
            return True
        return False

    def execute_and_validate_shoot(self, position):
        for ship in self.ships:
            if ship.attack_on_position(position):
                return True
        return False

    def update(self, subject):
        if isinstance(subject, Ship):
            if subject.state == constants.SHIP_DESTROYED:
                self.ships_available -= 1
            self.notify()

    def draw_current_board(self):
        row_index = self.get_next_row_index()
        for i in range(1, 11):
            print('   ' + str(i), end='')
        print()
        for x in range(0, constants.BOARD_WIDTH):
            print(next(row_index), end=' ')
            for y in range(0, constants.BOARD_HEIGHT):
                position = Position(x, y)
                position_char = '000' if position in self.positions else 'MMM'
                for ship in self.ships:
                    if position in ship.position_occupied:
                        position_char = ship.name[:3].upper()
                        break
                    elif position in ship.position_fired:
                        position_char = ship.name[:2].upper() + 'F'
                        break
                print(position_char, end=' ')
            print()

    def get_next_row_index(self):
        alphabets = [chr(x) for x in range(ord('A'), ord('K'))]
        for alphabet in alphabets:
            yield alphabet
