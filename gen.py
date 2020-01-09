import time
import copy
import random
level = "Easy"


class Cell:
    def __init__(self, position):
        self.possible_answers = [x+1 for x in range(9)]
        self.answer = None
        self.position = position
        self.solved = False
        self.leng = len(self.possible_answers)

    def remove(self, num):
        if num in self.possible_answers and not self.solved:
            self.possible_answers.remove(num)
            if self.leng == 1:
                self.answer = self.possible_answers[0]
                self.solved = True
        if num in self.possible_answers and self.solved:
            self.answer = 0

    def lenOfPossible(self):
        return len(self.possible_answers)

    def returnSolved(self):
        if self.solved:
            return self.possible_answers[0]
        else:
            return 0

    def setAnswer(self, num):
        if num in [1, 2, 3, 4, 5, 6, 7, 8, 9]:
            self.solved = True
            self.answer = num
            self.possible_answers = [num]
        else:
            raise ValueError

    def reset(self):
        self.possible_answers = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        self.answer = None
        self.solved = False


def empty_board():
    ans = []
    for x in range(1, 10):
        if x in [7, 8, 9]:
            intz = 7
            z = 7
        if x in [4, 5, 6]:
            intz = 4
            z = 4
        if x in [1, 2, 3]:
            intz = 1
            z = 1
        for y in range(1, 10):
            z = intz
            if y in [7, 8, 9]:
                z += 2
            if y in [4, 5, 6]:
                z += 1
            if y in [1, 2, 3]:
                z += 0
            c = Cell((x, y, z))
            ans.append(c)
    return ans


def sudokuGen():
    cells = [i for i in range(81)]
    sudoku = empty_board()
    while cells:
        lowest_num = []
        lowest = []
        for i in cells:
            lowest_num.append(sudoku[i].leng)
        m = min(lowest_num)
        for i in cells:
            if sudoku[i].leng == m:
                lowest.append(sudoku[i])
            try:
                choice_element = random.choice(lowest)
            except IndexError:
                break
            choice_index = sudoku.index(choice_element)
            try:
                cells.remove(choice_index)
            except ValueError:
                pass
            position_1 = choice_element.position
            if not choice_element.solved:
                possible_values = choice_element.possible_answers
                try:
                    final_value = random.choice(possible_values)
                except IndexError:
                    break
                choice_element.setAnswer(final_value)
                for i in cells:
                    position_2 = sudoku[i].position
                    if position_1[0] == position_2[0]:
                        sudoku[i].remove(final_value)
                    if position_1[1] == position_2[1]:
                        sudoku[i].remove(final_value)
                    if position_1[2] == position_2[2]:
                        sudoku[i].remove(final_value)

            else:
                final_value = choice_element.returnSolved()
                for i in cells:
                    position_2 = sudoku[i].position
                    if position_1[0] == position_2[0]:
                        sudoku[i].remove(final_value)
                    if position_1[1] == position_2[1]:
                        sudoku[i].remove(final_value)
                    if position_1[2] == position_2[2]:
                        sudoku[i].remove(final_value)
    return sudoku


def sudokuChecker(sudoku):
    for j in range(len(sudoku)):
        for k in range(len(sudoku)):
            if j != k:
                position_1 = sudoku[j].position
                position_2 = sudoku[k].position
                if position_1[0] == position_2[0] or position_1[1] == position_2[1] or position_1[2] == position_2[2]:
                    num1 = sudoku[k].returnSolved()
                    num2 = sudoku[j].returnSolved()
                    if num1 == num2:
                        return False
    return True


def perfectSudoku():
    result = False
    while not result:
        s = sudokuGen()
        result = sudokuChecker(s)
    return s


# please don't read this, this func is god's mistake, i didn't wanna copy my brooks' hw so here we are
def solver(sudoku, f=0):
    if f > 900:
        return False
    guesses = 0
    copy_s = copy.deepcopy(sudoku)
    cells = [i for i in range(81)]
    solvedCells = []
    for i in cells:
        if copy_s[i].lenOfPossible() == 1:
            solvedCells.append(i)
    while solvedCells != []:
        for n in solvedCells:
            cell = copy_s[n]
            position1 = cell.position
            finalValue = copy_s[n].returnSolved()
            for i in cells:
                position2 = copy_s[i].position
                if position1[0] == position2[0]:
                    copy_s[i].remove(finalValue)
                if position1[1] == position2[1]:
                    copy_s[i].remove(finalValue)
                if position1[2] == position2[2]:
                    copy_s[i].remove(finalValue)
                if copy_s[i].lenOfPossible() == 1 and i not in solvedCells and i in cells:
                    solvedCells.append(i)
                print(n)
            solvedCells.remove(n)
            cells.remove(n)
        if cells != [] and solvedCells == []:
            lowestNum = []
            lowest = []
            for i in cells:
                lowestNum.append(copy_s[i].lenOfPossible())
            m = min(lowestNum)
            for i in cells:
                if copy_s[i].lenOfPossible() == m:
                    lowest.append(copy_s[i])
            randomChoice = random.choice(lowest)
            randCell = copy_s.index(randomChoice)
            randGuess = random.choice(copy_s[randCell].possible_answers)
            copy_s[randCell].setAnswer(randGuess)
            solvedCells.append(randCell)
            guesses += 1
    if sudokuChecker(copy_s):
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
    if n < 30:
        s = solver(sudoku)
        if s != False:
            return s
        else:
            solve(sudoku, n + 1)
    else:
        return False


def puzzleGen(sudoku):
    cells = [i for i in range(81)]
    while cells:
        copy_s = copy.deepcopy(sudoku)
        randIndex = random.choice(cells)
        cells.remove(randIndex)
        copy_s[randIndex].reset()
        s = solve(copy_s)
        if not s[0]:
            f = solve(sudoku)
            print("Guesses: " + str(f[1]))
            print("Level: " + str(f[2]))
            return print(sudoku)
        elif equalChecker(s[0], solve(copy_s)[0]):
            if equalChecker(s[0], solve(copy_s)[0]):
                sudoku[randIndex].reset()
        else:
            f = solve(sudoku)
            return sudoku, f[1], f[2]


def equalChecker(s1, s2):
    for i in range(len(s1)):
        if s1[i].returnSolved() != s2[i].returnSolved():
            return False
    return True


def main(level):
    t1 = time.time()
    n = 0
    if level == 'Easy':
        p = perfectSudoku()
        s = puzzleGen(p)
        if s[2] != 'Easy':
            return main(level)
        t2 = time.time()
        t3 = t2 - t1
        print("Runtime is " + str(t3) + " seconds")
        print("Guesses: " + str(s[1]))
        print("Level: " + str(s[2]))
        print(s[0])
    if level == 'Medium':
        p = perfectSudoku()
        s = puzzleGen(p)
        while s[2] == 'Easy':
            n += 1
            s = puzzleGen(p)
            if n > 50:
                return main(level)
        if s[2] != 'Medium':
            return main(level)
        t2 = time.time()
        t3 = t2 - t1
        print("Runtime is " + str(t3) + " seconds")
        print("Guesses: " + str(s[1]))
        print("Level: " + str(s[2]))
        print(s[0])
    if level == 'Hard':
        p = perfectSudoku()
        s = puzzleGen(p)
        while s[2] == 'Easy':
            n += 1
            s = puzzleGen(p)
            if n > 50:
                return main(level)
        while s[2] == 'Medium':
            n += 1
            s = puzzleGen(p)
            if n > 50:
                return main(level)
        if s[2] != 'Hard':
            return main(level)
        t2 = time.time()
        t3 = t2 - t1
        print("Runtime is " + str(t3) + " seconds")
        print("Guesses: " + str(s[1]))
        print("Level: " + str(s[2]))
        print(s[0])
    if level == 'Insane':
        p = perfectSudoku()
        s = puzzleGen(p)
        while s[2] != 'Insane':
            n += 1
            s = puzzleGen(p)
            if n > 50:
                return main(level)
        t2 = time.time()
        t3 = t2 - t1
        print("Runtime is " + str(t3) + " seconds")
        print("Guesses: " + str(s[1]))
        print("Level: " + str(s[2]))
        print(s[0])
    else:
        raise ValueError


main("Easy")
