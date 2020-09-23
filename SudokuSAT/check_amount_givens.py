def determine_sudoku_file(version):
    if version == 4:
        file = open("sat_tests/sudoku_txt/4x4.txt", "r") #open file in read mode
        sudoku_amount = len(open('sat_tests/sudoku_txt/4x4.txt').readlines())
        return check_sudoku(file, sudoku_amount, version)
    elif version == 9:
        file = open("sat_tests/sudoku_txt/1000 sudokus hard.txt", "r") #open file in read mode
        sudoku_amount = len(open('sat_tests/sudoku_txt/1000 sudokus hard.txt').readlines())
        return check_sudoku(file, sudoku_amount, version)


def check_sudoku(file, sudoku_amount, version):
    print('Amount of sudokus in this file :', sudoku_amount)
    linebreak_amount = sudoku_amount

    #read the content of file and replace the dots with nothing
    data = file.read().replace(".","")

    #get the length of the data
    number_of_givens = len(data)-linebreak_amount

    average_given = number_of_givens/sudoku_amount
    percentage_given = (average_given/(version*version))*100

    print('Total amount of givens in text file :', number_of_givens)
    print('Average of givens per Sudoku :', average_given)
    print('Average percentage of givens: ', percentage_given)


pick_sudoku = input("Choose the sudoku version you want to analyze (4 or 9): ")
determine_sudoku_file(int(pick_sudoku))

