import random
from statistics import mode


def dp(cnf, solution):
    if not cnf:
        return True
    if [] in cnf:
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
    chosen = random_select(cnf) # first heuristic
    #chosen = most_common(cnf) # second heuristic -> DLIS

    sol_copy = [x for x in solution]
    a = dp(reduced(cnf, chosen), sol_copy)
    if a:
        # print('a ', chosen)
        for x in sol_copy:
            if x not in solution:
                solution.append(x)
        if chosen > 0:
            solution.append(chosen)
        return a
    sol_copy2 = [x for x in solution]
    b = dp(reduced(cnf, -chosen), sol_copy2)
    if b:
        # print('b ', -chosen)
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
    return random.choice(cnf_flat_list)


def most_common(cnf): # first heuristics: maximum individual sum
    if not cnf:
        return 0
    cnf_flat_list = cnf_to_flat_list(cnf)
    return mode(cnf_flat_list)


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
