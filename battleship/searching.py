import abc
import random

from battleship.position import Position


class PositionSearching(metaclass=abc.ABCMeta):

    def __init__(self, position, player):
        self.position = position
        self.player = player

    @abc.abstractmethod
    def search_position_to_attack(self):
        raise NotImplementedError(
            self.__class__.__name__ + ' is an abstract class!!! Use proper implementation!!!')


class ConcreteSearching(PositionSearching):
    def __init__(self, position, player):
        super(ConcreteSearching, self).__init__(position, player)

    def search_position_to_attack(self):
        return Position(self.position.x, self.position.y)


class RandomPositionSearching(PositionSearching):
    def __init__(self, position, player):
        super(RandomPositionSearching, self).__init__(position, player)

    def search_position_to_attack(self):
        return self.player.get_board().get_available_position()


class NearbySearching(PositionSearching):
    def __init__(self, game, position, player):
        super(NearbySearching, self).__init__(game, position, player)

    def search_position_to_attack(self):
        temp_positions = []
        possible_positions = []

        temp_positions.append(Position(self.position.x + 1, self.position.y))
        temp_positions.append(Position(self.position.x - 1, self.position.y))
        temp_positions.append(Position(self.position.x, self.position.y + 1))
        temp_positions.append(Position(self.position.x, self.position.y - 1))

        for possible_position in temp_positions:
            if self.player.get_board().validate_position(possible_position):
                possible_positions.append(possible_position)

        if possible_positions:
            return possible_positions[random.randint(0, len(possible_positions))]
