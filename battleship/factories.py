from battleship import ship, constants
from battleship import turn


class ShipFactory:
    def __init__(self):
        pass

    @staticmethod
    def create_ship(name):
        if name == constants.SHIP_CRUISER:
            return ship.Cruiser(name)
        elif name == constants.SHIP_BATTLESHIP:
            return ship.BattleShip(name)
        elif name == constants.SHIP_CARRIER:
            return ship.Carrier(name)
        elif name == constants.SHIP_DESTROYER:
            return ship.Destroyer(name)
        elif name == constants.SHIP_SUBMARINE:
            return ship.Submarine(name)


class TurnFactory:
    @staticmethod
    def create_turn(player):
        if player.type == constants.GAME_PLAYER_TYPE_HUMAN:
            return turn.HumanTurn()
        else:
            return turn.ComputerTurn()
