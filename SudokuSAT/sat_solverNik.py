import random
from statistics import mode
import numpy as np


nrofSplits = 0
nrofBacktracks = 0
heur = ''

def dp(cnf, solution):
    global nrofSplits
    global nrofBacktracks
    global nrofSplits_tosave
    global nrofBacktracks_tosave
    global putnamCalls
    if not cnf:
        nrofSplits_tosave = nrofSplits
        nrofBacktracks_tosave = nrofBacktracks
        putnamCalls = nrofBacktracks_tosave + nrofSplits_tosave + 1
        print(nrofSplits)
        nrofSplits = 0
        nrofBacktracks = 0
        return True
    if [] in cnf:
        nrofBacktracks += 1
        print('backtrack')
        return False
    for clause in cnf:
        if len(clause) == 1:  # unit propagation
            if clause[0] > 0 and clause[0] not in solution:
                solution.append(clause[0])
            # cnf = reduced(cnf, clause[0]) it is slower like this
            return dp(reduced(cnf, clause[0]), solution)
    # literals = literals_list(cnf)  it is slower with this
    # for literal in literals:
    #     if is_pure(literals, literal):
    #         return dpll(reduced(cnf, literal))

    # chosen = cnf[0][0]
    # chosen = random_select(cnf) # first heuristic
    chosen = most_common(cnf) # second heuristic -> DLIS
    nrofSplits += 1
    countA= 0
    countB= 0
    sol_copy = [x for x in solution]
    a = dp(reduced(cnf, chosen), sol_copy)
    if a:
        #countA += countA
        #print('a ', chosen)
        for x in sol_copy:
            if x not in solution:
                solution.append(x)
        if chosen > 0:
            solution.append(chosen)
        return a
    sol_copy2 = [x for x in solution]
    b = dp(reduced(cnf, -chosen), sol_copy2)
    if b:
        #countB += countB
        #print('b ', -chosen)
        for x in sol_copy2:
            if x not in solution:
                solution.append(x)
        if -chosen > 0:
            solution.append(-chosen)
    return b


def reduced(cnf, literal): # returns a new cnf without clauses that include var and without -var
    new_cnf = []
    for clause in cnf:
        if literal not in clause:
            new_cnf.append([x for x in clause if x != -literal])
    return new_cnf


def cnf_to_flat_list(cnf):
    cnf_flat_list = []
    for clause in cnf:
        for literal in clause:
            cnf_flat_list.append(literal)
    return cnf_flat_list


def random_select(cnf):
    if not cnf:
        return 0
    cnf_flat_list = cnf_to_flat_list(cnf)
    global heur
    heur = 'Random'
    return random.choice(cnf_flat_list)


def most_common(cnf): # first heuristics: maximum individual sum
    if not cnf:
        return 0
    cnf_flat_list = cnf_to_flat_list(cnf)
    global heur
    heur = 'DLIS'
    return mode(cnf_flat_list)

def min_heur(cnf):
    if not cnf:
        return 0
    cnf_flat_list = cnf_to_flat_list(cnf)
    global heur
    heur = 'Min Heur'
    return min(cnf_flat_list)

def pdlis(cnf):
    if not cnf:
        return 0
    cnf_flat_list = cnf_to_flat_list(cnf)
    values = [cnf_flat_list[key] for key in cnf_flat_list.keys()]
    prob = [(value / sum(values)) for value in values]

    return np.random.choice(cnf_flat_list, size = 1, p=prob)[0]




# this was for pure literal
# def is_pure(literals, literal):
#     if not literals:
#         return False
#     if -literal in literals:
#         return False
#     return True


# this was for pure literal
# def literals_list(cnf):
#     literals = []
#     for clause in cnf:
#         for literal in clause:
#             if literal not in literals:
#                 literals.append(literal)
#     return literals
