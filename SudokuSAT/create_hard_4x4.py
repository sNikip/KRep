import random

# with is like your try .. finally block in this case
with open("sat_tests/sudoku_txt/1000 sudokus.txt", 'r') as file:
    # read a list of lines into data
    data = file.readlines()




# and write everything back
#with open('stats.txt', 'w') as file:
#    file.writelines( data )

f = open("sat_tests/sudoku_txt/1000 sudokus hard.txt", "a")


for line in range(50):
    numbers = sum(c.isdigit() for c in data[line])
    lijst = list(data[line].strip())
    #print(numbers)
    #print(''.join(lijst))
    while numbers > 17:
        #print(lijst)
        indices = []
        for i in range(len(lijst)):
            if lijst[i].isdigit() is True:
                indices.append(i)
        rand_int = random.choice(indices)
        #print(rand_int)
        lijst[rand_int] = '.'
        indices.remove(rand_int)
        numbers += -1
        #print(numbers)
    if numbers == 17:
        new_lijst = ''.join(lijst)
        print(new_lijst, file=f)

f.close()
