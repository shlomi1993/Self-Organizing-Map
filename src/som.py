# Shlomi Ben-Shushan 311408264


import numpy as np
from src.hexagonal import HexagonalGrid


class Representative:
    def __init__(self, cell, distance):
        self.cell = cell
        self.distance = distance  # for Quantization Error.
        self.validator = None  # for Topological Error.


def init_weights(grid, low, high, length):
    for row in grid:
        for cell in row:
            cell.neuron = np.random.randint(low=low, high=high, size=length)


def RMSD(V, N):
    delta = np.floor(V - N)  # avoid overflow
    return np.sqrt(np.mean(np.square(delta)))  # maybe mean?


def update_weights(grid, representatives, lr):
    for vr, rep in representatives.items():
        Nk = rep.cell
        i, j = Nk.pos[0], Nk.pos[1]
        error = vr.vector - Nk.neuron
        neighborhood = grid.get_neighborhood_of(i, j, 2)
        layer1 = neighborhood[1]
        layer2 = neighborhood[2]
        addend0 = lr * 0.3 * error
        addend1 = lr * 0.2 * error
        addend2 = lr * 0.1 * error
        grid[i][j].neuron = Nk.neuron + addend0
        for N in layer1:
            grid[N.pos[0]][N.pos[1]].neuron = N.neuron + addend1
        for N in layer2:
            grid[N.pos[0]][N.pos[1]].neuron = N.neuron + addend2


def train(data, epochs=10, learning_rate=0.1, decay=0.1):
    voting_records, mapper, max_votes = data
    lr = learning_rate
    grid = HexagonalGrid(size=5)
    init_weights(grid, 0, 200, len(voting_records[0].vector))
    representatives = {}
    solutions = []
    for t in range(epochs):
        np.random.shuffle(voting_records)  # to avoid bias.
        for vr in voting_records:
            candidates = []
            for row in grid:
                for cell in row:
                    distance = RMSD(V=vr.vector, N=cell.neuron)
                    candidates.append(Representative(cell, distance))
            candidates.sort(key=lambda r: r.distance)
            chosen = candidates[0]
            chosen.validator = candidates[1].cell
            representatives[vr] = chosen
        solutions.append(representatives)
        update_weights(grid, representatives, lr)
        lr *= np.exp(-t * decay)
    positions = []
    for row in grid:
        for cell in row:
            positions.append(cell.pos)
    return solutions, positions


def analyze(results, positions):
    temp = {}
    town_to_cell = {}
    cell_to_vectors = {}
    for vr, rn in results.items():
        p = rn.cell.pos
        if p in temp.keys():
            temp[p].append(vr)
        else:
            temp[p] = [vr]
        town_to_cell[vr.town] = (vr.cluster, rn.cell)
    for p in positions:
        if p in temp.keys():
            vrs = temp[p]
            average_cluster = round(sum(vr.cluster for vr in vrs) / len(vrs))
            cell_to_vectors[p] = (vrs, average_cluster)
        else:
            cell_to_vectors[p] = ([], 0)
    return town_to_cell, cell_to_vectors
