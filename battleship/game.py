from battleship import constants
from battleship.board import Board
from battleship.factories import TurnFactory
from battleship.observer import Observer


class Game(Observer):

    def __init__(self, name, player1, player2):
        self.name = name
        self.players = []
        self.state = constants.GAME_STATE_PLAYING
        board1 = Board()
        board2 = Board()
        player1.attach_game(name, self, board1)
        player2.attach_game(name, self, board2)
        self.players.append(player1)
        self.players.append(player2)
        self.attacking_player = self.players[0]
        self.attacked_player = self.players[1]
        board1.attach(self)
        board2.attach(self)

    def play(self):
        for player in self.players:
            player.change_current_game(self.name)

    def attack(self, player, position):
        self.validate_game_status()
        self.validate_players_turn(player)
        self.play_attack(player, position)
        self.swap_players()

    def validate_game_status(self):
        if self.state == constants.GAME_STATE_FINISHED:
            raise Exception('Game has been finished')

    def validate_players_turn(self, player):
        if player == self.attacked_player:
            raise Exception('Invalid turn for {}'.format(player.name))

    def play_attack(self, player, position):
        turn = TurnFactory.create_turn(player)
        turn.set_players(self.attacking_player, self.attacked_player)
        turn.play_turn(position)

    def swap_players(self):
        if self.attacking_player == self.players[0]:
            self.attacking_player, self.attacked_player = self.players[1], self.players[0]
        else:
            self.attacking_player, self.attacked_player = self.players[0], self.players[1]

    def update(self, subject):
        if isinstance(subject, Board):
            if subject.ships_available == 0:
                self.state = constants.GAME_STATE_FINISHED
