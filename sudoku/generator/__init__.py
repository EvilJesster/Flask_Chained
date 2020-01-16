import time
import copy
import random

DEBUG = False
EASY = 'Easy'
MEDIUM = 'Medium'
HARD = 'Hard'
INSANE = 'Insane'
DEMO = 'Demo'

class Cell:
    def __init__(self, position):
        self.possibleAnswers = [x + 1 for x in range(9)]
        self.answer = None
        self.position = position
        self.solved = False

    def __repr__(self):
        return str(self.answer)

    def remove(self, num):
        if num in self.possibleAnswers and not self.solved:
            self.possibleAnswers.remove(num)
            if len(self.possibleAnswers) == 1:
                self.answer = self.possibleAnswers[0]
                self.solved = True
        if num in self.possibleAnswers and self.solved:
            self.answer = 0

    def len_of_possible(self):
        """ finds the length of all possible solutions to the cell"""
        return len(self.possibleAnswers)

    def return_solved(self):
        return self.possibleAnswers[0] if self.solved else 0

    def set_answer(self, num):
        """ solves the cell, removes all other possible answers.
        if an input solution is not a valid solution an error is thrown"""
        if num in [x + 1 for x in range(9)]:
            self.solved = True
            self.answer = num
            self.possibleAnswers = [num]
        else:
            raise ValueError

    def reset(self):
        self.possibleAnswers = [x + 1 for x in range(9)]
        self.answer = None
        self.solved = False


def empty_sudoku():
    ans = []
    for x in range(1, 10):
        if 7 <= x <= 9:
            intz = 7
        elif 4 <= x <= 6:
            intz = 4
        else:
            intz = 1
        for y in range(1, 10):
            z = intz
            if 7 <= y <= 9:
                z += 2
            elif 4 <= y <= 6:
                z += 1
            else:
                z += 0
            c = Cell((x, y, z))
            ans.append(c)
    return ans

def sudoku_to_array(sudoku):
    row1 = row2 = row3 = row4 = row5 = row6 = row7 = row8 = row9 = []
    for i in range(81):
        if i in range(0, 9):
            row1.append(sudoku[i].return_solved())
        if i in range(9, 18):
            row2.append(sudoku[i].return_solved())
        if i in range(18, 27):
            row3.append(sudoku[i].return_solved())
        if i in range(27, 36):
            row4.append(sudoku[i].return_solved())
        if i in range(36, 45):
            row5.append(sudoku[i].return_solved())
        if i in range(45, 54):
            row6.append(sudoku[i].return_solved())
        if i in range(54, 63):
            row7.append(sudoku[i].return_solved())
        if i in range(63, 72):
            row8.append(sudoku[i].return_solved())
        if i in range(72, 81):
            row9.append(sudoku[i].return_solved())
    return row1 + row2 + row3 + row4 + row5 + row6 + row7 + row8 + row9


def sudoku_gen():
    """Generates a completed sudoku. Board is as random as it can get"""
    cells = [i for i in range(81)] 
    sudoku = empty_sudoku()
    while len(cells) != 0:
        lowest_num = []
        lowest = []
        for i in cells:
            lowest_num.append(
                sudoku[i].len_of_possible())  
        m = min(lowest_num)
        '''Puts all of the cells with the lowest number of possible answers in a list titled Lowest'''
        for i in cells:
            if sudoku[i].len_of_possible() == m:
                lowest.append(sudoku[i])
        '''Now we randomly choose a possible answer and set it to the cell'''
        choice_element = random.choice(lowest)
        choice_index = sudoku.index(choice_element)
        cells.remove(choice_index)
        position1 = choice_element.position
        if not choice_element.solved:  ##the actual setting of the cell
            possible_values = choice_element.possibleAnswers
            final_value = random.choice(possible_values)
            choice_element.set_answer(final_value)
            for i in cells:
                position2 = sudoku[i].position
                if position1[0] == position2[0]:
                    sudoku[i].remove(final_value)
                if position1[1] == position2[1]:
                    sudoku[i].remove(final_value)
                if position1[2] == position2[2]:
                    sudoku[i].remove(final_value)

        else:
            final_value = choice_element.return_solved()
            for i in cells:
                position2 = sudoku[i].position
                if position1[0] == position2[0]:
                    sudoku[i].remove(final_value)
                if position1[1] == position2[1]:
                    sudoku[i].remove(final_value)
                if position1[2] == position2[2]:
                    sudoku[i].remove(final_value)
    return sudoku


def sudoku_checker(sudoku):
    """ Checks to see if an input a completed sudoku puzzle is of the correct format and abides by all
        of the rules of a sudoku puzzle. Returns True if the puzzle is correct. False if otherwise"""
    for i in range(len(sudoku)):
        for n in range(len(sudoku)):
            if i != n:
                position1 = sudoku[i].position
                position2 = sudoku[n].position
                if position1[0] == position2[0] or position1[1] == position2[1] or position1[2] == position2[2]:
                    num1 = sudoku[i].return_solved()
                    num2 = sudoku[n].return_solved()
                    if num1 == num2:
                        return False
    return True


def perfect_sudoku():
    """Generates a completed sudoku. Sudoku is in the correct format and is completly random"""
    result = False
    s = None
    while not result:
        s = sudoku_gen()
        result = sudoku_checker(s)
    return s

## this is a rough draft of a generic sudoku solver, this will be sufficiently expedited at a later moment in time
def solver(sudoku, f=0):
    if f > 900:
        return False
    guesses = 0
    copy_s = copy.deepcopy(sudoku)
    cells = [i for i in range(81)]
    solved_cells = []
    for i in cells:
        if copy_s[i].len_of_possible() == 1:
            solved_cells.append(i)
    while solved_cells:
        for n in solved_cells:
            cell = copy_s[n]
            position1 = cell.position
            final_value = copy_s[n].return_solved()
            for i in cells:
                position2 = copy_s[i].position
                if position1[0] == position2[0]:
                    copy_s[i].remove(final_value)
                if position1[1] == position2[1]:
                    copy_s[i].remove(final_value)
                if position1[2] == position2[2]:
                    copy_s[i].remove(final_value)
                if copy_s[i].len_of_possible() == 1 and i not in solved_cells and i in cells:
                    solved_cells.append(i)
                ##print(n)
            solved_cells.remove(n)
            cells.remove(n)
        if cells != [] and solved_cells == []:
            lowest_num = []
            lowest = []
            for i in cells:
                lowest_num.append(copy_s[i].len_of_possible())
            m = min(lowest_num)
            for i in cells:
                if copy_s[i].len_of_possible() == m:
                    lowest.append(copy_s[i])
            random_choice = random.choice(lowest)
            rand_cell = copy_s.index(random_choice)
            rand_guess = random.choice(copy_s[rand_cell].possibleAnswers)
            copy_s[rand_cell].set_answer(rand_guess)
            solved_cells.append(rand_cell)
            guesses += 1
    if sudoku_checker(copy_s):
        if guesses == 0:
            level = 'Easy'
        elif guesses <= 2:
            level = 'Medium'
        elif guesses <= 7:
            level = 'Hard'
        else:
            level = 'Insane'
        return copy_s, guesses, level
    else:
        return solver(sudoku, f + 1)


def solve(sudoku, n=0):
    """ Uses the solver method to solve a puzzle. This method was built in order to avoid recursion depth errors. Returns True if the puzzle is solvable and
        false if otherwise"""
    if n < 30:
        s = solver(sudoku)
        return s if s else solve(sudoku, n + 1)
    return False


def puzzle_gen(sudoku, demo_parameter=False):
    """ Generates a puzzle with a unique solution. """
    cells = [i for i in range(81)]
    while cells:
        copy_s = copy.deepcopy(sudoku)
        rand_index = random.choice(cells) if not demo_parameter else random.choice(42, 36, 25)
        cells.remove(rand_index)
        copy_s[rand_index].reset()
        s = solve(copy_s)
        # print(s)
        if not s[0]:
            f = solve(sudoku)
            print("Guesses: " + str(f[1]))
            print("Level: " + str(f[2]))
            return printSudoku(sudoku)
        elif equal_checker(s[0], solve(copy_s)[0]):
            if equal_checker(s[0], solve(copy_s)[0]):
                sudoku[rand_index].reset()
        else:
            f = solve(sudoku)
            ##            print("Guesses: " + str(f[1]))
            ##            print("Level: " + str(f[2]))
            #print([str(x) for x in sudoku], f[1], f[2])
            return sudoku, f[1], f[2]
        

def equal_checker(s1, s2):
    """ Checks to see if two puzzles are the same"""
    for i in range(len(s1)):
        if s1[i].return_solved() != s2[i].return_solved():
            return False
    return True


def main(level):
    t1 = time.time()
    n = 0
    if level == 'Easy':
        p = perfect_sudoku()
        solved = copy.deepcopy(p)
        s = puzzle_gen(p)
        if s[2] != 'Easy':
            return main(level)
        t2 = time.time()
        t3 = t2 - t1
        if DEBUG:
            print("Runtime is " + str(t3) + " seconds")
            print("Guesses: " + str(s[1]))
            print("Level: " + str(s[2]))
            return sudoku_to_array(s[0])[:81], solved
        if level == 'Medium':
            p = perfect_sudoku()
            solved = copy.deepcopy(p)
            s = puzzle_gen(p)
        while s[2] == 'Easy':
            n += 1
            s = puzzle_gen(p)
            if n > 50:
                return main(level)
        if s[2] != 'Medium':
            return main(level)
        t2 = time.time()
        t3 = t2 - t1
        if DEBUG:
            print("Runtime is " + str(t3) + " seconds")
            print("Guesses: " + str(s[1]))
            print("Level: " + str(s[2]))
            printSudoku(s[0])
        return sudoku_to_array(s[0])[:81], solved
    if level == 'Hard':
        p = perfect_sudoku()
        solved = copy.deepcopy(p)
        s = puzzle_gen(p)
        while s[2] == 'Easy':
            n += 1
            s = puzzle_gen(p)
            if n > 50:
                return main(level)
        while s[2] == 'Medium':
            n += 1
            s = puzzle_gen(p)
            if n > 50:
                return main(level)
        if s[2] != 'Hard':
            return main(level)
        t2 = time.time()
        t3 = t2 - t1
        if DEBUG:
            print("Runtime is " + str(t3) + " seconds")
            print("Guesses: " + str(s[1]))
            print("Level: " + str(s[2]))
        printSudoku(s[0])
        return sudoku_to_array(s[0])[:81], solved
    if level == 'Insane':
        p = perfect_sudoku()
        solved = copy.deepcopy(p)
        s = puzzle_gen(p)
        while s[2] != 'Insane':
            n += 1
            s = puzzle_gen(p)
            if n > 50:
                return main(level)
        t2 = time.time()
        t3 = t2 - t1
        if DEBUG:
            print("Runtime is " + str(t3) + " seconds")
            print("Guesses: " + str(s[1]))
            print("Level: " + str(s[2]))
            printSudoku(s[0])
        return sudoku_to_array(s[0])[:81], solved
    if level == 'Demo':
        p = perfect_sudoku()
        s = copy.deepcopy(p)
        return sudoku_to_array(s)[:81], p
    else:
        print("Difficulty doesn't exist")
        raise ValueError

def gen_sudoku(difficulty):
    # for testing    
    assert(difficulty in [EASY, MEDIUM, HARD, INSANE, DEMO])
    ans = main(difficulty)
    return ans
