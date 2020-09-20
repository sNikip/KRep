import pandas as pd


def det_file_site(version):
    if version == '4':
        f = open("4sudoku.txt", "a")
        site = 'http://www.menneske.no/sudoku/2/eng/'
        return create_sudo(f, site)
    elif version == '9':
        f = open("9sudoku.txt", "a")
        site = 'http://www.menneske.no/sudoku/eng/'
        return create_sudo(f, site)


def create_sudo(f, site):
    for i in range(0,10):
        df = pd.read_html(site)[3]
        df = df.fillna(0)
        df = df.astype(int)
        df = df.astype(str)
        df = df.stack().tolist()
        df = ''.join(df)
        print(df.replace("0", "."), file=f)
    f.close()
    return


user_version = input("Choose the sudoku version you want to make (4 or 9): ")
det_file_site(user_version)

