import random
from statistics import mode
import numpy as np

nrofSplits = 0
nrofBacktracks = 0
heur = ''

def dp(cnf, solution, h):
    global nrofSplits
    global nrofBacktracks
    global nrofSplits_tosave
    global nrofBacktracks_tosave
    if not cnf:
        nrofSplits_tosave = nrofSplits
        nrofBacktracks_tosave = nrofBacktracks
        nrofSplits = 0
        nrofBacktracks = 0
        return True
    if [] in cnf:
        nrofBacktracks += 1
        return False
    for clause in cnf:
        if len(clause) == 1:  # unit propagation
            if clause[0] > 0 and clause[0] not in solution:
                solution.append(clause[0])
            # cnf = reduced(cnf, clause[0])
            return dp(reduced(cnf, clause[0]), solution, h)

    if h == 0:
        chosen = cnf[0][0]
    elif h == 1:
        chosen = random_select(cnf) # first heuristic
    elif h == 2:
        chosen = most_common(cnf) # second heuristic -> DLIS
    elif h == 3:
        chosen = dlcs(cnf)
    elif h == 4:
        chosen = min_heur(cnf)

    nrofSplits += 1

    sol_copy = [x for x in solution]
    a = dp(reduced(cnf, chosen), sol_copy, h)
    if a:
        for x in sol_copy:
            if x not in solution:
                solution.append(x)
        if chosen > 0:
            solution.append(chosen)
        return a
    sol_copy2 = [x for x in solution]
    b = dp(reduced(cnf, -chosen), sol_copy2, h)
    if b:
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


def dlcs(cnf): # first heuristics: maximum combined sum
    if not cnf:
        return 0
    cnf_flat_list = cnf_to_flat_list(cnf)
    global heur
    heur = 'DLCS'
    count_pos = 0
    count_neg = 0
    m = mode([abs(x) for x in cnf_flat_list])
    for el in cnf_flat_list:
        if el == m:
            count_pos += 1
        elif el == -m:
            count_neg += 1
    if count_pos > count_neg:
        return m
    return -m


def min_heur(cnf):
    if not cnf:
        return 0
    cnf_flat_list = cnf_to_flat_list(cnf)
    global heur
    heur = 'Min Heur'
    return min(cnf_flat_list)

def jw(cnf):
    scores = get_jw_scores(cnf)
    return max(scores, key=scores.get)

def get_jw_scores(cnf, w=2):
    scores = {}
    for clause in cnf:
        for lit in clause:
            if lit in scores:
                scores[lit] += w ** -len(clause)
            else:
                scores[lit] = w ** -len(clause)
    return scores

