from collections import Counter, defaultdict
from heapq import heappop, heappush, heappushpop
from functools import reduce
from bisect import bisect_left, bisect_right, bisect


pos = [3-1,5-1] # position [player1,player2]
tot = [0,0] # total [player1,player2]
r = 1 # next roll
p = 1 # player who just moved (next player is p=0 which is player 1)

while tot[p] < 1000:
    p = 1 - p
    pos[p] = (pos[p] + 3*r + 3) % 10
    tot[p] += pos[p] + 1
    r += 3

print("Losing score:", min(tot), ". Last roll:", r-1)
print("LS * LR:", min(tot) * (r-1))

rf = [(3,1),(4,3),(5,6),(6,7),(7,6),(8,3),(9,1)]

## if p1 is about to move, return (w1,w2) where
## wj is the number of universes where player j wins
def wins(p1,t1,p2,t2):
    if t2 <= 0: return (0,1) # p2 has won (never p1 since p1 about to move)

    w1,w2 = 0,0
    for (r,f) in rf:
        c2,c1 = wins(p2,t2,(p1+r)%10,t1 - 1 - (p1+r)%10) # p2 about to move
        w1,w2 = w1 + f * c1, w2 + f * c2

    return w1,w2

print("Bigger winner universes:",max(wins(2,21,4,21))) # initially p1=4,p2=2

def read_input(path: str = 'input.txt'):
    inputs = []
    with open(path) as filet:
        for line in filet.readlines():
            line = line.rstrip()
            inputs.append(line)
    inputs = [int(ele.split()[-1]) for ele in inputs]
    return inputs


def main1():
    result = 0
    print(f'The result for solution 1 is: {result}')


def main2():
    result = 0
    print(f'The result for solution 2 is: {result}')


if __name__ == '__main__':
    main1()
    main2()
