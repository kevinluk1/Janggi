# Author: Kevin Luk
# Date: 3/3/2021
# Description: This is the game of Janggi, one of the ancient precursors to Chess.

class Piece:
    """Super-class for each possible game piece. This is the blueprint for every piece in the game,
    and is used when setting the board."""

    def __init__(self, color):
        """Initializes a Piece object. The color parameter determines what player the piece belongs to"""
        self._color = color
        self._type = None

    def get_piece_color(self):
        """Returns the color of the piece at a given location"""
        return self._color

    def get_piece_type(self):
        """Returns the type of piece"""
        return self._type


class Soldier(Piece):
    """Subclass of Piece. Represents the soldier piece"""

    def __init__(self, color):
        """Initializes soldier piece """
        super().__init__(color)
        self._type = "Soldier"

    def __repr__(self):
        """Defines string representation for this class"""
        return "S" + self._color[0]


class General(Piece):
    """Subclass of piece. Represents the general piece"""

    def __init__(self, color):
        """Initializes general piece """
        super().__init__(color)
        self._type = "General"

    def __repr__(self):
        """Defines string representation for this class"""
        return "G" + self._color[0]


class Cannon(Piece):
    """Subclass of piece. Represents the cannon piece"""

    def __init__(self, color):
        """Initializes cannon piece"""
        super().__init__(color)
        self._type = "Cannon"

    def __repr__(self):
        """Defines string representation for this class"""
        return "C" + self._color[0]


class Guard(Piece):
    """Subclass of piece. Represents the guard piece"""

    def __init__(self, color):
        """Initializes guard piece"""
        super().__init__(color)
        self._type = "Guard"

    def __repr__(self):
        """Defines string representation for this class"""
        return "Q" + self._color[0]


class Horse(Piece):
    """Subclass of piece. Represents the horse piece"""

    def __init__(self, color):
        """Initializes horse piece"""
        super().__init__(color)
        self._type = "Horse"

    def __repr__(self):
        """Defines string representation for this class"""
        return "H" + self._color[0]


class Elephant(Piece):
    """Subclass of piece. Represents the elephant piece"""

    def __init__(self, color):
        """Initializes elephant piece"""
        super().__init__(color)
        self._type = "Elephant"

    def __repr__(self):
        """Defines string representation for this class"""
        return "E" + self._color[0]


class Chariot(Piece):
    """Subclass of piece. Represents the chariot piece"""

    def __init__(self, color):
        """Initializes chariot piece"""
        super().__init__(color)
        self._type = "Chariot"

    def __repr__(self):
        """Defines string representation for this class"""
        return "R" + self._color[0]


class JanggiGame:

    def __init__(self):
        """Creates an instance of Game, also calls set_board() to instantiate multiple piece objects (method calling
        a class) """
        self._board = [["" for _ in range(9)]  # Creates the game board
                       for _ in range(10)]

        self._translation_key = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7, "i": 8, "j": 9}
        self._translation_backwards = {0: "a", 1: "b", 2: "c", 3: "d", 4: "e", 5: "f", 6: "g", 7: "h", 8: "i", 9: "i"}
        self._possible_game_state = ["UNFINISHED", "RED_WON", "BLUE_WON"]
        self._game_state = self._possible_game_state[0]
        self._players = ["BLUE", "RED"]
        self._current_turn = self._players[0]
        self._turn_counter = 0
        self._red_is_in_check = False
        self._blue_is_in_check = False
        self.next_move_red = None
        self.next_move_blue = None

        self._game_state = self._possible_game_state[0]
        self.set_board()

    def is_in_check(self, color):
        """Returns whether a player's general is in check"""
        if color == 'red':
            if self._red_is_in_check:
                return True
            return False
        if color == "blue":
            if self._blue_is_in_check:
                return True
            return False

    def is_red_in_check_helper(self, pos2):
        """The purpose of this helper function is find the current position of red's general
        and then pass the position of red's general and the _NEXT_ position of the previous is_legal_move() call to is_legal_move() AGAIN.
        This essentially checks to see if a piece that was just moved threatens red's general and sets self._red_is_in_check to True if so."""
        for x in range(0, 4):
            for i in self._board[x]:
                if i != "" and i.get_piece_type() == "General":
                    column = self._board[x].index(i)
                    general_pos = (self._translation_backwards[column] + str(x + 1))

        from_coordinate = self.pos_to_coordinate(pos2)
        to_coordinate = self.pos_to_coordinate(general_pos)
        current_piece = self._board[from_coordinate[1]][
            from_coordinate[0]]
        next_location_or_piece = self._board[to_coordinate[1]][to_coordinate[0]]

        if self.is_legal_move(from_coordinate, current_piece, to_coordinate, next_location_or_piece) == True:
            if from_coordinate != to_coordinate and current_piece.get_piece_color() != next_location_or_piece.get_piece_color():
                self._red_is_in_check = True
                return True
            else:
                self._red_is_in_check = False
                return False

    def is_blue_in_check_helper(self, pos2):
        """This does the same thing as is_red_in_check_helper, except it checks the location of blue's general"""
        for list_number in range(7, 10):
            for list_element in self._board[list_number]:
                if list_element != "" and list_element.get_piece_type() == "General":
                    column = self._board[list_number].index(list_element)
                    general_pos = (self._translation_backwards[column] + str(list_number + 1))

        from_coordinate = self.pos_to_coordinate(pos2)
        to_coordinate = self.pos_to_coordinate(general_pos)
        current_piece = self._board[from_coordinate[1]][
            from_coordinate[0]]
        next_location_or_piece = self._board[to_coordinate[1]][to_coordinate[0]]

        if self.is_legal_move(from_coordinate, current_piece, to_coordinate, next_location_or_piece):

            if from_coordinate != to_coordinate and current_piece.get_piece_color() != next_location_or_piece.get_piece_color():
                self._blue_is_in_check = True
                return True
            else:
                self._blue_is_in_check = False
                return False

    def get_game_state(self):
        """Returns current game state"""
        return self._game_state

    def display_board(self):
        """Prints board"""
        for board in self._board:
            print(board)

    def set_board(self):
        """After the empty board is instantiated, this method creates a piece object for each player,
        and places it on the board"""

        # Soldiers
        for i in range(0, 9, 2):
            self._board[3][i] = Soldier("RED")
        for i in range(0, 9, 2):
            self._board[6][i] = Soldier("BLUE")

        # Generals
        self._board[1][4] = General("RED")
        self._board[8][4] = General("BLUE")

        # Cannons
        self._board[2][1] = Cannon("RED")
        self._board[2][7] = Cannon("RED")
        self._board[7][1] = Cannon("BLUE")
        self._board[7][7] = Cannon("BLUE")

        # Chariots
        self._board[0][8] = Chariot("RED")
        self._board[0][0] = Chariot("RED")
        self._board[9][8] = Chariot("BLUE")
        self._board[9][0] = Chariot("BLUE")
        # Guards
        self._board[9][3] = Guard("BLUE")
        self._board[9][5] = Guard("BLUE")
        self._board[0][3] = Guard("RED")
        self._board[0][5] = Guard("RED")
        # Horses
        self._board[0][7] = Horse("RED")
        self._board[0][2] = Horse("RED")
        self._board[9][7] = Horse("BLUE")
        self._board[9][2] = Horse("BLUE")
        # Elephants
        self._board[9][1] = Elephant("BLUE")
        self._board[9][6] = Elephant("BLUE")
        self._board[0][1] = Elephant("RED")
        self._board[0][6] = Elephant("RED")

    def switch_turn(self):
        """Switches player turn by using modulo operator and counter"""
        self._turn_counter += 1
        self._current_turn = self._players[self._turn_counter % len(self._players)]

    def pos_to_coordinate(self, pos: str):
        """Converts square position to coordinates"""
        return [self._translation_key[pos[0]], int(pos[1:]) - 1]

    def make_move(self, pos1, pos2):
        """Primary logic for moving pieces across the board. Calls is_legal_move() to determine if there are any obstructions, then moves the pieces."""
        from_coordinate = self.pos_to_coordinate(pos1)
        to_coordinate = self.pos_to_coordinate(pos2)
        current_piece = self._board[from_coordinate[1]][
            from_coordinate[0]]  # board is y,x
        next_location_or_piece = self._board[to_coordinate[1]][to_coordinate[0]]

        # print(from_coordinate, "to", to_coordinate)
        # print(current_piece, "to", next_location_or_piece)

        if self._game_state != self._possible_game_state[0]:
            return False

        if current_piece == "":  # Ensures beginning piece is actually a piece
            return False

        if current_piece.get_piece_color() != self._current_turn:  # Ensures player does not move outside his turn
            return False

        if from_coordinate == to_coordinate:  # If beginning position and ending position are the same, skip turn
            self.switch_turn()
            return True

        if not self.is_legal_move(from_coordinate, current_piece, to_coordinate,
                                  next_location_or_piece):  # Returns false if there are obstructions between starting position and end position
            # print("NOT A LEGAL MOVE")
            return False

        if self._board[to_coordinate[1]][to_coordinate[0]] != "":
            if self._board[to_coordinate[1]][to_coordinate[0]].get_piece_color() == self._board[from_coordinate[1]][
                from_coordinate[0]].get_piece_color():
                # print("CAN'T TAKE YOUR OWN PIECE")
                return False

        if self.is_legal_move(from_coordinate, current_piece, to_coordinate,
                              next_location_or_piece):  # Checks to see if a moves starting position and ending position are valid

            self._board[to_coordinate[1]][to_coordinate[0]] = self._board[from_coordinate[1]][
                from_coordinate[0]]  # Updates board with new piece positions
            self._board[from_coordinate[1]][from_coordinate[0]] = ""

            # The below logic checks to see if the move made by the player after being checked is valid.
            # Checks to see if a defending player's piece can block the check. Places a piece first to determine if that piece will block the check.
            # If it doesn't block the check, then revert the board update. There is definitely a better way to do this but i'm not smart enough to figure it out.

            if self._red_is_in_check != False:  # This cannot happen unless red is already in check
                if self.is_red_in_check_helper(self.next_move_red) == True:

                    # print("RED GENERAL NEEDS TO BE UNCHECKED")
                    self._board[from_coordinate[1]][from_coordinate[0]] = self._board[to_coordinate[1]][
                        to_coordinate[0]]
                    self._board[to_coordinate[1]][from_coordinate[0]] = ""

                    return False
                else:
                    self._red_is_in_check = False

            if self._blue_is_in_check != False:  # This cannot happen unless blue is already in check
                if self.is_blue_in_check_helper(self.next_move_blue) == True:

                    # print("BLUE GENERAL NEEDS TO BE UNCHECKED")
                    self._board[from_coordinate[1]][from_coordinate[0]] = self._board[to_coordinate[1]][
                        to_coordinate[0]]
                    self._board[to_coordinate[1]][from_coordinate[0]] = ""
                    return False

                else:
                    self._blue_is_in_check = False

            if self.is_red_in_check_helper(pos2):  # Logic to see if a move results in check
                self.next_move_red = pos2
                # print("red in check")
            if self.is_blue_in_check_helper(pos2):
                self.next_move_blue = pos2
                # print("blue in check")
            self.switch_turn()
            return True

    def is_legal_move(self, from_coordinate, current_piece: Piece, to_coordinate, next_piece: Piece):
        """Checks to see if there are any obstructions between a start and end position. Returns True or False to make move."""

        from_y = from_coordinate[1]
        from_x = from_coordinate[0]
        to_y = to_coordinate[1]
        to_x = to_coordinate[0]
        diff_y = to_y - from_y
        diff_x = to_x - from_x
        palace = [[3, 7], [4, 7], [5, 7], [3, 8], [4, 8], [5, 8], [3, 9], [4, 9], [5, 9],  # blue
                  [3, 0], [4, 0], [5, 0], [3, 1], [4, 1], [5, 1], [3, 2], [4, 2], [5, 2]]  # red

        def check_chariot_move(from_coordinate, current_piece, to_coordinate, next_piece):
            """Check for any chariot obstructions"""
            if diff_x != 0 and diff_y != 0:
                # CAN'T MOVE DIAGONALLY"
                return False

            if diff_x != 0:
                if diff_x > 0:  # Checking right
                    for i in range(from_x + 1, to_x, 1):
                        square_being_checked = self._board[from_y][i]
                        if i < to_x and square_being_checked != '':
                            # print("ERROR: THERE IS ANOTHER PIECE IN THE WAY")
                            return False

                if diff_x < 0:  # Checking left
                    for i in range(from_x - 1, to_x, -1):  # from_x-1 is necessary, otherwise it will count itself as an obstruction, same applies to other directions
                        square_being_checked = self._board[from_y][i]
                        if i > to_x and square_being_checked != '':
                            # print("ERROR: THERE IS ANOTHER PIECE IN THE WAY")
                            return False

            if diff_y != 0:  # Checking vertically (+y)
                if diff_y > 0:
                    for i in range(from_y + 1, to_y, 1):
                        square_being_checked = self._board[i][from_x]
                        if i < to_y and square_being_checked != '':
                            # print("ERROR: THERE IS ANOTHER PIECE IN THE WAY")
                            return False

                if diff_y < 0:  # Checking vertically (-y)
                    for i in range(from_y - 1, to_y, -1):  # don't count the starting piece (from_y-1) as an obstruction,
                        square_being_checked = self._board[i][from_x]  # checking vertically
                        if i > to_y and square_being_checked != '':  # if i (the row being checked) is greater than the destination (meaning i is lower on the board) and it is OCCUPIED, then the move is blocked
                            # print("ERROR: THERE IS ANOTHER PIECE IN THE WAY")
                            return False
            return True

        def check_soldier_move(from_coordinate, current_piece, to_coordinate, next_piece, palace):
            """Check for any soldier obstructions"""
            if from_coordinate in palace and to_coordinate in palace:  # start and end in palace
                if diff_x > 1 or diff_x < - 1 or diff_y > 1 or diff_y < -1:
                    return False
                square_being_checked = self._board[to_y][to_x]
                if square_being_checked == '' or square_being_checked != '':
                    return True
                return False

            if from_coordinate in palace and to_coordinate not in palace:  # start in palace, end outside of palace
                if diff_x != 0 and diff_y != 0:
                    # CAN'T MOVE DIAGONALLY
                    return False
                square_being_checked = self._board[to_y][to_x]
                if square_being_checked == '' or square_being_checked != '':
                    return True
                return False

            if from_coordinate not in palace and to_coordinate not in palace:
                if diff_x != 0 and diff_y != 0:
                    # CAN'T MOVE DIAGONALLY
                    return False

                if diff_x > 1 or diff_x < - 1 or diff_y > 1 or diff_y < -1:
                    return False

                square_being_checked = self._board[to_y][to_x]
                if square_being_checked == '' or square_being_checked != '':
                    return True
                return False

        def check_cannon_move(from_coordinate, current_piece, to_coordinate, next_piece):
            """Check for any cannon obstructions"""
            counter = 0  # if number of blockages > 1, return false

            if diff_x != 0:

                if diff_x == 2 and diff_y == 2:
                    if from_coordinate in palace and to_coordinate in palace:
                        square_being_checked = self._board[from_y + 1][from_x + 1]
                        if square_being_checked == '':
                            return False
                        if square_being_checked != '':
                            if square_being_checked.get_piece_type() == "Cannon":
                                return False
                            if square_being_checked.get_piece_type() != "Cannon":
                                return True
                    return False

                # if from_coordinate in palace and to_coordinate in palace:
                if diff_x == -2 and diff_y == -2:
                    if from_coordinate in palace and to_coordinate in palace:
                        square_being_checked = self._board[from_y - 1][from_x - 1]
                        if square_being_checked == '':
                            return False
                        if square_being_checked != '':
                            if square_being_checked.get_piece_type() == "Cannon":
                                return False
                            if square_being_checked.get_piece_type() != "Cannon":
                                return True
                    return False

                if diff_x == 2 and diff_y == -2:
                    if from_coordinate in palace and to_coordinate in palace:
                        square_being_checked = self._board[from_y - 1][from_x + 1]
                        if square_being_checked == '':
                            return False
                        if square_being_checked != '':
                            if square_being_checked.get_piece_type() == "Cannon":
                                return False
                            if square_being_checked.get_piece_type() != "Cannon":
                                return True
                    return False

                if diff_x == -2 and diff_y == 2:
                    if from_coordinate in palace and to_coordinate in palace:
                        square_being_checked = self._board[from_y + 1][from_x - 1]
                        if square_being_checked == '':
                            return False
                        if square_being_checked != '':
                            if square_being_checked.get_piece_type() == "Cannon":
                                return False
                            if square_being_checked.get_piece_type() != "Cannon":
                                return True
                    return False

                if from_coordinate not in palace and to_coordinate not in palace:
                    if diff_x != 0 and diff_y != 0:
                        # print("ERROR: CAN'T MOVE DIAGONALLY")
                        return False

                if diff_x > 0 and diff_y == 0:  # checking horizontally
                    for i in range(from_x + 1, to_x, 1):
                        square_being_checked = self._board[from_y][i]
                        if i < to_x and square_being_checked != '':
                            counter += 1
                            if counter > 1:
                                # print("MORE THAN ONE PIECE IN BETWEEN")
                                return False
                    for i in range(from_x + 1, to_x, 1):
                        square_being_checked = self._board[from_y][i]
                        if i < to_x and square_being_checked != '' and square_being_checked.get_piece_type() != "Cannon":  # valid move
                            if self._board[to_y][to_x] != '':
                                if self._board[to_y][
                                    to_x].get_piece_type() == "Cannon":  # cannon can't take cannon
                                    # print("CANNON CANT TAKE CANNON")
                                    return False
                            # print("CANNON JUMP")
                            return True
                if diff_x < 0 and diff_y == 0:  # checking horizontally
                    for i in range(from_x - 1, to_x, -1):
                        square_being_checked = self._board[from_y][i]
                        if i > to_x and square_being_checked != '':
                            counter += 1
                            if counter > 1:
                                # print("MORE THAN ONE PIECE IN BETWEEN")
                                return False
                    for i in range(from_x - 1, to_x, -1):
                        square_being_checked = self._board[from_y][i]
                        if i > to_x and square_being_checked != '' and square_being_checked.get_piece_type() != "Cannon":
                            if self._board[to_y][to_x] != "":
                                if self._board[to_y][to_x].get_piece_type() == "Cannon":
                                    # print("CANNON CANT TAKE CANNON")
                                    return False
                            # print("CANNON JUMP")
                            return True

            if diff_y != 0:

                if diff_y < 0 and diff_x == 0:  # checking vertically
                    for i in range(from_y - 1, to_y, -1):
                        square_being_checked = self._board[i][from_x]
                        if i > to_y and square_being_checked != '':
                            counter += 1
                            if counter > 1:
                                # print("MORE THAN ONE PIECE IN BETWEEN")
                                return False
                    for i in range(from_y - 1, to_y, -1):
                        square_being_checked = self._board[i][from_x]
                        if i > to_y and square_being_checked != '' and square_being_checked.get_piece_type() != "Cannon":
                            if self._board[to_y][to_x] != "":
                                if self._board[to_y][to_x].get_piece_type() == "Cannon":
                                    # print("CANNON CANT TAKE CANNON")
                                    return False
                            # print("CANNON JUMP")
                            return True
                if diff_y > 0 and diff_x == 0:  # checking vertically
                    for i in range(from_y + 1, to_y, 1):
                        square_being_checked = self._board[i][from_x]
                        if i < to_y and square_being_checked != '':
                            counter += 1
                            if counter > 1:
                                # print("MORE THAN ONE PIECE IN BETWEEN")
                                return False
                    for i in range(from_y + 1, to_y, 1):
                        square_being_checked = self._board[i][from_x]
                        if i < to_y and square_being_checked != '' and square_being_checked.get_piece_type() != "Cannon":
                            if self._board[to_y][to_x] != "":
                                if self._board[to_y][to_x].get_piece_type() == "Cannon":
                                    # print("CANNON CANT TAKE CANNON")
                                    return False
                            # print("CANNON JUMP")
                            return True

            return False

        def check_horse_move(from_coordinate, current_piece, to_coordinate, next_piece):
            """Check for any horse obstructions"""
            possible_moves = [[from_coordinate[0] + 1, from_coordinate[1] + 2],  # possible moves relative to current coordinate position
                              [from_coordinate[0] + 2, from_coordinate[1] + 1],
                              [from_coordinate[0] + 1, from_coordinate[1] - 2],
                              [from_coordinate[0] + 2, from_coordinate[1] - 1],
                              [from_coordinate[0] - 1, from_coordinate[1] + 2],
                              [from_coordinate[0] - 2, from_coordinate[1] + 1],
                              [from_coordinate[0] - 1, from_coordinate[1] - 2],
                              [from_coordinate[0] - 2, from_coordinate[1] - 1]]

            if diff_x == 0 or diff_y == 0:
                # print("ERROR: NOT POSSIBLE MOVE FOR HORSE")
                return False

            # Move logic is same for both players' horses

            if diff_x > 0 and diff_y < 0:  # upper right quadrant
                if to_coordinate not in possible_moves:
                    return False
                for i in range(from_y - 1, to_y, -1):
                    square_being_checked = self._board[i][from_x]
                    if i >= to_y and square_being_checked != '':
                        # print("ERROR: THERE IS ANOTHER PIECE IN THE WAY, VERTICAL")
                        return False
                for i in range(from_x + 1, to_x, 1):
                    square_being_checked = self._board[from_y][i]
                    if i <= to_y and square_being_checked != '':
                        # print("ERROR: THERE IS A PIECE IN THE WAY, HORIZONTAL")
                        return False

            if diff_x < 0 and diff_y < 0:  # upper left quadrant
                if to_coordinate not in possible_moves:
                    return False
                for i in range(from_y - 1, to_y, -1):
                    square_being_checked = self._board[i][from_x]
                    if i >= to_y and square_being_checked != '':
                        # print("ERROR: THERE IS ANOTHER PIECE IN THE WAY, VERTICAL")
                        return False
                for i in range(from_x - 1, to_x, 1):
                    square_being_checked = self._board[from_y][i]
                    if i >= to_y and square_being_checked != '':
                        # print("ERROR: THERE IS A PIECE IN THE WAY, HORIZONTAL")
                        return False

            if diff_x < 0 and diff_y > 0:  # lower left quadrant
                if to_coordinate not in possible_moves:
                    return False
                for i in range(from_y + 1, to_y, -1):
                    square_being_checked = self._board[i][from_x]
                    if i <= to_y and square_being_checked != '':
                        # print("ERROR: THERE IS ANOTHER PIECE IN THE WAY, VERTICAL")
                        return
                for i in range(from_x - 1, to_x, -1):
                    square_being_checked = self._board[from_y][i]
                    if i >= to_y and square_being_checked != '':
                        # print("ERROR: THERE IS A PIECE IN THE WAY, HORIZONTAL")
                        return False

            if diff_x > 0 and diff_y > 0:  # lower right quadrant
                if to_coordinate not in possible_moves:
                    return False

                for i in range(from_y + 1, to_y, -1):
                    square_being_checked = self._board[i][from_x]
                    if i <= to_y and square_being_checked != '':
                        # print("ERROR: THERE IS ANOTHER PIECE IN THE WAY, VERTICAL")
                        return

                for i in range(from_x + 1, to_x, 1):  # lower right quadrant
                    square_being_checked = self._board[from_y][i]
                    if i >= to_y and square_being_checked != '':
                        # print("ERROR: THERE IS A PIECE IN THE WAY, HORIZONTAL")
                        return False

            return True

        def check_elephant_move(from_coordinate, current_piece, to_coordinate, next_piece):
            # Move logic is same for both players' elephants

            possible_moves = [[from_coordinate[0] + 3, from_coordinate[1] + 2], # possible moves are relative to current posiiton
                              [from_coordinate[0] + 3, from_coordinate[1] - 2],
                              [from_coordinate[0] - 2, from_coordinate[1] + 3],
                              [from_coordinate[0] - 2, from_coordinate[1] - 3],
                              [from_coordinate[0] - 3, from_coordinate[1] - 2],
                              [from_coordinate[0] - 3, from_coordinate[1] + 2],
                              [from_coordinate[0] + 2, from_coordinate[1] - 3],
                              [from_coordinate[0] + 2, from_coordinate[1] + 3]]

            if diff_x == 0 or diff_y == 0:
                # print("ERROR: NOT A POSSIBLE MOVE FOR ELEPHANT")
                return False
            if to_coordinate not in possible_moves:
                return False

            # upper right quadrant
            if diff_x > 0 and diff_y < 0:

                if to_coordinate == [from_x + 2, from_y - 3]:
                    if self._board[from_y - 1][from_x] != '' or self._board[from_y - 2][from_x + 1] != '':
                        # print("ELEPHANT BLOCKED")
                        return False

                if to_coordinate == [from_x + 3, from_y - 2]:
                    if self._board[from_y][from_x + 1] != '' or self._board[from_y - 1][from_x + 2] != '':
                        # print("ELEPHANT BLOCKED")
                        return False

            # upper left quadrant
            if diff_x < 0 and diff_y < 0:

                if to_coordinate == [from_x - 2, from_y - 3]:
                    if self._board[from_y - 1][from_x] != '' or self._board[from_y - 2][from_x - 1] != '':
                        # print("ElEPHANT BLOCKED")
                        return False

                if to_coordinate == [from_x - 3, from_y - 2]:
                    if self._board[from_y][from_x - 1] != '' or self._board[from_y - 1][from_x - 2] != '':
                        # print("ELEPHANT BLOCKED")
                        return False

            # bottom right quadrant
            if diff_x > 0 and diff_y > 0:

                if to_coordinate == [from_x + 3, from_y + 2]:
                    if self._board[from_y][from_x + 1] != '' or self._board[from_y + 1][from_x + 2] != '':
                        # print("ELEPHANT BLOCKED")
                        return False

                if to_coordinate == [from_x + 2, from_y + 3]:
                    if self._board[from_y + 1][from_x] != '' or self._board[from_y + 2][from_x + 1] != '':
                        # print("ELEPHANT BLOCKED")
                        return False

            # bottom left quadrant
            if diff_x < 0 and diff_y > 0:
                if to_coordinate == [from_x - 2, from_y + 3]:
                    if self._board[from_y + 1][from_x] != '' or self._board[from_y + 2][from_x - 1] != '':
                        # print("ELEPHANT BLOCKED!")
                        return False
                if to_coordinate == [from_x - 3, from_y + 2]:
                    if self._board[from_y][from_x - 1] != '' or self._board[from_y + 1][from_x - 2] != '':
                        # print("ELEPHANT BLOCKED!")
                        return False

            return True

        def check_guard_move(from_coordinate, current_piece, to_coordinate, next_piece, palace):
            """Checks for guard obstructions"""
            if from_coordinate not in palace or to_coordinate not in palace: # Guard alternate palace logic
                # print("not in palace")
                return False

            if diff_x > 1 or diff_x < - 1 or diff_y > 1 or diff_y < -1:
                return False

            square_being_checked = self._board[to_y][to_x]
            if square_being_checked == '' or square_being_checked != '':
                # print("GUARD MOVED")
                return True
            return False

        def check_general_move(from_coordinate, current_piece, to_coordinate, next_piece, palace):
            if from_coordinate not in palace or to_coordinate not in palace:
                # print("not in palace")
                return False

            if diff_x > 1 or diff_x < - 1 or diff_y > 1 or diff_y < -1:  # apply to soldier as well
                return False

            square_being_checked = self._board[to_y][to_x]
            if square_being_checked == '' or square_being_checked != '':
                # print("GENERAL MOVED")
                return True
            return False

        piece_type = current_piece.get_piece_type()

        if piece_type == "Elephant":
            return check_elephant_move(from_coordinate, current_piece, to_coordinate, next_piece)
        if piece_type == "Horse":
            return check_horse_move(from_coordinate, current_piece, to_coordinate, next_piece)
        if piece_type == "Chariot":
            return check_chariot_move(from_coordinate, current_piece, to_coordinate, next_piece)
        if piece_type == "Soldier":
            return check_soldier_move(from_coordinate, current_piece, to_coordinate, next_piece, palace)
        if piece_type == "Cannon":
            return check_cannon_move(from_coordinate, current_piece, to_coordinate, next_piece)
        if piece_type == "Guard":
            return check_guard_move(from_coordinate, current_piece, to_coordinate, next_piece, palace)
        if piece_type == "General":
            return check_general_move(from_coordinate, current_piece, to_coordinate, next_piece, palace)