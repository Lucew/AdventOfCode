from collections import Counter, defaultdict, deque
from heapq import heappop, heappush, heapify
from functools import reduce
from bisect import bisect_left, bisect_right


def read_input(path: str = 'input.txt'):
    inputs = dict()
    with open(path) as filet:
        for line in filet.readlines():

            # get the line
            line = line.rstrip()

            # get the valve name
            name = line.split(' ')[1]

            # get the flow rate
            flow = int(line.split(' ')[4].split('=')[1][:-1])

            # get the next elements
            next_elements = line.split('valve')[1].replace('s ', '').replace(' ', '').split(',')

            # put the information into the dict
            inputs[name] = [flow, tuple(next_elements)]
    return inputs


def get_shortest_path(start, end, graph):

    # make bfs for the shortest path, as all path costs are equal
    queue = deque([(start, 0)])
    cost = defaultdict(lambda: float('inf'))
    while queue:

        # pop the current node
        position, steps = queue.popleft()

        # check whether we are at the target
        if position == end:
            break

        # check whether we have a higher cost of coming here
        if steps > cost[position]:
            continue

        # go through all neighbours and append the target
        for neighbour in graph[position][1]:

            # compute the new steps
            nsteps = steps + 1
            if nsteps < cost[neighbour]:

                # update the costs
                cost[neighbour] = nsteps

                # append to the queue
                queue.append((neighbour, nsteps))

    # return the cost of travelling
    return cost[end]


def get_worthy_valves(inputs: dict):
    non_zero = {name for name, value in inputs.items() if value[0] > 0}
    non_zero.add('AA')
    return non_zero


def get_shortest_connections(worthy_valves: set, graph: dict):
    # get the shortest path
    shortest_path = defaultdict(dict)

    # get the shortest path between 'AA' and any of the non zero elements
    # as well as the shortest path between each of those including their costs
    non_zero_list = list(worthy_valves)
    for idx, start in enumerate(non_zero_list):
        for end in non_zero_list[idx + 1:]:
            # get the shortest path
            path_cost = get_shortest_path(start, end, graph)

            # fill in the information
            shortest_path[start][end] = path_cost
            shortest_path[end][start] = path_cost
    return shortest_path


def main1():
    # parse the input
    inputs = read_input()

    # get all the valves that we should visit
    non_zero = get_worthy_valves(inputs)

    # get the shortest path between worthy valves
    shortest_path = get_shortest_connections(non_zero, inputs)

    # traverse our valves in bfs fashion
    queue = deque([('AA', 0, 30, set())])
    result = 0
    while queue:

        # pop the most recent node
        position, accumulated_flow, time, visited = queue.popleft()

        # get our neighbours that we can reach in time
        neighbours = [neighbor for neighbor in shortest_path[position]
                      if neighbor not in visited and shortest_path[position][neighbor] < time]

        # if we don't have neighbours left, we cann update the result
        if not neighbours:
            result = max(result, accumulated_flow)
            continue

        # append the neighbours
        for neighbor in neighbours:
            # get the new flow
            new_flow = (time - shortest_path[position][neighbor] - 1)*inputs[neighbor][0]

            # make the new set
            new_set = visited | {neighbor}
            queue.append((neighbor, accumulated_flow + new_flow, time-shortest_path[position][neighbor] - 1, new_set))
    print(f'The result for solution 1 is: {result}')


# make a greedy estimation of what is still possible
def upper_bound(time, graph):
    # open all valves at the same time
    return sum(time*value[0] for value in graph.values())


def main2():

    # parse the input
    inputs = read_input()

    # get all the valves that we should visit
    non_zero = get_worthy_valves(inputs)

    # get the shortest path between worthy valves
    shortest_path = get_shortest_connections(non_zero, inputs)

    # make a cache
    cache = defaultdict(lambda: -1)

    # traverse our valves in bfs fashion
    queue = [(0, (('AA', 26), ('AA', 26)), set())]
    result = 0
    counter = 0
    while queue:

        # increase the counter
        counter += 1

        # do something all 100_000 steps
        if counter % 100_000 == 0:

            # clean the queue
            queue = [ele for ele in queue if ele[0] - upper_bound(max(actor[1] for actor in ele[1]), inputs) < result]

            # make heap again
            heapify(queue)

            # print the result
            print(counter/1_000_000, 'M', result)

        # pop the most recent node
        # print(queue)
        accumulated_flow, actors, visited = heappop(queue)

        # find the actor with the most time left
        max_idx = 0
        max_time = actors[0][1]
        for idx, (position, time) in enumerate(actors):
            if time > max_time:
                max_idx = idx
                max_time = time

        # get the time and position for that actor
        time = max_time
        position = actors[max_idx][0]

        # check whether our reachable flow is to low
        if accumulated_flow - upper_bound(time, inputs) > result:
            continue

        # make a neighbour generator
        neighbours = (neighbor for neighbor in shortest_path[position]
                      if neighbor not in visited and shortest_path[position][neighbor] < time)

        # append the neighbours
        for neighbor in neighbours:
            # get the new flow
            new_flow = accumulated_flow - (time - shortest_path[position][neighbor] - 1) * inputs[neighbor][0]

            # make the new set
            new_set = visited | {neighbor}

            # compute the new time
            new_time = time-shortest_path[position][neighbor] - 1

            # check whether our reachable flow is to low
            if new_flow - upper_bound(time, inputs) > result:
                continue

            # update the flow
            if new_flow < result:
                result = new_flow

            # make the new actors
            new_actors = tuple(actor if idx != max_idx else (neighbor, new_time) for idx, actor in enumerate(actors))
            heappush(queue, (new_flow, new_actors, new_set))

    print(f'The result for solution 2 is: {result}')


if __name__ == '__main__':
    main1()
    main2()
