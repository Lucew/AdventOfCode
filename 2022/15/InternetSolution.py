# https://www.reddit.com/r/adventofcode/comments/zmcn64/comment/j0b90nr/
"""
Here's the idea:

As there is only one missing value, it's going to be just outside the boundaries of at least two scanners (unless we're
incredibly unlucky and it's right on the bounds of the 0-4_000_000 square, but it isn't!).

The boundary of a scanner is four line segments. If a scanner is in position (sx,sy) and has 'radius' r, then we want
the line segments just outside, i.e. of radius r+1. There will be two line segments of gradient 1:

y = x + sy-sx+r+1
y = x + sy-sx-r-1
and two line segments of gradient -1:

y = -x + sx+sy+r+1
y = -x + sx+sy-r-1
Determining where a line y=x+a and a line y=-x+b intersect is very easy -
they intersect at the point ( (b-a)/2 , (a+b)/2 ).

One of these intersection points will be the missing scanner location. So, we assemble a set of all the 'a' coefficients
 (lines of gradient 1) and all the 'b' coefficients (lines of gradient -1), then look at their intersections to see if
 they are the point we need. Given the number of scanners we only need to check a couple of thousand points at most.
"""
import re
def all_numbers(s): return [int(d) for d in re.findall("(-?\d+)", s)]
def md(p, q): return abs(p[0]-q[0])+abs(p[1]-q[1])

input_data = open('input.txt').read()
data = [all_numbers(line) for line in input_data.split("\n")]
radius = {(a,b):md((a,b),(c,d)) for (a,b,c,d) in data}
scanners = radius.keys()

acoeffs, bcoeffs = set(), set()
for ((x,y), r) in radius.items():
    acoeffs.add(y-x+r+1)
    acoeffs.add(y-x-r-1)
    bcoeffs.add(x+y+r+1)
    bcoeffs.add(x+y-r-1)

bound = 4_000_000
for a in acoeffs:
    for b in bcoeffs:
        p = ((b-a)//2, (a+b)//2)
        if all(0<c<bound for c in p):
            if all(md(p,t)>radius[t] for t in scanners):
                print(4_000_000*p[0]+p[1])