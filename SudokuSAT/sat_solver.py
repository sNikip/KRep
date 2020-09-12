import random
from statistics import mode

solution = []


def dpll(cnf):
    if not cnf:
        return True
    if [] in cnf:
        return False
    cnf_copy = [x for x in cnf]  # deep copy
    for clause in cnf_copy:
        if len(clause) == 1:  # unit propagation
            if clause[0] > 0 and clause[0] not in solution:
                solution.append(clause[0])
            return dpll(reduced(cnf, clause[0]))
    # literals = literals_list(cnf)  it is slower with this
    # for literal in literals:
    #     if is_pure(literals, literal):
    #         return dpll(reduced(cnf, literal))

    # chosen = random(cnf) # no heuristic
    chosen = most_common(cnf) # first heuristic
    return dpll(reduced(cnf, chosen)) or dpll(reduced(cnf, -chosen))


def reduced(cnf, var): # returns a new cnf without clauses that include var and without -var
    new_cnf = []
    for clause in cnf:
        if var not in clause:
            new_cnf.append([x for x in clause if x != -var])
    return new_cnf


def cnf_to_flat_list(cnf):
    cnf_flat_list = []
    for clause in cnf:
        for literal in clause:
            cnf_flat_list.append(literal)
    return cnf_flat_list


def random(cnf):
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
