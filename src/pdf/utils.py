import glob


def find_files(pattern):
    """Find files matching pattern"""
    return glob.iglob(pattern)


def plural(num, singular, plural=None):
    if plural is None:
        plural = singular + 's'
    if num == 1:
        return singular
    else:
        return plural


def confirm_files(file_list):
    for index, file in enumerate(file_list, start=1):
        print(f'{index}. {file}')
    print('Are these the files in correct order? (y/n) ', end='')
    answer = input()
    accepted = ['y', 'yes']
    if answer.lower() in accepted:
        return True
    else:
        return False
