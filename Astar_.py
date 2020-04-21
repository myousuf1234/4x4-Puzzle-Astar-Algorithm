from queue import PriorityQueue  # will use priority queue when looping
                                    # through puzzle objects

class PuzzleAstar(object):  # class puzzle solver using A* search
    def __init__(self, puzzle, depth):

        # the puzzleboard
        self.puzzle = puzzle
        self.next_moves = []  # next moves
        self.currturn_moves = []  # moves right now
        self.depth = depth  # current level

        # the f(n) value
        self.astar_val = 0

    def __gt__(self, other):  # is a star algo currently greater than the other algorithm?
        if self.astar_val > other.astar_val:  # greater than operator overloader
            return True
        else:
            return False

    def copyfunc(self, puzzle):  # a copy function to copy an array over
        copyarr = []
        for i in puzzle:
            arr = []
            for j in i:
                arr.append(j)
            copyarr.append(arr)
        return copyarr

    def gen_next_move(self):  # restriction function on what moves can and cannot be made
        temp_next_move = []  # a next move array local to this function
        if self.puzzle[0][0] != '0' and self.puzzle[1][0] != '0' and self.puzzle[2][0] != '0' and self.puzzle[3][0] != '0':
            temp_next_move.append('L')

        if self.puzzle[0][3] != '0' and self.puzzle[1][3] != '0' and self.puzzle[2][3] != '0' and self.puzzle[3][3] != '0':
            temp_next_move.append('R')

        if self.puzzle[0][0] != '0' and self.puzzle[0][1] != '0' and self.puzzle[0][2] != '0' and self.puzzle[0][3] != '0':
            temp_next_move.append('U')

        if self.puzzle[3][0] != '0' and self.puzzle[3][1] != '0' and self.puzzle[3][2] != '0' and self.puzzle[3][3] != '0':
            temp_next_move.append('D')
        self.next_moves = temp_next_move

    def aStar_func(self, goal_board):
        mh_distance = 0  # will be used for sum of manhattan distances
        for i in range(1, 16):
            start_board = target_finder(self.puzzle, str(i))
            end_board = target_finder(goal_board, str(i))

            # manhattan heuristic
            mh_distance = mh_distance + abs(start_board[0] - end_board[0]) + abs(start_board[1] - end_board[1])

        # depth is g(n) and mh_distance is h(n). this computed value is f(n)
        self.astar_val = self.depth + mh_distance


def copyfunc2(puzzle):  # copy function usable outside of an instance of the class
    copyarr = []
    for i in puzzle:
        arr = []
        for j in i:
            arr.append(j)
        copyarr.append(arr)
    return copyarr


def file_browse(fname):  # open file function
    f = open(fname, "r")
    file_info = f.read().splitlines()
    inp_board = [line.split() for line in file_info]

    # the first will be input board, the second will be output board
    return inp_board[0:4], inp_board[5:9]


def target_finder(puzzle, target):  # helpful function to find target vals instead of using
    # this tedious loop over and over again
    for i in range(4):
        for j in range(4):
            if puzzle[i][j] == target:
                return [i, j]


def tile_switch(curr_board, move):  # switching positions when blank tile moves left, right, up, or down

    # find location of blank tile which has a val of 0
    blank_tile = target_finder(curr_board, '0')
    replace_board = copyfunc2(curr_board)
    if move == 'U':
        replace_board[blank_tile[0]][blank_tile[1]] = replace_board[blank_tile[0] - 1][blank_tile[1]]
        replace_board[blank_tile[0] - 1][blank_tile[1]] = '0'
    elif move == 'D':
        replace_board[blank_tile[0]][blank_tile[1]] = replace_board[blank_tile[0] + 1][blank_tile[1]]
        replace_board[blank_tile[0] + 1][blank_tile[1]] = '0'
    elif move == 'L':
        replace_board[blank_tile[0]][blank_tile[1]] = replace_board[blank_tile[0]][blank_tile[1] - 1]
        replace_board[blank_tile[0]][blank_tile[1] - 1] = '0'
    elif move == 'R':
        replace_board[blank_tile[0]][blank_tile[1]] = replace_board[blank_tile[0]][blank_tile[1] + 1]
        replace_board[blank_tile[0]][blank_tile[1] + 1] = '0'
    return replace_board


def make_new_board(curr_puzz, move, goal_board):  # create new board based on move,
    # need to do this every move
    # switch tiles and create new board based on that
    replace_board = tile_switch(curr_puzz.puzzle, move)

    # create new object with replace_board's properties
    mod_puzzle = PuzzleAstar(replace_board, curr_puzz.depth + 1)

    # copying over list of current moves undertaken
    curr_moves = mod_puzzle.copyfunc(curr_puzz.currturn_moves)

    curr_moves.append(move)

    mod_puzzle.currturn_moves = curr_moves
    mod_puzzle.aStar_func(goal_board)
    mod_puzzle.gen_next_move()
    return mod_puzzle


def main():
    node_track = 1  # will use this as counter for nodes created

    # sets up the input and output puzzles from the text file
    input_board, goal_board = file_browse("Input5.txt")

    input_puzzle = PuzzleAstar(input_board, 0)
    input_puzzle.gen_next_move()
    input_puzzle.aStar_func(goal_board)

    # an array checking for repeats, since A* does not want to waste time exploring repeat nodes
    repeats = [input_board]

    priorityq = [input_puzzle]

    f = open("output1.txt", "w")
    i = 0
    while i < 4:  # 4x4
        f.write(str(input_board[i]))
        f.write("\n")
        i = i + 1
    f.write("\n")
    i = 0

    while i < 4:
        f.write(str(goal_board[i]))
        f.write("\n")
        i = i + 1
    f.write("\n")

    astararray = []  # holds fvals leading to solution

    while priorityq:
        priorityq.sort(reverse=True)

        # puzzle currently being looked at
        top_puzzle = priorityq.pop()

        # append the f(n) values for the nodes leading to solution
        astararray.append(top_puzzle.astar_val)

        if top_puzzle.puzzle == goal_board:

            # depth of solution, f.write() only accepts strings
            f.write(str(top_puzzle.depth))

            f.write("\n")

            # total nodes created
            f.write(str(node_track))
            f.write("\n")

            for i in top_puzzle.currturn_moves:
                f.write(str(i))  # The list of correct moves to get to goal node
            f.write("\n")

            # we've found what we want so stop the loop
            break

        for move in top_puzzle.next_moves:
            mod_puzzle = make_new_board(top_puzzle, move, goal_board)
            if mod_puzzle.puzzle in repeats:

                # if we come across something we've seen already, go back to start of for loop
                continue

            else:
                node_track += 1

                # keep track of the puzzle as it is
                repeats.append(mod_puzzle.puzzle)

                priorityq.append(mod_puzzle)

    # for loop to write the astar values to the document
    for elem in astararray:
        f.write(str(elem))
        f.write(" ")


main()
