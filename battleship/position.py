class Position:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, obj):
        if obj and isinstance(obj, Position) and obj.x == self.x and obj.y == self.y:
            return True
        return False
