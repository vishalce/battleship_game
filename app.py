from battleship import constants
from battleship.game import Game
from battleship.player import Player
from battleship.position import Position

alphabets = [chr(x) for x in range(ord('a'), ord('k'))]

player1 = Player('Player1', constants.GAME_PLAYER_TYPE_HUMAN)
player2 = Player('Player2', constants.GAME_PLAYER_TYPE_HUMAN)
player3 = Player('Computer', constants.GAME_PLAYER_TYPE_COMPUTER)

games = [Game('game1', player1, player2), Game('game2', player1, player3)]

current_game = games[0]
current_game.play()

print('Playing {}'.format(current_game.name))

while True:

    if current_game.state == constants.GAME_STATE_FINISHED:
        print('GAME FINISHED')
        break

    print('\n' + current_game.attacking_player.name + ':')

    command = input().lower()
    if command == 'change game':
        print('Enter name of game:', end=' ')
        game_name = input().lower()
        current_game = current_game.attacking_player.get_game(game_name)
        current_game.play()
        print('\n Playing {}'.format(current_game.name))

    if command == 'exit':
        break

    elif command == 'draw_board':
        print('Current Status of Game: {}'.format(
            'FINISHED' if current_game.state == constants.GAME_STATE_FINISHED else 'PLAYING'))
        print('Board position of {}'.format(current_game.attacking_player.name))
        current_game.attacking_player.get_board().draw_current_board()
        print('\nBoard position of {}'.format(current_game.attacked_player.name))
        current_game.attacked_player.get_board().draw_current_board()

    elif command.startswith('fire '):
        try:
            fire_command = command.split()[1]
            x = alphabets.index(fire_command[0])
            y = int(fire_command[1]) - 1
            position = Position(x, y)
            # player attack
            current_game.attack(current_game.attacking_player, position)
            shoot = current_game.attacked_player.get_previous_turn().shoot
            print('SUCCESS' if shoot.state == 1 else 'MISSED')

            if current_game.attacking_player.name == constants.GAME_PLAYER_NAME_COMPUTER:
                player_index = 2
                # computer attack
                current_game.attack(current_game.attacking_player, position)
                shoot = current_game.attacked_player.get_previous_turn().shoot
                print('COMPUTER')
                print(shoot.position.x, shoot.position.y, 'SUCCESS' if shoot.state == 1 else 'MISSED')

        except Exception as ex:
            print(ex)
