import random
from statistics import mode
from collections import defaultdict


def dpll(cnf, solution):
    if not cnf:
        return True
    if [] in cnf:
        return False
    for clause in cnf:
        if len(clause) == 1:  # unit propagation
            if clause[0] > 0 and clause[0] not in solution:
                solution.append(clause[0])
            return dpll(reduced(cnf, clause[0]), solution)
    # literals = literals_list(cnf)  it is slower with this
    # for literal in literals:
    #     if is_pure(literals, literal):
    #         return dpll(reduced(cnf, literal))

    #chosen = random_select(cnf)
    chosen = most_common(cnf) # first heuristic
    #chosen = moms(cnf) # first heuristic
    #chosen = jw(cnf)
    #print(chosen)

    sol_copy = [x for x in solution]
    a = dpll(reduced(cnf, chosen), sol_copy)
    if a:
        for x in sol_copy:
            if x not in solution:
                solution.append(x)
        if chosen > 0:
            solution.append(chosen)
        return a
    sol_copy2 = [x for x in solution]
    b = dpll(reduced(cnf, -chosen), sol_copy2)
    if b:
        for x in sol_copy2:
            if x not in solution:
                solution.append(x)
        if -chosen > 0:
            solution.append(-chosen)
    return b


def reduced(cnf, var): # returns a new cnf without clauses that include var and without -var
    new_cnf = []
    #print (var)
    for clause in cnf:
        #print(clause)
        if var not in clause:
            #print('HERE WE GO')
            new_cnf.append([x for x in clause if x != -var])
            #print([x for x in clause if x != -var])
    #print(new_cnf)
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

# get minimum size clauses
def minClauses(clauses):
	minClauses = []
	size = -1

	for clause in clauses:
		csize = len(clause)

		# Either the current clause is smaller
		if size == -1 or csize < size:
			minClauses = [clause]
			size = csize

		# Or it is of minimum size as well
		elif csize == size:
			minClauses.append(clause)

	return minClauses

def literalCountHelper(clauses, id):

	# Assign a score to each literal
	score = defaultdict(int)

	# Iterate over all clauses
	for clause in clauses:

		# Determine by how much to increment the score
		# DLIS : +1 (occurrences)
		# MOMs : +1 (occurrences)
		# JW   : +2^{-|Clause|}
		incr = 1

		for l in clause:
			score[l] += incr

	# Return the literal maximizing that score
	return max(score, key=score.get)

def moms(cnf):

	# Step 1 : Find Clause with Minimum Size
	minc = minClauses(cnf)

	# Step 2 : Find the literal with maximum occurrence
	return literalCountHelper(minc, "moms")


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
