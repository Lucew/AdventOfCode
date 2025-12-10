#!/usr/bin/env python3

import sys
import re
import numpy as np
from scipy.optimize import milp, LinearConstraint, Bounds
from time import time

ts = time()

def read_input(path: str = 'input.txt'):
    inputs = []
    with open(path) as filet:
        for line in filet.readlines():
            line = line.rstrip()
            inputs.append(line)
    return inputs

machines = []
for line in read_input():
    button_strs = re.findall(r"\(([^)]*)\)", line)
    buttons = []
    for button in button_strs:
        inds = [int(x) for x in button.split(',')]
        buttons.append(inds)
    m = re.search(r"\{([^}]*)\}", line)
    jolts = [int(x) for x in m.group(1).split(',')]
    machines.append((buttons, jolts))

def ilp(buttons, jolts):
    n = len(jolts)
    m = len(buttons)

    A = np.zeros((n, m), dtype=int)
    for j, inds in enumerate(buttons):
        for i in inds:
            A[i, j] = 1

    c = np.ones(m, dtype=float)

    jolts = np.array(jolts, dtype=float)
    lc = LinearConstraint(A, lb=jolts, ub=jolts)

    bounds = Bounds(lb=np.zeros(m), ub=np.full(m, np.inf))

    integrality = np.ones(m, dtype=int)

    res = milp(c=c,
               constraints=[lc],
               integrality=integrality,
               bounds=bounds)
    if res.status != 0:
        raise RuntimeError(f"ILP failed with status {res.status}: {res.message}")

    return int(round(res.fun))

total = 0
for buttons, jolts in machines:
    total += ilp(buttons, jolts)

print(total)

print(f"runtime: {time() - ts:.4f}s")