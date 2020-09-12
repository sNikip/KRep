import sat_solver
import time


def load_dimacs(file):
    f = open(file, 'r') # open file in reading mode
    data = f.read() # read file in data variable; string type
    f.close()
    lines = data.split("\n") # split the data into a list of lines
    cnf = []
    for line in lines:
        if len(line) == 0 or line[0] in ['c', 'p', '%', '0']:
            continue # ignore the lines without clauses
        clause = [int(x) for x in line.split()[:-1]] # transform the string clause format into a int one, remove the last 0;
        cnf.append(clause) # add the clause to the list
    return cnf


def load_txt(file): # transform a sudoku into cnf
    f = open(file, 'r')
    data = f.read()
    f.close()
    cnf = []
    for i in range(1, 10):
        for j in range(1, 10):
            if data[0] != '.':
                cnf.append([i*100 + j*10 + int(data[0])])
            data = data[1:]
    return cnf


# sudoku = load_txt('sat_tests/sudoku_txt/sudoku1.txt')
sudoku = load_dimacs('sat_tests/sudoku_dimacs/sudoku1')
rules = load_dimacs('sudoku-rules.txt')
cnf = sudoku + rules


start = time.time()
print(sat_solver.dpll(cnf))
sat_solver.solution.sort()
print('Sudoku solution: ', sat_solver.solution)
print('Solution length: ', len(sat_solver.solution)) # length > 81 means there are multiple solutions
end = time.time()
print('Time: ', end - start)


output = open('file.out', 'w')
if sat_solver.dpll(cnf):
    for element in sat_solver.solution:
        output.write(str(element) + ' 0 \n')
output.close()
