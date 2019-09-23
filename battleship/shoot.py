class Shoot:
    def __init__(self, position_searching):
        self.position_searching = position_searching
        self.state = 0
        self.position = None

    def search_position(self):
        self.position = self.position_searching.search_position_to_attack()
