import random

# with is like your try .. finally block in this case
with open("sat_tests/sudoku_txt/4x4 test a.txt", 'r') as file:
    # read a list of lines into data
    data = file.readlines()

def make_list(list):
    return [[el] for el in list]


#for line in data:
    print(line)
#sudo = make_list(data)
#for item in sudo[0]:
#    print(item)

#print "Your name: " + data[0]

# now change the 2nd line, note that you have to add a newline
#data[1] = 'Mage\n'

# and write everything back
#with open('stats.txt', 'w') as file:
#    file.writelines( data )


""""for line in range(len(data)):
    numbers = sum(c.isdigit() for c in data[line])
    lijst = list(data[line].strip())
    print(numbers)
    print(lijst)
    indices = []
    while numbers > 3:
        #print(numbers)
        for i in range(len(lijst)):
            if lijst[i].isdigit() is True:
                indices.append(i)
        rand_int = random.choice(indices)
        #print(rand_int)
        lijst[rand_int] = '.'
        numbers += -1
    print(numbers)
    print(lijst)"""

a = ['1', '2', '3', '4', '6', '7']
numbers = sum(c.isdigit() for c in a)


while numbers > 3:
    print(a)
    indices = []
    for i in range(len(a)):
        if a[i].isdigit() is True:
            indices.append(i)
    rand_int = random.choice(indices)
    #print(rand_int)
    a[rand_int] = '.'
    indices.remove(rand_int)
    numbers += -1
    print(numbers)
print(a)
