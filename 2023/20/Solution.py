import collections
from collections import Counter, defaultdict
from heapq import heappop, heappush, heappushpop
from functools import reduce
from bisect import bisect_left, bisect_right, bisect
import math


def read_input(path: str = 'input.txt'):
    inputs = []
    with open(path) as filet:
        for line in filet.readlines():
            line = line.rstrip()

            # get the name and the destinations
            name, destinations = line.split(" -> ")

            # check whether it is the broadcaster
            if name == "broadcaster":
                typed = name
            else:
                typed = name[0]
                name = name[1:]
            destinations = destinations.split(", ")
            inputs.append((typed, name, destinations))
    return inputs


class Element:

    def __init__(self, connections: list[str], name: str, debug: bool):

        # save the destinations
        self.connections = connections

        # save our own name
        self.name = name

        # save a debug variable
        self.debug = debug

    def receive(self, pulse: bool, origin: str) -> list[(str, bool, str)]:
        pass

    def send(self, pulse: bool, in_pulse: bool, origin: str) -> list[(str, bool, str)]:
        self.debug_message(in_pulse, pulse, origin)
        return [(name, pulse, self.name) for name in self.connections]

    @staticmethod
    def p2str(pulse: bool):
        return 'HIGH' if pulse else 'LOW'

    def debug_message(self, in_pulse: bool, out_pulse: bool, origin: str):
        # make debug print
        if self.debug:
            print(f"[{self.name}] received {self.p2str(in_pulse)} from [{origin}]. -> {self.p2str(out_pulse)}.")


class Broadcaster(Element):

    def __init__(self, connections: list[str], name: str, debug: bool):
        super().__init__(connections, name, debug)

    def receive(self, pulse: bool, origin: str) -> list[(str, bool, str)]:

        # send pulses to all the appliances
        return self.send(pulse, pulse, origin)


class FlipFlop(Element):

    def __init__(self, connections: list[str], name: str, debug: bool):
        super().__init__(connections, name, debug)

        # make a variable to save the status
        self.on = False

    def receive(self, pulse: bool, origin: str) -> list[(str, bool, str)]:

        # check whether we received a low pulse (toggle)
        if not pulse:
            self.on = not self.on
            return self.send(self.on, pulse, origin)
        return []


class Conjunction(Element):

    def __init__(self, connections: list[str], name: str, debug: bool):
        super().__init__(connections, name, debug)

        # make a list that remembers the status (but it has to be initialized)
        self.received = None
        self.high_count = 0

    def initialize(self, inbound_connections: list[str]):
        self.received = {name: False for name in inbound_connections}

    def receive(self, pulse: bool, origin: str) -> list[(str, bool, str)]:

        # check whether we initialized all ingoing connections
        if self.received is None:
            raise ValueError(f"Conjunction [{self.name}] was never initialized.")

        # update our memory and the counter
        curr_status = self.received[origin]
        if curr_status != pulse:
            if pulse:
                self.high_count += 1
            else:
                self.high_count -= 1
        self.received[origin] = pulse

        # send high pulse if high count equals the length of inbound connections
        out = not self.high_count == len(self.received)

        # send in to all other connections
        return self.send(out, pulse, origin)


def factory(typed, name, destinations, debug=False):
    if typed == "%":
        return FlipFlop(destinations, name, debug)
    elif typed == "&":
        return Conjunction(destinations, name, debug)
    elif typed == "broadcaster":
        return Broadcaster(destinations, name, debug)
    else:
        raise ValueError(f"Type {typed} not known to the factory.")


def make_graph():

    # get the graph from the input
    graph = {name: factory(typed, name, destinations, False) for typed, name, destinations in read_input()}

    # find all the inbound connections of conjunctions
    inbound = collections.defaultdict(list)
    for element in graph.values():
        for destination in element.connections:
            if destination not in graph or not isinstance(graph[destination], Conjunction):
                continue
            inbound[destination].append(element.name)

    # initialize all conjunctions
    for key, values in inbound.items():
        graph[key].initialize(values)
    return graph


def make_cycle(graph: dict[str:Element], low: int, high: int, interest: dict[str:list[int]] = None, btx: int = 0):

    # check whether we have no interest
    if interest is None:
        interest = dict()

    # make a queue for the cycle
    queue = collections.deque([("broadcaster", False, "Button")])

    # go until the queue is empty and count the pulses (including the one from the button)
    counter = [low, high]
    while queue:

        # get the current pulse
        name, pulse, origin = queue.popleft()

        # make the debug print
        # print(f"{origin} -{Element.p2str(pulse)}-> {name}")

        # update the interesting elements
        if origin in interest:
            interest[origin][0] += 1
            if pulse:
                interest[origin].append((interest[origin][0], btx))

        # add to the counter
        counter[int(pulse)] += 1

        # make the push
        if name not in graph:
            pass
            # print(f"{name} received {Element.p2str(pulse)} from {origin} but is not graph.")
        else:
            queue.extend(graph[name].receive(pulse, origin))
    return counter[0], counter[1]


def main1():

    # get the graph with initialized elements
    graph = make_graph()

    # make cycles
    all_low = 0
    all_high = 0
    for _ in range(1000):
        all_low, all_high = make_cycle(graph, all_low, all_high)
    print(f'The result for solution 1 is: {all_high*all_low}')


def main2():
    # get the graph with initialized elements
    graph = make_graph()

    # make a list of elements that are of interest to us
    interest = {"lz": [0], "kh": [0], "tg": [0], "hn": [0]}

    # make cycles
    for idx in range(15000):
        _ = make_cycle(graph, 0, 0, interest, idx)

    # check for cycle length
    cycles = []
    for ele, values in interest.items():
        diffs = [a[1]-b[1] for a, b in zip(values[2:], values[1:-1])]
        cycles.append(diffs[-1])
    print(f'The result for solution 1 is: {math.lcm(*cycles)}')


if __name__ == '__main__':
    main1()
    main2()
