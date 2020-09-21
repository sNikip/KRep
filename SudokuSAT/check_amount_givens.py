sudoku_amount = len(open('sat_tests/sudoku_txt/1000 sudokus.txt').readlines())
print(sudoku_amount)
linebreak_amount = sudoku_amount - 1

#open file in read mode
file = open("sat_tests/sudoku_txt/1000 sudokus.txt", "r")

#read the content of file and replace the dots with nothing
data = file.read().replace(".","")

#get the length of the data
number_of_characters = len(data)-linebreak_amount

average_given = number_of_characters/sudoku_amount
percentage_given = (average_given/81)*100

print('Number of characters in text file :', number_of_characters)
print('Average of givens per Sudoku :', average_given)
print('Amount percentage of givens: ', percentage_given)

