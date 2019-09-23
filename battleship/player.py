class Player():
    def __init__(self, name, type):
        self.name = name
        self.type = type
        self.games = {}
        self.current_game = None

    def attach_game(self, name, game, board):
        if name not in self.games.keys():
            self.games[name] = {
                'game': game,
                'turns': [],
                'board': board,
            }
        else:
            raise Exception('Player is already playing {}'.format(name))

    def get_game(self, game):
        if game in self.games:
            return self.games[game]['game']
        else:
            raise Exception('Player is not playing {}'.format(game))

    def get_current_game(self):
        return self.current_game

    def change_current_game(self, game):
        self.current_game = game

    def get_board(self):
        return self.games[self.current_game]['board']

    def get_turns(self):
        return self.games[self.current_game]['turns']

    def get_previous_turn(self):
        return self.games[self.current_game]['turns'][-1]

    def get_previous_successful_turn(self):
        turn = None

        control_steps_back = 0
        for i in range(len(self.games[self.current_game]['turns']) - 1, -1, -1):
            control_steps_back += 1
            turn = self.games[self.current_game]['turns'][i]

        return turn
