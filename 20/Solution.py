from collections import Counter, defaultdict
from heapq import heappop, heappush, heappushpop
from functools import reduce
from bisect import bisect_left, bisect_right


class Node:

    def __init__(self, value, cycle_length: int, previous_node: 'Node' = None, next_node: 'Node' = None):
        self.val = value
        self.prev = previous_node
        self.next = next_node
        self.moved = False
        self.cycle = cycle_length

    def move(self):

        # detach ourselves and stitch the list back together
        self.prev.next = self.next
        self.next.prev = self.prev

        # check whether we are positive or negative
        if self.val > 0:

            # find our next and previous
            for _ in range(self.val % (self.cycle - 1)):
                self.next = self.next.next
                self.prev = self.prev.next

        elif self.val < 0:

            # find our next and previous
            for _ in range(abs(self.val) % (self.cycle - 1)):
                self.next = self.prev
                self.prev = self.prev.prev

        # cut the chain at this point and insert ourselves
        self.prev.next = self
        self.next.prev = self

        # set our value to moved
        self.moved = True

    def get_element(self, n):
        node = self
        for _ in range(n % self.cycle):
            node = node.next
        return node.val

    def __str__(self):

        result = []
        pointer = self
        for _ in range(self.cycle):
            result.append(pointer.val)
            pointer = pointer.next

        return " -> ".join(str(val) for val in result)


def read_input(path: str = 'input.txt'):
    inputs = []
    with open(path) as filet:
        for line in filet.readlines():
            line = line.rstrip()
            inputs.append(int(line))
    return inputs


def create_linked_list(values: list[int], multiplier: int = 1):

    # keep a reference to the first object
    first = Node(values[0]*multiplier, len(values))

    # keep a reference to the zero element
    zero = first

    # keep a list of pointers, so we can iterate through them
    nodes = [first]

    # go through the list and create nodes
    for value in values[1:]:
        new_node = Node(value*multiplier, len(values), nodes[-1])
        nodes[-1].next = new_node
        nodes.append(new_node)
        if value == 0:
            zero = new_node

    # make a full cycle (attach the end to the beginning)
    nodes[-1].next = nodes[0]
    nodes[0].prev = nodes[-1]

    return nodes, zero


def main1():

    # read the input
    inputs = read_input()

    # make the linked list
    llist, zero = create_linked_list(inputs)

    # make the rotation for every node in the list
    for node in llist:
        node.move()

    # get the elements and sum them
    result = sum(zero.get_element(idx) for idx in [1000, 2000, 3000])
    print(f'The result for solution 1 is: {result}')


def main2():

    # read the input
    inputs = read_input()

    # make the linked list
    llist, zero = create_linked_list(inputs, multiplier=811589153)

    # make the rotation for every node in the list
    for _ in range(10):
        for node in llist:
            node.move()

    # get the elements and sum them
    result = sum(zero.get_element(idx) for idx in [1000, 2000, 3000])
    print(f'The result for solution 2 is: {result}')


if __name__ == '__main__':
    main1()
    main2()
