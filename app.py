# Shlomi Ben-Shushan 311408264


import sys
import math
from random import randint, shuffle
from src.parser import parse
from src.hexagonal import HexagonalGrid


def init_weights(grid, rand_range, length):
    start, end = rand_range
    for row in grid:
        for node in row:
            node.pointer = [randint(start, end) for _ in range(length)]


def RMS(V, N):
    return math.sqrt(sum(math.pow(V[i] - N[i], 2) for i in range(len(V))))


def vector_add(v1, v2):
    if len(v1) != len(v2):
        return None
    return [v1[i] + v2[i] for i in range(len(v1))]


def vector_sub(v1, v2):
    if len(v1) != len(v2):
        return None
    return [v1[i] - v2[i] for i in range(len(v1))]


def vector_const_mult(v, c):
    return [c * v[i] for i in range(len(v))]


def update_weights(grid, representatives, lr):
    for Vi, Nk in representatives.items():
        i, j = Nk.pos[0], Nk.pos[1]
        error = vector_sub(Vi.voting_vector, Nk.pointer)
        neighborhood = grid.get_neighborhood_of(i, j, 2)
        layer1 = neighborhood[1]
        layer2 = neighborhood[2]
        addend0 = vector_const_mult(vector_const_mult(error, 0.3), lr)
        addend1 = vector_const_mult(vector_const_mult(error, 0.2), lr)
        addend2 = vector_const_mult(vector_const_mult(error, 0.1), lr)
        grid[i][j].pointer = vector_add(Nk.pointer, addend0)
        for N in layer1:
            i, j = N.pos[0], N.pos[1]
            grid[i][j].pointer = vector_add(N.pointer, addend1)
        for N in layer2:
            i, j = N.pos[0], N.pos[1]
            grid[i][j].pointer = vector_add(N.pointer, addend2)


def train(data, epochs=10, learning_rate=0.01, decay=0.1):
    voting_records, mapper, max_votes = data
    lr = learning_rate
    grid = HexagonalGrid(size=5)
    init_weights(grid, (0, max_votes), len(voting_records[0].voting_vector))
    representatives = {}
    for t in range(epochs):
        shuffle(voting_records)  # to avoid bias.
        for vr in voting_records:
            tuples = []
            for row in grid:
                for node in row:
                    distance = RMS(V=vr.voting_vector, N=node.pointer)
                    tuples.append((node, distance))
            representatives[vr] = min(tuples, key=lambda tup: tup[1])[0]
        X = grid[0][0]
        update_weights(grid, representatives, lr)
        Y = grid[0][0]
        # lr *= math.exp(-t * decay)
        # for vr, rn in representatives:
        #     rms = RMS(vr.voting_vector, rn.pointer)
        #     print(f'{vr.municipality} is represented by node {rn.pos} RMS is: {rms}')
        # exit()
    return representatives


def quantization_error():
    # average distance between Nk to Vi.
    pass


def topological_error():
    # is 2nd best close to the 1st best?
    pass


economic_cluster_color_mapper = {
    1: '#9e0142',
    2: '#d53e4f',
    3: '#f46d43',
    4: '#fdae61',
    5: '#fee08b',
    6: '#e6f598',
    7: '#abdda4',
    8: '#66c2a5',
    9: '#3288bd',
    10: '#5e4fa2',
}


def main():
    data = parse(sys.argv[1])
    results = train(data, epochs=10, learning_rate=0.1)
    for vr, rn in results.items():
        rms = RMS(vr.voting_vector, rn.pointer)
        print(f'{vr.municipality} is represented by node {rn.pos} RMS is: {rms}')


if __name__ == '__main__':
    main()
