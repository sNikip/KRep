from __future__ import print_function
import sat_solver
import time
import logging
log = logging.getLogger("my-logger")

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

def load_txt4(file): # transform a sudoku into cnf - can generalize this method by adding a dimension param for the 'for' loop
    f = open(file, 'r')
    data = f.read()
    f.close()
    cnf = []
    for i in range(1, 5):
        for j in range(1, 5):
            #print(data[0])
            if data[0] != '.':
                cnf.append([i*100 + j*10 + int(data[0])])
            data = data[1:]
    return cnf

def load_txt16(file): # transform a sudoku into cnf - can generalize this method by adding a dimension param for the 'for' loop
    f = open(file, 'r')
    data = f.read()
    f.close()
    cnf = []
    for i in range(1, 17):
        for j in range(1, 17):        
            if data[0] != '.':                
                if (data[0] == 'G'):
                    d = 16
                else:
                    d = int(data[0], 16)
                cnf.append([i*17*17 + j*17 + d])
            #print(i, j)
            #print(i*17*17 + j*17 + d)
            data = data[1:]
    return cnf


#sudoku = load_txt('sat_tests/sudoku_txt/sudoku1.txt')
#sudoku = load_txt4('sat_tests/sudoku_txt/4x4single.txt')
sudoku = load_txt16('sat_tests/sudoku_txt/16x16single.txt')
#sudoku = load_dimacs('sat_tests/sudoku_dimacs/sudoku2')
#rules = load_dimacs('sudoku-rules.txt')
#rules = load_dimacs('sat_tests/sudoku_dimacs/sudoku-rules-4x4.txt')
rules = load_dimacs('sat_tests/sudoku_dimacs/sudoku-rules-16x16.txt')
cnf = sudoku + rules


start = time.time()
sol = []
print(sat_solver.dpll(cnf, sol))
sol.sort()
print('Sudoku solution: ', sol)
print('Solution length: ', len(sol)) # length > 81 means there are multiple solutions
end = time.time()
print('Time: ', end - start)

lag = 0
dim = 16
for i in range(0, len(sol)):
    cell = i + 11 + (i // dim)
    #logging.warning("i --- " + str(i))
    #logging.warning("lag --- " + str(lag))
    #logging.warning("cell --- " + str(cell))
    #logging.warning("sol[i - lag] --- " + str(sol[i - lag]))
    #logging.warning("sol[i - lag] // 10 --- " + str(sol[i - lag] // 10))
    if sol[i - lag] // 10 != cell:
        print('Missing: ', end=' ')
        print(cell)
        lag = lag + 1


for i in range(0, len(sol)):
    print(sol[i]%10, end=' ')
    if (i+1) % dim == 0:
        print('\n', end='')


output = open('file.out', 'w')
for element in sol:
    output.write(str(element) + ' 0 \n')
output.close()
