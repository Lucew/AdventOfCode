import collections
from collections import Counter, defaultdict
from heapq import heappop, heappush, heappushpop
from functools import reduce
from bisect import bisect_left, bisect_right, bisect


def read_input(path: str = 'input.txt'):
    inputs = []
    with open(path) as filet:
        for line in filet.readlines():
            line = line.rstrip()
            inputs.append(line)
    return inputs


def function_translator(x: int, function_triple: tuple):

    # check the triple
    assert len(function_triple) == 3, f"Something is wrong with function definition: {function_triple}."

    # unpack the tuple
    signature, threshold, return_val = function_triple
    if signature == "<" and x < threshold:
        return return_val
    elif signature == ">" and x > threshold:
        return return_val
    elif signature != ">" and signature != "<":
        raise ValueError(f"Signature {signature} not kown.")
    return -1


def get_workflows_items():

    # get the lines
    lines = read_input()

    # get objects and workflows
    workflows = dict()
    pdx = 0
    for idx, line in enumerate(lines):

        # check whether we reached parts
        if not line:
            pdx = idx
            break

        # parse the workflow
        name, workflow = line[:-1].split("{")
        workflow = workflow.split(",")

        # create the workflow conditions
        workflows[name] = []
        for condition in workflow[:-1]:
            # get function and return value
            function, return_val = condition.split(":")

            # parse the condition into a function
            variable = function[0]
            number = int(function[2:])
            # print(variable, number, return_val)

            # make it into a function
            workflows[name].append((variable, function[1], number, return_val))

        # create the default
        workflows[name].append((workflow[-1],))

    # print(workflows)
    # check that we reached the elements
    assert pdx > 0, "We did not reach the items."
    items = []
    for item in lines[pdx + 1:]:
        # get the items and their condition
        items.append({ele.split("=")[0]: int(ele.split("=")[1]) for ele in item[1:-1].split(",")})
    return workflows, items


def main1():

    # get the input
    workflows, items = get_workflows_items()

    # go through the items and check whether they are rejected or accepted
    queue = [(idx, "in") for idx in range(len(items))]
    result = 0
    while queue:

        # get the current item index and workflow position
        idx, workflow = queue.pop()

        # get the actual item
        item = items[idx]

        # get the workflow
        workflow = workflows[workflow]

        # go through the workflow keys and make checks
        next_workflow = ""
        for info in workflow:
            # check whether we reached the default key
            if len(info) == 1:
                next_workflow = info[0]
                break

            # unpack the quadruple
            key, *ftriple = info

            # check whether the element fits
            return_val = function_translator(item[key], ftriple)
            if return_val != -1:
                next_workflow = return_val
                break

        # check if we need to get further
        # print(next_workflow, item, workflow)
        if next_workflow == "A":
            result += sum(item.values())
        elif next_workflow and next_workflow != "R":
            queue.append((idx, next_workflow))

    print(f'The result for solution 1 is: {result}')


def copy_item(item: dict[str:[int, int]]):
    return {key: [ele for ele in values] for key, values in item.items()}


def compute_volume(item: dict[str:[int, int]]):
    volume = 1
    for value in item.values():
        volume *= (value[1]-value[0]+1)
    return volume


def main2():

    # get the parsed input
    workflows, _ = get_workflows_items()

    # make some ranges that we can keep track of
    queue = [({"x": [1, 4000], "m": [1, 4000], "a": [1, 4000], "s": [1, 4000]}, "in")]
    result = 0
    while queue:

        # pop from the queue
        item, workflow_name = queue.pop()
        workflow = workflows[workflow_name]

        # go through the rules and check if the at least partially apply
        hit = False
        for key, signature, threshold, return_val in workflow[:-1]:

            # check if it applies
            if signature == "<" and item[key][0] < threshold:

                # check whether we need a second item
                if item[key][1] >= threshold:

                    # make a copy of the item
                    item2 = copy_item(item)

                    # adapt the threshold
                    item2[key][0] = threshold

                    # append to the stack
                    queue.append((item2, workflow_name))

                # change the interval of the second item
                item[key][1] = min(threshold-1, item[key][1])

                # mark a rule hit
                hit = True

            elif signature == ">" and item[key][1] > threshold:

                # check whether we need a second item
                if item[key][0] <= threshold:
                    # make a copy of the item
                    item2 = copy_item(item)

                    # adapt the threshold
                    item2[key][1] = threshold

                    # append to the stack
                    queue.append((item2, workflow_name))

                # change the interval of the second item
                item[key][0] = max(threshold + 1, item[key][0])

                # mark a rule hit
                hit = True

            elif signature != "<" and signature != ">":
                raise ValueError(f"Signature {signature} unknown.")

            # check whether we are rejected or accepted
            if hit and return_val == "A":
                result += compute_volume(item)
            elif hit and return_val == "R":
                pass
            elif hit:
                queue.append((item, return_val))

            # check whether we had a hit
            if hit:
                break

        # check if we need to apply default rule
        if not hit:

            # check whether we are rejected or accepted
            if workflow[-1][0] == "A":
                result += compute_volume(item)
            elif workflow[-1][0] == "R":
                pass
            else:
                queue.append((item, workflow[-1][0]))
    print(f'The result for solution 2 is: {result}')


if __name__ == '__main__':
    main1()
    main2()
