from argparse import ArgumentParser, ArgumentTypeError
import os
import shutil


def directory_number(x):
    x = int(x)
    if x < 1 or x > 25:
        raise ArgumentTypeError("Number needs to be between 1 and 25 (including).")
    return x


# check whether we want to have the timer file
def copy_timer_file(file_path: str, destination_folder: str):
    if os.path.isfile(file_path):
        shutil.copy(file_path, os.path.join(destination_folder, file_path))
    else:
        print(f'Could not find timer file [{os.path.join(os.path.dirname(__file__), destination_folder, file_path)}]')


def main(args):
    folder_name = f'{args.number:02d}'
    default_file = 'default.py'
    timer_file = 'TimeIt.py'

    # check whether folder already exists
    if os.path.isdir(folder_name):
        print(f'Folder {folder_name} already exists and cannot be initialized.')
        exit(-1)

    # create the folder
    os.mkdir(folder_name)

    # read the solution file
    content = ""
    if not os.path.isfile(default_file):
        print(f'Could not find default python file [{default_file}].')
    else:
        with open(default_file) as filet:
            content = filet.read()

    # create the solution file
    with open(os.path.join(folder_name, args.solution_name), 'w') as f:
        f.write(content)

    # create the input file
    with open(os.path.join(folder_name, args.input_name), 'w') as f:
        f.write("")

    # copy the timer
    if args.timer:
        copy_timer_file(timer_file, folder_name)

    print('Done everything.')


if __name__ == '__main__':
    parser = ArgumentParser(prog='AoC Setup', description='What the program does',
                            epilog='This program sets up a new folder for the Advent of Code')

    # go through the folders and check whether they exist
    new_folder = 0
    for number in range(1, 26):
        if not os.path.isdir(f'{number:02d}'):
            new_folder = number
            break
    if not new_folder:
        print(f'All folders from 01 to 25 are already there.')
        exit(-1)

    parser.add_argument('-n', '--number', default=new_folder, type=directory_number,
                        help='The number of the new folder')
    parser.add_argument('-sn', '--solution_name', default='Solution.py', help='The name of the initial python file.')
    parser.add_argument('-in', '--input_name', default='input.txt', help='The name of the initial input file.')
    parser.add_argument('-t', '--timer', default=True, help='The name of the initial input file.')

    # run the main function
    main(parser.parse_args())
