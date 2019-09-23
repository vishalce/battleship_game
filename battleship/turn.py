from abc import ABC
from abc import abstractmethod

from battleship import searching, constants
from battleship.shoot import Shoot


class Turn(ABC):

    def __init__(self):
        self.shoot = None
        self.attacking_player = None
        self.attaked_player = None

    def set_players(self, attaking_player, attaked_player):
        self.attacking_player = attaking_player
        self.attaked_player = attaked_player

    def play_turn(self, position):
        self.shoot = self.create_shoot(position)
        self.validate_shoot(self.shoot)
        self.execute_shoot()
        self.save_turn()

    @abstractmethod
    def create_shoot(self, position):
        raise NotImplementedError(
            self.__class__.__name__ + ' is an abstract class!!! Use proper implementation!!!')

    def execute_shoot(self):
        self.shoot.state = constants.SHOOT_STATE_SUCCESSFUL \
            if self.attaked_player.get_board().execute_and_validate_shoot(self.shoot.position) \
            else constants.SHOOT_STATE_MISSED

    def validate_shoot(self, shoot):
        if not self.attaked_player.get_board().validate_shoot_position(shoot.position):
            raise Exception('You\'ve already fired at position or invalid position')

    def save_turn(self):
        self.attacking_player.games[self.attacking_player.current_game]['turns'].append(self)


class HumanTurn(Turn):

    def create_shoot(self, position):
        position_searching = searching.ConcreteSearching(position, self.attaked_player)
        shoot = Shoot(position_searching)
        shoot.search_position()
        return shoot


class ComputerTurn(Turn):

    def create_shoot(self, position):
        position_searching = None
        shoot = None
        valid_shoot = False
        flag = len(self.attacking_player.get_turns())

        while not valid_shoot:
            if flag > 0:
                previous_turn = self.attacking_player.get_previous_successful_turn()
                if previous_turn.shoot.state == constants.SHOOT_STATE_SUCCESSFUL:
                    position_searching = searching.NearbySearching(previous_turn.shoot.position, self.attaked_player)
                elif previous_turn.shoot.state == constants.SHOOT_STATE_MISSED:
                    position_searching = searching.RandomPositionSearching(None, self.attaked_player)
            else:
                position_searching = searching.RandomPositionSearching(None, self.attaked_player)

            shoot = Shoot(position_searching)
            shoot.search_position()

            if not shoot.position:
                flag = 0
            else:
                valid_shoot = True
        return shoot
