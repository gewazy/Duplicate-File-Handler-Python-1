import sys
import os
import hashlib


def main():
    path = check_args()
    ext = input('Enter file format:\n')

    files = search_file(path, ext) if ext else search_file(path)

    s_opt = sorting_option()

    sorted_files = files_sorter(files, s_opt)

    if asker('Check for duplicates?\n'):
        hashed_files = file_hasher(sorted_files)

    if asker('Delete files?\n'):
        deleter(hashed_files)


def check_args():
    ''' Checks if there is command-line argument. '''
    if len(args) != 2:
        print('Directory is not specified')
        sys.exit()
    else:
        return args[1]


def sorting_option():
    sort = input('Size sorting options:\n'
                 '1. Descending\n'
                 '2. Ascending\n')
    if sort not in ('1', '2'):
        print('Wrong option')
        return sorting_option()
    elif sort == '1':
        return True
    else:
        return False


def search_file(path, ext=''):
    '''
    Returns dictionary
        Parameters:
            path (str): path to root directory with files and folders
            ext (str) extension of the files to be searched;
                      if not specified, all types of files will be searched
        Returns:
            dictionary: key is size of files
                        value is list of key-size files.
    '''

    dic = {}
    os.chdir(path)
    for root, dirs, files in os.walk(".", topdown=True):
        for name in files:
            if name.endswith(ext):
                if os.path.getsize(os.path.join(root, name)) in dic:
                    dic[os.path.getsize(os.path.join(root, name))].append(os.path.join(root, name))
                else:
                    dic[os.path.getsize(os.path.join(root, name))] = [os.path.join(root, name)]
    return dic


def files_sorter(dic, order):
    '''Sorts and print data in specific way.'''
    dic = dict(sorted(dic.items(), reverse=order))
    for k, v in dic.items():
        print(k, 'bytes')
        for i in v:
            print(i)
        print()
    return dic


def file_hasher(files):
    '''
    :param files: dictonary with files to check for duplicate
    :return: nested dictionary with duplicate files
    '''

    hashed_files = {}
    c = 1  # for numbering duplicate files

    for k, v in files.items():
        if len(v) > 1:  # checking only multiple one-size files
            hashed = []  # collect hashed files [hash, path]
            for i in v:
                with open(i, "rb") as file:
                    m = hashlib.md5()
                    m.update(file.read())
                    h = m.hexdigest()
                    hashed.append([h, i])
            hashes = [i[0] for i in hashed]  # all hashes
            duplicate_hash = set([i for i in hashes if hashes.count(i) > 1])  # only duplicate hashes

            # selecting only duplicate files and sorting them by hash:
            hashed = sorted([i for i in hashed if i[0] in duplicate_hash], key=lambda x: x[0])
            h = {}  # temporary  dictionary for hash and numbered path
            for i in hashed:
                if i[0] in h:
                    h[i[0]].append([c, i[1]])
                    c += 1
                else:
                    h[i[0]] = [[c, i[1]]]
                    c += 1
            hashed_files[k] = h

    # printing duplicate files:
    for key, value in hashed_files.items():
        print(key, 'bytes')
        for k, v in value.items():
            print('Hash', k)
            for i in v:
                print(f'{i[0]}. {i[1]}')

    return hashed_files


def deleter(files):

    files_numbers = []  # possible files numbers to delete
    for key, values in files.items():
        for k, v in values.items():
            for i in v:
                files_numbers.append(str(i[0]))

    answer = str(input('Enter file numbers to delete:')).split(' ')

    to_delete = []
    for i in answer:
        if i not in files_numbers:
            print('Wrong format')
            return deleter(files)
        else:
            to_delete.append(int(i))

    total = 0
    for key, values in files.items():
        for k, v in values.items():
            for i in v:
                if i[0] in to_delete:
                    os.remove(i[1])
                    total += int(key)

    print(f'Total freed up space: {total} bytes')


def asker(question):
    answer = input(question).lower()

    if answer not in ('yes', 'no'):
        print('Wrong option')
        return asker(question)
    elif answer == 'no':
        sys.exit()
    else:
        return True



if __name__ == '__main__':
    args = sys.argv
    main()
