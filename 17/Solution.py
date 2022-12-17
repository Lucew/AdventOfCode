import time
import collections


def read_input(path: str = 'input.txt'):
    with open(path) as filet:
        pattern = filet.read().rstrip()
    return pattern


def pattern_generator(pattern: str):
    idx = 0
    n = len(pattern)
    while True:
        yield pattern[idx], idx
        idx = (idx + 1) % n


class Rock:

    def __init__(self, rock_type: str, y_offset: int, x_offset: int = 2):

        # make the initialization depending on the type of rock
        if rock_type == '-':
            self.positions = [[x, y_offset] for x in range(x_offset, x_offset+4)]
        elif rock_type == '+':
            self.positions = [[x_offset+1, y_offset+2], [x_offset, y_offset+1], [x_offset+1, y_offset+1],
                              [x_offset+2, y_offset+1], [x_offset+1, y_offset]]
        elif rock_type == 'L':
            self.positions = [[x_offset + 2, y_offset + 2], [x_offset+2, y_offset + 1]] \
                             + [[x, y_offset] for x in range(x_offset, x_offset+3)]
        elif rock_type == 'I':
            self.positions = [[x_offset, y] for y in range(y_offset+3, y_offset-1, -1)]
        elif rock_type == 'o':
            self.positions = [[x_offset, y_offset+1], [x_offset+1, y_offset+1], [x_offset, y_offset],
                              [x_offset+1, y_offset]]
        else:
            raise NotImplementedError(f'Tried to spawn rock of type: {rock_type}')

        # save the rock type
        self.type = rock_type

    def get_positions(self) -> list[tuple[int]]:
        return [tuple(position) for position in self.positions]

    def move(self, dx, dy):
        for coordinates in self.positions:
            coordinates[0] += dx
            coordinates[1] += dy


class Cave:
    def __init__(self,  wind_pattern: str, rock_pattern: str = '-+LIo', width=7):
        self.width = width
        self.occupied = set()
        self.highest = -1
        self.falling_rock = None
        self.wind_generator = pattern_generator(wind_pattern)
        self.rock_type_generator = pattern_generator(rock_pattern)
        self.rock_counter = 0
        self.state_cache = collections.defaultdict(list)

    def _spawn_rock(self):
        self.falling_rock = Rock(next(self.rock_type_generator)[0], self.highest+4, 2)

    def _place_rock(self, rock: Rock):
        """get the positions of the rock
        pieces and check them whether
        our pile grew"""

        # get rock positions
        positions = rock.get_positions()

        # update our cave height
        self.highest = max(self.highest, *[position[1] for position in positions])

        # update the occupied rocks
        self.occupied.update(positions)

        # increase the rock counter
        self.rock_counter += 1

        # despawn the rock
        self.falling_rock = None

    def _check_rock_collision(self, rock: Rock):
        return any(self._check_collision(*position) for position in rock.get_positions())

    def _check_collision(self, x: int, y: int):
        return x < 0 or x > self.width - 1 or y < 0 or (x, y) in self.occupied

    def highest_row_blocked(self):
        # check whether a complete row is blocked (we could clean the occupied dict then)
        return all((x, self.highest) in self.occupied for x in range(0, self.width))

    def detect_cycles(self) -> tuple[tuple[int, int], int, int]:
        # check the state cache for repeated states
        cycles = []

        # find the cycle
        for value in self.state_cache.values():
            if len(value) > 1:
                cycles = value
                break

        # return none if not correct
        if not cycles:
            return (-1, -1), -1, -1

        # get the cycle modulo and the height increase as each element in self.state_cache.values()
        # is : (rock_counter, current_highest_resting_rock)
        # also return the begin of the cycle and the height at this point
        return cycles[0], cycles[1][0] - cycles[0][0], cycles[1][1] - cycles[0][1]

    @staticmethod
    def _get_direction_from_string(direction: str, inverse: bool = False):

        # translate the direction if inverse
        if inverse:
            if direction == '>':
                direction = '<'
            elif direction == '<':
                direction = '>'
            elif direction == 'v':
                direction = '^'
            elif direction == '^':
                direction = 'v'
            else:
                raise NotImplementedError

        # go through the different cases
        if direction == '>':
            dx = 1
            dy = 0
        elif direction == '<':
            dx = -1
            dy = 0
        elif direction == 'v':
            dx = 0
            dy = -1
        elif direction == '^':
            dx = 0
            dy = 1
        else:
            raise NotImplementedError
        return dx, dy

    def _make_string(self, print_falling_rock: bool = True, print_ground: bool = True):

        # print the cave row by row starting from the bottom
        if print_ground:
            cave_str = ["".join('+' if idx == -1 or idx == self.width else '-' for idx in range(-1, self.width + 1))]
        else:
            cave_str = []

        # copy the occupied set in order to add the falling rock
        occupied = self.occupied.copy()
        highest = self.highest
        if self.falling_rock and print_falling_rock:
            # get the positions
            positions = self.falling_rock.get_positions()

            # add the positions to the dict
            occupied.update(positions)

            # update the highest
            highest = max(*[position[1] for position in positions])

        # go through the rows with placed rocks
        for y in range(0, highest + 1):
            cave_row = "".join('#' if (x, y) in occupied else '.' for x in range(0, self.width))
            cave_str.append(f'|{cave_row}|\n')

        return "".join(reversed(cave_str))

    def __str__(self):
        return self._make_string()

    def _get_surface_profile(self):
        # go through each column and find the first element that is blocked coming from top
        # this gives us a surface profile that determines a repeated state
        profile = []
        for x in range(0, self.width):
            y = self.highest
            while not self._check_collision(x, y):
                y -= 1
            profile.append(self.highest - y)
        return tuple(profile)

    def step(self):

        # get the current wind
        wind, wind_idx = next(self.wind_generator)

        # boolean whether we placed a rock in this step
        placed = False

        # check if we have a falling rock or spawn one into the cave
        if not self.falling_rock:

            # spawn the rock
            self._spawn_rock()

            # create a unique key of the state for cycle detection
            key = (*self._get_surface_profile(), wind_idx, self.falling_rock.type)

            # append the current rock counter to the state cache
            self.state_cache[key].append((self.rock_counter, self.highest))

        # apply the wind to the rock
        self.falling_rock.move(*self._get_direction_from_string(wind))

        # check if the rock collided
        if self._check_rock_collision(self.falling_rock):

            # reverse the movement
            self.falling_rock.move(*self._get_direction_from_string(wind, inverse=True))

        # apply the falling motion
        self.falling_rock.move(*self._get_direction_from_string('v'))

        # check whether the rock collided in this move
        if self._check_rock_collision(self.falling_rock):

            # reverse the movement
            self.falling_rock.move(*self._get_direction_from_string('v', inverse=True))

            # place the rock into the cave as resting
            self._place_rock(self.falling_rock)

            # set placing boolean to true
            placed = True

        return placed


def main1(rocks=2022):

    # read the jet pattern
    pattern = read_input()

    # make the cave
    cave = Cave(pattern)

    # make several steps
    while cave.rock_counter < rocks:
        cave.step()
    print(f'The result for solution 1 is: {cave.highest+1}')


def main2(target=1_000_000_000_000):
    # read the jet pattern
    pattern = read_input()

    # make the cave
    cave = Cave(pattern)

    # amount of rocks we want to let fall
    rocks = 2800

    # make several steps
    t = time.time()
    heights = []
    while cave.rock_counter < rocks:
        if cave.step():
            heights.append(cave.highest)
    elapsed = time.time() - t
    print(f'{rocks} rocks took {elapsed:0.4f} seconds. '
          f'For {target} rocks it will take: {target * elapsed / rocks / 3600 / 24:0.4f} days.')
    print(f'The height was: {cave.highest}')

    # detect cycles
    (cycle_start, highest_start), cycle_size, height_per_cycle = cave.detect_cycles()
    assert cycle_size != -1, 'Did not find a cycle.'

    # get the height before the first circle
    result = heights[cycle_start]

    # check how often the cycle fits into the target (minus the rocks before the cycle)
    cycle_number, rest = divmod(target-cycle_start, cycle_size)

    # add up the result
    result += cycle_number*height_per_cycle + (heights[cycle_start + rest] - heights[cycle_start])
    print(f'The result for solution 2 is: {result}')


if __name__ == '__main__':
    main1()
    main2()
