# Shlomi Ben-Shushan 311408264


import numpy as np
from src.hexagonal import HexagonalGrid


def init_weights(grid, low, high, length):
    for row in grid:
        for node in row:
            node.pointer = np.random.randint(low=low, high=100, size=length)


def RMS(V, N):
    delta = np.floor(V - N)  # avoid overflow
    return np.sqrt(np.sum(np.square(delta)))  # maybe mean?


def update_weights(grid, representatives, lr):
    updated_grid = grid.rows
    for Vi, Nk in representatives.items():
        i, j = Nk.pos[0], Nk.pos[1]
        error = Vi.voting_vector - Nk.pointer
        neighborhood = grid.get_neighborhood_of(i, j, 2)
        layer1 = neighborhood[1]
        layer2 = neighborhood[2]
        addend0 = lr * 0.3 * error
        addend1 = lr * 0.2 * error
        addend2 = lr * 0.1 * error
        updated_grid[i][j].pointer = Nk.pointer + addend0
        for N in layer1:
            updated_grid[N.pos[0]][N.pos[1]].pointer = N.pointer + addend1
        for N in layer2:
            updated_grid[N.pos[0]][N.pos[1]].pointer = N.pointer + addend2
    return updated_grid


def train(data, epochs=10, learning_rate=0.1, decay=0.1):
    voting_records, mapper, max_votes = data
    lr = learning_rate
    grid = HexagonalGrid(size=5)
    init_weights(grid, 0, max_votes, len(voting_records[0].voting_vector))
    representatives = {}
    for t in range(epochs):
        np.random.shuffle(voting_records)  # to avoid bias.
        for vr in voting_records:
            tuples = []
            for row in grid:
                for node in row:
                    distance = RMS(V=vr.voting_vector, N=node.pointer)
                    tuples.append((node, distance))
            representatives[vr] = min(tuples, key=lambda tup: tup[1])[0]
        grid.rows = update_weights(grid, representatives, lr)
        lr *= np.exp(-t * decay)
    positions = []
    for row in grid:
        for cell in row:
            positions.append(cell.pos)
    return representatives, positions
