from collections import defaultdict

class BattleshipStateTracker:

    # Create a board
    # Note: assume height and width are integers
    # height    height of board
    # width     height of board
    def __init__(self, height=10, width=10):
        if height <= 1 or width <= 1:
            raise ValueError('Height and width must be positive!')
        self.height       = height
        self.width        = width
        self.board        = defaultdict(lambda: [0, False]) # ship no. and hit status; 0 means no ship
        self.ship_count   = 0 # no. of ship left
        self.ship_section = defaultdict(int) # no. of undamaged sections for each ship

    # Add a battleship to the board
    # Note: assume x_start, y_start and n are integers, and orientation is a string
    # x_start       x position of the ship head
    # y_start       y position of the ship head
    # orientation   orientation of the ship ('h': horizontal, 'v': vertical)
    # n             length of the ship
    def add_battleship(self, x_start, y_start, orientation, n):
        if not 0 <= x_start < self.width or not 0 <= y_start < self.height:
            raise ValueError('Invalid coordinate!')
        if n < 1:
            raise ValueError('Invalid ship length!')
        x_stop, y_stop = x_start + 1, y_start + 1
        if orientation == 'h':
            x_stop = x_start + n
            if x_stop > self.width:
                raise ValueError('Invalid coordinate!')
        elif orientation == 'v':
            y_stop = y_start + n
            if y_stop > self.height:
                raise ValueError('Invalid coordinate!')
        else:
            raise ValueError('Invalid orientation!')
        
        coordinates = [(x, y) for x in range(x_start, x_stop) for y in range(y_start, y_stop)]
        if all(not self.board.get(coordinate) for coordinate in coordinates):
            self.ship_count += 1
            ship_no = self.ship_count
            self.ship_section[ship_no] = n
            for coordinate in coordinates:
                self.board[coordinate][0] = ship_no
        else:
            raise ValueError('Invalid coordinate!')

    # Take an attack at a given coordinate
    # Note: assume x and y are integers
    # x     x axis
    # y     y axis
    # return True if attack hit, False otherwise
    def take_attack(self, x, y):
        if not 0 <= x < self.width or not 0 <= y < self.height:
            raise ValueError('Invalid coordinate!')
        ship_no, status = self.board[(x, y)]
        if status == True:
            raise ValueError('You have already been attacked in this location!')
        self.board[(x, y)][1] = True
        if ship_no == 0:
            return False # attack miss
        else:
            self.ship_section[ship_no] -= 1
            if self.ship_section[ship_no] == 0:
               self.ship_count -= 1 
            return True # attack hit

    # Check if the player has lost the game
    # return 0 if the player has lost the game, >0 otherwise
    def get_status(self):
        return self.ship_count # 0: battle lost, else: otherwise
