import collections
import time
from functools import lru_cache


def read_input(path: str = 'input.txt'):
    inputs = []
    with open(path) as filet:
        for idx, line in enumerate(filet.readlines()):

            # read the line
            line = line.rstrip()

            # divide into instructions and blueprint number
            line = line.split(': ')

            # get and check the blueprint number
            blueprint = int(line[0].split(' ')[-1])
            assert blueprint == idx + 1, 'Blueprint number is not as expected.'

            # get the robot costs
            robots = line[1].split('. ')

            robot_materials = []
            # go through each of them and check whether they are as expected
            for idx, robot in enumerate(robots):

                # split the line further
                robot = robot.split(' ')

                # check for expected stuff
                if robot[1] == 'ore':

                    # check that it is the first robot
                    assert idx == 0, 'The ore robot is not the first.'

                    # check that it requires ore
                    assert robot[5] == 'ore', 'The ore robot is not as expected.'

                    # make the materials tuple
                    robot_materials.append((int(robot[4]), 0, 0, 0))

                elif robot[1] == 'clay':

                    # check that it is the first robot
                    assert idx == 1, 'The clay robot is not the second.'

                    # check that it requires ore
                    assert robot[5] == 'ore', 'The clay robot is not as expected.'

                    # make the materials tuple
                    robot_materials.append((int(robot[4]), 0, 0, 0))

                elif robot[1] == 'obsidian':

                    # check that it is the first robot
                    assert idx == 2, 'The obsidian robot is not the third.'

                    # check that it requires ore
                    assert robot[5] == 'ore' and robot[8] == 'clay', 'The obsidian robot is not as expected.'

                    # make the materials tuple
                    robot_materials.append((int(robot[4]), int(robot[7]), 0, 0))

                elif robot[1] == 'geode':

                    # check that it is the first robot
                    assert idx == 3, 'The geode robot is not the fourth.'

                    # check that it requires ore
                    assert robot[5] == 'ore' and robot[8] == 'obsidian.', 'The geode robot is not as expected.'

                    # make the materials tuple
                    robot_materials.append((int(robot[4]), 0, int(robot[7]), 0))
            inputs.append(robot_materials)
    return inputs


def optimize_factory(costs: list[tuple[int, int, int, int]], time_horizon: int, debug=False) -> tuple[int, int]:
    # first idea is to build some kind of simulation for a factory on how many geodes we can break with it.
    #
    # I think a simulation per minute is appropriate. We could do this using BFS, so we have everything in a loop.
    # Our target is the amount of geodes we can crack.
    #
    # Maybe we should do some kind of topological sort in order to keep track of which robots we can build?
    #
    # Other than that we need to keep track of:
    #
    # 1) Which Materials we have after n minutes
    # 2) How many Materials we produce every minute
    # 3) Which robots we can build with this
    # 4) How many geodes we cracked

    # 1) and 2) from above will be our search space, as we can construct different robots and any minute
    # 3) is a function that tells us which paths we can go
    # 4) is the thing we want to maximize and also keep track of

    # get the maximum amount of materials used for any robot, so we don't make more robots than this cost
    # as we would not be able to get rid of it
    max_materials_necessary = [max(cost[idx] for cost in costs) for idx in range(len(costs))]
    max_materials_necessary[3] = float('inf')  # we need as many geodes opened as possible

    # initialize the bfs with some kind of queue that consists of tuples
    # (time_left, materials(ore, clay, obsidian, geodes), robots(ore, clay, obsidian, geodes))
    queue = collections.deque([(time_horizon, (0, 0, 0, 0), (1, 0, 0, 0))])
    # the order of things happening will be:
    #
    # a) keep track of maximum geodes
    # b) check which robots we can build
    # c) for every path update the materials
    # d) for every path append (build) the robots and updated materials to the queue
    result = 0
    counter = 0
    start_time = time.time()
    state_cache = collections.defaultdict(lambda: -1)
    while queue:

        # pop from the queue (from the rightmost as this might be the ones having geode robots, as I append these
        # last!)
        time_left, materials, robots = queue.pop()

        # increase the counter
        counter += 1
        if counter % 500_000 == 0 and debug:
            print(time_left, materials, robots, len(queue))
            print(f'{counter / 1_000_000:0.1f} M. Result: {result}. Elapsed time: {time.time() - start_time} s.')
            print()

        # keep track of maximum geodes
        result = max(result, materials[3])

        # think about whether we can reach the goal if we produce a geode roboter in every step now (upper bound) ------
        upper_bound_geodes = ((time_left + robots[3]) * (time_left + robots[3] + 1)) // 2 \
                             - (robots[3] * (robots[3] + 1)) // 2 \
                             + materials[3]
        if upper_bound_geodes <= result:
            continue

        # update the cache and see whether we already found a better path ----------------------------------------------
        # make and update the cache (for the cache it does not matter how much geode a state has
        # only how much it can produce as no one can use the geode to make any more robots)
        key = (time_left, materials[:3], robots)
        if state_cache[key] >= materials[3]:
            continue
        else:
            state_cache[key] = materials[3]

        # check whether our time is up
        if not time_left:
            continue

        # now think about whether it is useful to wait for any materials -----------------------------------------------

        # check whether we wait for any robot because we do not have the material yet
        # also: we only need to wait for that material if we have a robot for it, otherwise this specific material
        # will not be growing even if we wait for it
        should_wait = any(material < max_material and robot
                          for material, max_material, robot in zip(materials, max_materials_necessary, robots))

        # if we are still shure we should wait, then we append a waiting state
        if should_wait:
            new_materials = tuple(material + robot for material, robot in zip(materials, robots))
            new_robots = robots[:]

            # append to the queue
            queue.append((time_left - 1, new_materials, new_robots))

        # build the robots ---------------------------------------------------------------------------------------------
        for idx, cost in enumerate(costs):

            # only build a robot if:
            #
            # a) We need more of that robot as we do not produce enough material every step to produce any robot
            # b) We have all the material we need for that robot
            if max_materials_necessary[idx] > robots[idx] \
                    and all(material >= prize for material, prize in zip(materials, cost)):
                # update the materials we will have in the next step
                new_materials = tuple(
                    material + robot - prize for material, robot, prize in zip(materials, robots, cost))

                # update the robots we will have
                new_robots = tuple(robot + 1 if rx == idx else robot for rx, robot in enumerate(robots))

                # append to the queue
                queue.append((time_left - 1, new_materials, new_robots))
    return result, counter


def main1(time_horizon=24):

    # get the inputs (we now know how much each robot costs)
    inputs = read_input()

    # go through each factory (and time it)
    result = 0
    for idx, factory in enumerate(inputs, 1):
        start_time = time.time()
        best_geodes, steps = optimize_factory(factory, time_horizon)
        print(f'Factory {idx} for {time_horizon} minutes optimization took {time.time() - start_time: 0.2f} s '
              f'and {steps/1_000_000:0.3f} M steps.')
        result += best_geodes*idx

    print(f'The result for solution 1 is: {result}')


def main2(time_horizon=32):

    # get the inputs (we now know how much each robot costs)
    inputs = read_input()

    # go through each factory
    result = 1
    for idx, factory in enumerate(inputs[:3], 1):
        start_time = time.time()
        best_geodes, steps = optimize_factory(factory, time_horizon)
        print(best_geodes)
        print(f'Factory {idx} for {time_horizon} minutes optimization took {time.time() - start_time: 0.2f} s '
              f'and {steps/1_000_000:0.3f} M steps.')
        result *= best_geodes

    print(f'The result for solution 1 is: {result}')


if __name__ == '__main__':
    # main1()
    main2()
