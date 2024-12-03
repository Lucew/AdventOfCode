from collections import Counter, defaultdict
from heapq import heappop, heappush, heappushpop
from functools import reduce
from bisect import bisect_left, bisect_right, bisect
# https://www.reddit.com/r/adventofcode/comments/rlxhmg/comment/hqxczc4/?utm_source=share&utm_medium=web3x&utm_name=web3xcss&utm_term=1&utm_content=share_button

cuboids = [s.replace('x=','').replace(',y=',' ').replace(',z=',' ').replace('..',' ') for s in open("input.txt").readlines()]
cuboids = [s.replace('on','1').replace('off','0') for s in cuboids]
cuboids = [[int(x) for x in s.split()] for s in cuboids]
# cuboids = [c for c in cuboids if abs(c[1]) <= 50] # for part 1

# a cuboid is represented as [+1/-1,xmin,xmax,ymin,ymax,zmin,zmax]
# where +1 is 'added cuboid' and -1 is 'subtracted cuboid'

# return the cuboid at the intersection of cuboids s and t
# if cuboid t is added, the intersection is subtracted, and vice versa
def intersection(s,t):
    mm = [lambda a,b:-b,max,min,max,min,max,min]
    n = [mm[i](s[i],t[i]) for i in range(7)]
    return None if n[1] > n[2] or n[3] > n[4] or n[5] > n[6] else n

cores = []
for cuboid in cuboids:
    toadd = [cuboid] if cuboid[0] == 1 else [] # add cuboid to core if 'on'
    for core in cores:
        inter = intersection(cuboid,core)
        if inter:
            toadd += [inter] # if nonempty, add to the core later
    cores += toadd

def countoncubes(cores):
    oncount = 0
    for c in cores:
        oncount += c[0] * (c[2]-c[1]+1) * (c[4]-c[3]+1) * (c[6]-c[5]+1)
    return oncount

print('On cubes:', countoncubes(cores))
