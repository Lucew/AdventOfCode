import timeit
import os
import importlib
import contextlib
from inspect import getmembers, isfunction, getfullargspec
from argparse import ArgumentParser
import time


def import_folder_modules(partial_module_name: str = 'Solution'):
    imported_modules = []
    for module in os.listdir(os.path.dirname(__file__)):
        if module.endswith('.py') and partial_module_name in module:
            imported_modules.append(importlib.import_module(module[:-3]))
    return imported_modules


def check_input_arguments(function: callable):

    # inspect the function
    specc = getfullargspec(function)

    # check that all arguments have default values
    return not specc.args or (not specc.defaults or len(specc.args) == len(specc.defaults))


def prepare_modules(modules: list, valid_function_names: tuple = ('main1', 'main2')):

    # go through the models and get handles to all functions that have the specified names
    function_handles = dict()
    for module in modules:

        # get the function handles and names
        functions = getmembers(module, isfunction)

        # make sure all the functions have only defaulted value arguments
        functions = list(filter(lambda function: check_input_arguments(function[1]), functions))

        # make a dict with function handles and search for certain names
        function_handles[module.__name__] = {name: handle for name, handle in functions if name in valid_function_names}

    return function_handles


def time_the_functions(function_handles: dict[dict[callable]],
                       measurements: int = 5, repetition_per_measurement: int = 100):

    # get the elapsed time for the measurements
    started = time.time()

    # go through the functions and time them (suppressing print output)
    timings = dict()
    with contextlib.redirect_stdout(None):
        for module, functions in function_handles.items():
            for function, handle in functions.items():

                # get the timings
                timed = timeit.Timer(handle).repeat(repeat=measurements, number=repetition_per_measurement)

                # get the per function basis
                timed = [ele/repetition_per_measurement for ele in timed]

                # save the timings
                timings[f'{module}.{function}'] = timed

    # check whether we timed anything
    if not timings:
        print(f'We found nothing to time.')
        exit(-1)

    # compute mean and std for the measurements
    timings = {key: min(values) for key, values in timings.items()}

    # get the max key length
    max_key_length = max(len(key) for key in timings.keys())

    # make the header for the table
    table_header = f'{"| Function names".ljust(max_key_length+2)} | Minimum runtime in ms'

    # sort the timings and create the table lines
    timings = sorted(timings.items(), key=lambda x: x[1])
    table_lines = [f'| {key.ljust(max_key_length)} | {value*1000:0.2f} '
                   f'(+{(value - timings[idx-1][1])*1000 if idx else 0:0.2f})'
                   for idx, (key, value) in enumerate(timings)]

    # get the table width
    table_width = max(max(len(line) for line in table_lines), len(table_header))

    # get a table separator
    table_separator = '-'*(table_width+2)

    # print the result
    print()
    print('Functions testing!')
    print()
    print(f'We found {len(function_handles)} modules and {len(timings)} functions overall.')
    print(f'For every functions we ran {measurements} measurements '
          f'and {repetition_per_measurement} repetitions for each measurement.')
    print()
    print(table_separator)
    print(table_header.ljust(table_width) + ' |')
    print(table_separator)
    for line in table_lines:
        # shift the | to the end of the table line
        print(line.ljust(table_width) + ' |')
    print(table_separator)

    # make the timing overall print
    print()
    print(f'Overall time elapsed during this test (including prints): { time.time() - started:0.3f} s.')
    print()


def main(args):

    # import the modules with specified name
    modules = import_folder_modules(partial_module_name=args.module)

    # get all the functions in our current directory
    function_handles = prepare_modules(modules, valid_function_names=tuple(args.functions))

    # time and print the function
    time_the_functions(function_handles, measurements=args.measurements, repetition_per_measurement=args.repetitions)


if __name__ == '__main__':

    # make the parser
    parser = ArgumentParser(prog='AoC Function Timing',
                            description='This script searches through your folder and times specified functions.')

    # add some arguments
    parser.add_argument('-m', '--module', default='Solution', help='Substring to select modules. Case sensitive.')
    parser.add_argument('-f', '--functions', default=('main1', 'main2'), type=str, nargs='+',
                        help='Exact names of functions we want to test.')
    parser.add_argument('-ms', '--measurements', type=int, default=5,
                        help='Measurements. The amount of runs is: functions*measurements*repetitions.')
    parser.add_argument('-rs', '--repetitions', type=int, default=10, help='Repetitions per measurement.')
    main(parser.parse_args())
