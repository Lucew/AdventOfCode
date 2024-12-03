from collections import defaultdict
import heapq
# https://www.reddit.com/r/adventofcode/comments/rmnozs/comment/hpyp72s/?utm_source=share&utm_medium=web3x&utm_name=web3xcss&utm_term=1&utm_content=share_button

# ENUMERATORS
E = 0
A = 1
B = 10
C = 100
D = 1000
enum2char = {0: "E", 1: "A", 10: "B", 100: "C", 1000: "D"}
enum2room = {1: 1, 10: 3, 100: 5, 1000: 7}

class Room:
    def __init__(self):
        # Type of room:
        #  A, B, C, D are the rooms
        #  E = hallway
        self.type = E # A B C D E
        self.pos = [E, E]
        self.s = len(self.pos)

    def is_complete(self):
        # Hallways shouldn't be checked if they are complete anyway
        if self.type == E:
            return True

        for crab in self.pos:
            if crab != self.type:
                return False

        return True

    def has_space(self):
        """Used on halways
        """
        if self.pos[0]:
            return False

        return True

    def is_empty(self):
        """Returns true if it is empty or if it is filled with correct type
        crabs. If it is a hallway only the first element is checked.
        """
        for i in range(self.s):
            # In case that the room is filled with the correct crabs,
            # we ignore them
            if self.pos[i] == self.type:
                continue

            if self.pos[i]:
                return False
        return True

    def get_next(self):
        # Return the next crab to move out. This should be called after
        # checking if it is complete or in case of hallway, get the next crab.
        # The i acts also as an offset for computing the number of steps.
        for i in range(self.s):
            if self.pos[i]:
                return self.pos[i], i

    def get_position(self):
        """Should be called after if it empty to get the correct index of the
        position.

        Returns the deepest level of move for current room. Can be used also
        for halways.
        """
        for i in range(self.s - 1, -1, -1):
            if not self.pos[i]:
                return i + 1

    def __eq__(self, other: 'Room'):
        for j in range(self.s):
            if self.pos[j] != other.pos[j]:
                return False
        return True

class State:
    def __init__(self, part_one=True):
        self.rooms = []
        if part_one:
            self.room_depths = 2
        else:
            self.room_depths = 4
        self.rooms_complete = 0

    def count_completed_rooms(self):
        """Not only do we count completed rooms, we favor those that have the
        expensive crabs already sorted in their correct room.
        """
        self.rooms_complete = 0
        for i in [1, 3, 5, 7]:
            if self.rooms[i].is_complete():
                self.rooms_complete += self.rooms[i].type

    def __lt__(self, other: 'State'):
        # For heapq
        # See who has more rooms complete
        # Favor rooms that have more expensive crabs already tucked.


        if self.rooms_complete < other.rooms_complete:
            return True

        return False

    def create_rooms(self):
        identifier = {1: A, 3:B, 5:C, 7:D}
        for i in range(9):
            room = Room()
            if i % 2 == 0:
                room.type = E
                if i == 0 or i == 8:
                    room.pos = [E, E]
                    room.s = 2
                else:
                    room.pos = [E]
                    room.s = 1
            else:
                room.type = identifier[i]
                room.pos = [identifier[i] for j in range(self.room_depths)]
                room.s = self.room_depths
            self.rooms.append(room)

    def is_complete(self):
        eq = True
        for i in [1, 3, 5, 7]:
            eq &= self.rooms[i].is_complete()

        return eq

    def __eq__(self, other: 'State'):
        """Easier is to call complete, but to compare states this can be used
        """

        eq = True
        for i in [1, 3, 5, 7]:
            eq &= self.rooms[i] == other.rooms[i]

        return eq

    def __hash__(self):
        """Create a hash in the following way:

        HALL - ROOM - HALL - ROOM -...
        """
        string = ""
        for room in self.rooms:
            for pos in room.pos:
                string += enum2char[pos]
        return hash(string)

    def __repr__(self):
        vis = "\n"
        vis += 13 * "#" + "\n"
        # Collect the hallways
        vis += "#"
        vis += enum2char[self.rooms[0].pos[1]]
        vis += enum2char[self.rooms[0].pos[0]]
        vis += " "
        for j in [2, 4, 6]:
            vis += "".join([enum2char[self.rooms[j].pos[_]] for _ in range(len(self.rooms[j].pos))])
            vis += " "
        vis += enum2char[self.rooms[8].pos[0]]
        vis += enum2char[self.rooms[8].pos[1]]
        vis += "#\n"

        first = True
        for i in range(self.room_depths):
            if first:
                vis += "###"
            else:
                vis += "  #"
            vis += "#".join([enum2char[self.rooms[j].pos[i]] for j in [1, 3, 5, 7]])

            if first:
                vis += "###\n"
                first = False
            else:
                vis += "#\n"
        vis += "  " + 9*"#" + "\n"
        return vis

def _deepcopy(state_obj: State):
    new_obj = State()
    new_obj.room_depths = state_obj.room_depths
    for i in range(len(state_obj.rooms)):
        room = Room()
        room.type = state_obj.rooms[i].type
        room.pos = state_obj.rooms[i].pos[:]
        room.s = state_obj.rooms[i].s
        new_obj.rooms.append(room)

    return new_obj

# Create states
part_one = 0

target_state = State(part_one=part_one)
target_state.create_rooms()

current_state = State(part_one=part_one)
current_state.create_rooms()

# Part 1
if part_one:
    current_state.rooms[1].pos = [B, D]
    current_state.rooms[3].pos = [C, D]
    current_state.rooms[5].pos = [C, A]
    current_state.rooms[7].pos = [B, A]
# Part 2
else:
    current_state.rooms[1].pos = [B, D, D, D]
    current_state.rooms[3].pos = [C, C, B, D]
    current_state.rooms[5].pos = [C, B, A, A]
    current_state.rooms[7].pos = [B, A, C, A]

HALLWAY_IND = [0, 2, 4, 6, 8]
ROOMS_INDIC = [1, 3, 5, 7]

def get_next_states(state: State):
    """Create new states, but prioritize the following:

    asdjkgnmweormelfkmw

    Prioritize nothing...

    """
    out = []

    # First we check hallways.
    for i in HALLWAY_IND:
        # Check if the room has any crabs
        hall = state.rooms[i]
        if hall.is_empty():
            continue

        # Get the crab
        crab, crab_pos = hall.get_next()

        # Get target room
        target_room = enum2room[crab]
        if state.rooms[target_room].is_empty():
            # Wait, first we need to see if we can move it to the room

            if i < target_room:
                # Hallway is on the left of the room
                left = i
                right = target_room
            else:
                left = target_room
                right = i

            but_can_it_move = True
            for j in range(left, right):
                if j % 2:
                    continue
                if j == i:
                    continue
                if state.rooms[j].has_space():
                    continue
                but_can_it_move = False
                break

            if but_can_it_move:
                # We can move the crab!

                new_state = _deepcopy(state)
                # Calculate the new cost
                # The path is the current position of the crab in the current
                # hallway, then the position in the target room and finaly
                # the move between the hallways and rooms
                target_position = state.rooms[target_room].get_position()
                move = abs(target_room - i)
                new_cost = (crab_pos + target_position + move) * crab

                # Apply changes to the state
                new_state.rooms[i].pos[crab_pos] = E
                new_state.rooms[target_room].pos[target_position - 1] = crab
                new_state.count_completed_rooms()
                out.append((new_cost, new_state))


    for i in ROOMS_INDIC:
        # Check if room is complete
        room = state.rooms[i]
        if room.is_complete():
            continue

        if room.is_empty():
            continue

        # The room is not complete so we have to move the topmost crab out.
        crab, crab_pos = room.get_next()

        # See where it has to go
        target_room = enum2room[crab]

        # See if target room is empty so we can directly move in to the
        # target room
        if state.rooms[target_room].is_empty():
            if i < target_room:
                left = i
                right = target_room
            else:
                left = target_room
                right = i
            but_can_it_move = True
            for j in range(left, right):
                if j % 2:
                    # Other rooms
                    continue
                if j == i:
                    continue
                if state.rooms[j].has_space():
                    continue
                but_can_it_move = False
                break

            if but_can_it_move:
                new_state = _deepcopy(state)
                target_position = state.rooms[target_room].get_position()
                # Calculate the new state
                move = abs(target_room - i) + 1
                new_cost = (crab_pos + move + target_position) * crab

                # Apply changes
                new_state.rooms[i].pos[crab_pos] = E
                new_state.rooms[target_room].pos[target_position - 1] = crab
                new_state.count_completed_rooms()
                out.append((new_cost, new_state))
        # Well now let's see if we can move to a halway
        for j in HALLWAY_IND:
            # We fill all the hallways. All of them...
            hall = state.rooms[j]
            if hall.has_space():
                # We can move it here.
                but_can_it_move = True

                if i < j:
                    left = i
                    right = j
                else:
                    left = j
                    right = i

                for l in range(left, right):
                    if l == j: # Ignore target hall
                        continue
                    if l % 2:  # Ignore rooms
                        continue

                    if state.rooms[l].is_empty():
                        continue

                    but_can_it_move = False
                    break

                if but_can_it_move:

                    # Fill all possible positions for this hallway.
                    for k in range(hall.s -1, -1, -1):
                        if hall.pos[k]:
                            continue

                        new_state = _deepcopy(state)
                        move = abs(i - j)

                        new_cost = (crab_pos + k + 1 + move) * crab

                        # Make the change
                        new_state.rooms[i].pos[crab_pos] = E
                        new_state.rooms[j].pos[k] = crab
                        new_state.count_completed_rooms()
                        out.append((new_cost, new_state))
    return out

def dict_def_value():
    return 100_000_000

risk_levels = defaultdict(dict_def_value)
stack = [(0, current_state)]

while stack:
    cost, state = heapq.heappop(stack)
    if state.is_complete():
        # We do not need to search more
        print("Completed!")
        break

    next_states = get_next_states(state)
    for new_cost, new_state in next_states:
        updated_cost = cost + new_cost

        if cost + new_cost < risk_levels[new_state]:
            risk_levels[new_state] = updated_cost
            heapq.heappush(stack, (updated_cost, new_state))

print(state)
msg = "Part 2: "
if part_one:
    msg = "Part 1:"

print(msg, risk_levels[target_state])