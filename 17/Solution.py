import time
import functools as ft


def read_input(path: str = 'input.txt'):
    with open(path) as filet:
        pattern = filet.read().rstrip()
    return pattern


def pattern_generator(pattern: str):
    idx = 0
    n = len(pattern)
    while True:
        yield pattern[idx]
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

    def _spawn_rock(self):
        self.falling_rock = Rock(next(self.rock_type_generator), self.highest+4, 2)

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

    def cave_repeats(self):

        # make the cave string
        cave_string = self._make_string(print_falling_rock=False, print_ground=False)

        # get the number of lines
        line_numbers = len(cave_string) // (self.width + 3)

        # get the index of the half
        half = line_numbers // 2

        # check whether a pattern repeats
        return line_numbers % 2 == 0 and cave_string[:half] == cave_string[half:]

    def step(self):

        # get the current wind
        wind = next(self.wind_generator)

        # boolean whether we placed a rock in this step
        placed = False

        # get the direction
        dx, dy = self._get_direction_from_string(wind)

        # check if we have a falling rock or spawn one
        if not self.falling_rock:
            self._spawn_rock()

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


def longest_repeated_substring(pattern):
    # https: // www.geeksforgeeks.org / longest - repeating - and -non - overlapping - substring /
    n = len(pattern)
    dp = [[0 for _ in range(n + 1)] for _ in range(n + 1)]
    res_length = 0  # To store length of result

    # building table in bottom-up manner
    index = 0
    for i in range(1, n + 1):
        for j in range(i + 1, n + 1):

            # (j-i) > dp[i-1][j-1] to remove overlapping
            if pattern[i - 1] == pattern[j - 1] and dp[i - 1][j - 1] < (j - i):
                dp[i][j] = dp[i - 1][j - 1] + 1

                # updating maximum length of the substring and updating the finishing
                # index of the suffix
                if dp[i][j] > res_length:
                    res_length = dp[i][j]
                    index = max(i, index)

            else:
                dp[i][j] = 0

    # If we have non-empty result, then insert all characters from first character to
    # last character of string
    res = pattern[index - res_length:index]
    return res, index


def string_is_repeated(pattern: str):
    # https://www.geeksforgeeks.org/python-check-if-string-repeats-itself/
    position = (pattern + pattern).find(pattern, 1, -1)
    return position != -1, pattern[:position]


def main2(target=1_000_000_000_000):
    # read the jet pattern
    pattern = read_input()

    # make the cave
    cave = Cave(pattern)

    # amount of rocks we want to let fall
    rocks = 6000

    # initialize an array of height growth
    heights = []
    was_plattform = []

    # make several steps
    t = time.time()
    prev_height = -1
    while cave.rock_counter < rocks:
        if cave.step():
            heights.append(cave.highest - prev_height)
            prev_height = cave.highest

            # check if we occupied a complete row
            if cave.highest_row_blocked():
                was_plattform.append((cave.rock_counter, cave.highest))
    elapsed = time.time() - t
    print(f'{rocks} rocks took {elapsed:0.4f} seconds. '
          f'For {target} rocks it will take: {target * elapsed / rocks / 3600 / 24:0.4f} days.')
    print(f'The height was: {cave.highest}')

    """# convert heights to string
    heights_string = "".join(str(height) for height in heights)

    # find the longest repeated substring in heights
    sub, first_occurrence = longest_repeated_substring(heights_string)
    if not sub:
        print('Did not find repeated subpattern')

    # check whether this one is a repetition of itself
    is_repeated, base = string_is_repeated(sub)
    if not is_repeated:
        print('Our subpattern needs to be repeated.')

    # get the height up until this point (we do not need the offset that, as we would normally start at -1)
    until_height = sum(heights[:first_occurrence])
    repeated_height = sum(heights[first_occurrence:first_occurrence+len(base)])

    # compute the height of our testing immediately
    test_rocks = target - first_occurrence
    test_height = until_height
    test_height += (test_rocks // len(base))*repeated_height
    test_height += sum(heights[first_occurrence+1: first_occurrence + (test_rocks % len(base))])"""

    # compute the height difference per platform
    differences = [(rocks - was_plattform[idx][0], height - was_plattform[idx][1]) for idx, (rocks, height) in enumerate(was_plattform[1:])]
    first_height = sum(heights[:was_plattform[0][0]])
    test_rocks = target - was_plattform[0][0]
    first_height += (test_rocks // differences[0][0])*differences[0][1]
    first_height += sum(heights[was_plattform[0][0]:was_plattform[0][0] + test_rocks % differences[0][0]])

    print(f'The result for solution 1 is: {first_height-1}')


if __name__ == '__main__':
    main1()
    main2()
