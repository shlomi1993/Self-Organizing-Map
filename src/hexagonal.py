# Shlomi Ben-Shushan 311408264


class Cell:
    def __init__(self, i, j):
        self.pos = (i, j)
        self.neuron = None
        self.neighbors = []

    def __str__(self):
        return f'Cell {self.pos} holds: {self.neuron}'

    def is_in(self, group):
        for x in group:
            if x.pos == self.pos:
                return True
        return False


class HexagonalGrid:
    def __init__(self, size):
        first_row = [Cell(0, j) for j in range(size)]
        for j in range(size - 1):
            first_row[j].neighbors.append(first_row[j + 1])
            first_row[j + 1].neighbors.append(first_row[j])
        self.rows = [first_row]
        for i in range(1, size):
            new_row = [Cell(i, j) for j in range(size + i)]
            for j in range(size + i - 1):
                new_row[j].neighbors.append(self.rows[i - 1][j])
                new_row[j + 1].neighbors.append(self.rows[i - 1][j])
                new_row[j].neighbors.append(new_row[j + 1])
                new_row[j + 1].neighbors.append(new_row[j])
                self.rows[i - 1][j].neighbors.append(new_row[j])
                self.rows[i - 1][j].neighbors.append(new_row[j + 1])
            self.rows.append(new_row)
        max_size = len(self.rows[-1])
        k = 1
        for i in range(size, max_size):
            new_row = [Cell(i, j) for j in range(max_size - k)]
            k += 1
            for j in range(len(new_row)):
                new_row[j].neighbors.append(self.rows[i - 1][j])
                new_row[j].neighbors.append(self.rows[i - 1][j + 1])
                if j < len(new_row) - 1:
                    new_row[j].neighbors.append(new_row[j + 1])
                if j > 0:
                    new_row[j].neighbors.append(new_row[j - 1])
                self.rows[i - 1][j].neighbors.append(new_row[j])
                self.rows[i - 1][j + 1].neighbors.append(new_row[j])
            self.rows.append(new_row)

    def __str__(self):
        string = ''
        for i, row in zip(range(len(self.rows)), self.rows):
            string += f'Row {i}:\n'
            for j, cell in zip(range(len(row)), row):
                string += f'  Col {j}: ' + cell.__str__() + '\n'
            string += '\n'
        return string

    def __iter__(self):
        self.iter = self.rows.__iter__()
        return self

    def __next__(self):
        return self.iter.__next__()

    def __getitem__(self, item):
        return self.rows.__getitem__(item)

    def get_neighbors_of(self, i, j):
        return self.rows[i][j].neighbors

    def get_neighborhood_of(self, i, j, k):
        neighborhood = {0: [self.rows[i][j]]}
        if k == 0:
            return neighborhood
        neighborhood[1] = self.get_neighbors_of(i, j)
        if k == 1:
            return neighborhood
        collected = neighborhood[0] + neighborhood[1]
        for x in range(2, k + 1):
            next_layer = []
            prev_layer = neighborhood[x - 1]
            for n in prev_layer:
                mid_set = self.get_neighbors_of(n.pos[0], n.pos[1])
                for nn in mid_set:
                    if not nn.is_in(prev_layer) and not nn.is_in(collected):
                        next_layer.append(nn)
                        collected.append(nn)
            neighborhood[x] = next_layer
        return neighborhood
