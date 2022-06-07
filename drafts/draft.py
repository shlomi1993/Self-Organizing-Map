import numpy as np
import matplotlib.pyplot as plt


# Return the (g,h) index of the BMU in the grid
def find_BMU(SOM, x):
    distSq = (np.square(SOM - x)).sum(axis=2)
    return np.unravel_index(np.argmin(distSq, axis=None), distSq.shape)


# Update the weights of the SOM cells when given a single training example
# and the model parameters along with BMU coordinates as a tuple
def update_weights(SOM, train_ex, learn_rate, radius_sq,
                   BMU_coord, step=3):
    g, h = BMU_coord
    # if radius is close to zero then only BMU is changed
    if radius_sq < 1e-3:
        SOM[g, h, :] += learn_rate * (train_ex - SOM[g, h, :])
        return SOM
    # Change all cells in a small neighborhood of BMU
    for i in range(max(0, g - step), min(SOM.shape[0], g + step)):
        for j in range(max(0, h - step), min(SOM.shape[1], h + step)):
            dist_sq = np.square(i - g) + np.square(j - h)
            dist_func = np.exp(-dist_sq / 2 / radius_sq)
            SOM[i, j, :] += learn_rate * dist_func * (train_ex - SOM[i, j, :])
    return SOM


# Main routine for training an SOM. It requires an initialized SOM grid
# or a partially trained grid as parameter
def train_SOM(SOM, train_data, learn_rate=.1, radius_sq=1,
              lr_decay=.1, radius_decay=.1, epochs=10):
    learn_rate_0 = learn_rate
    radius_0 = radius_sq
    for epoch in np.arange(0, epochs):
        np.random.shuffle(train_data)
        for train_ex in train_data:
            g, h = find_BMU(SOM, train_ex)
            SOM = update_weights(SOM, train_ex,
                                 learn_rate, radius_sq, (g, h))
        # Update learning rate and radius
        learn_rate = learn_rate_0 * np.exp(-epoch * lr_decay)
        radius_sq = radius_0 * np.exp(-epoch * radius_decay)
    return SOM


def main():
    # Dimensions of the SOM grid
    m = 10
    n = 10
    # Number of training examples
    n_x = 3000
    rand = np.random.RandomState(0)
    # Initialize the training data
    train_data = rand.randint(0, 255, (n_x, 3))
    # Initialize the SOM randomly
    SOM = rand.randint(0, 255, (m, n, 3)).astype(float)
    # Display both the training matrix and the SOM grid
    fig, ax = plt.subplots(
        nrows=1, ncols=2, figsize=(12, 3.5),
        subplot_kw=dict(xticks=[], yticks=[]))
    ax[0].imshow(train_data.reshape(50, 60, 3))
    ax[0].title.set_text('Training Data')
    ax[1].imshow(SOM.astype(int))
    ax[1].title.set_text('Randomly Initialized SOM Grid')
    fig, ax = plt.subplots(
        nrows=1, ncols=4, figsize=(15, 3.5),
        subplot_kw=dict(xticks=[], yticks=[]))
    total_epochs = 0
    for epochs, i in zip([0, 1, 5, 20], range(0, 4)):
        total_epochs += epochs
        SOM = train_SOM(SOM, train_data, epochs=epochs)
        ax[i].imshow(SOM.astype(int))
        ax[i].title.set_text('Epochs = ' + str(total_epochs))
    plt.show()


# if __name__ == '__main__':
#     main()


# import numpy as np
# import matplotlib.pyplot as plt
# from random import randint
#
# DIM = 6
#
#
# # def create_hexagonal():
# #     grid = []
# #     for i in range(4):
#
# class VotingRecord:
#     def __init__(self, municipality, cluster, total_votes, vector):
#         self.municipality = municipality
#         self.economic_cluster = cluster
#         self.total_votes = total_votes
#         self.voting_vector = vector
#
#
# def parse(file_path):
#     with open(file_path, 'r') as f:
#         lines = f.readlines()
#     parties = lines[0].split(',')[3:]
#     zipped = zip(range(len(parties)), parties)
#     party_idx_to_name = {int(idx): name for idx, name in zipped}
#     records = []
#     max_votes = 0
#     for line in lines[1:]:
#         values = line.split(',')
#         municipality = values[0]
#         cluster = int(values[1])
#         total_votes = int(values[2])
#         voting_vector = [int(i) for i in values[3:]]
#         local_max = max(voting_vector)
#         if local_max > max_votes:
#             max_votes = local_max
#         # voting_vector.append(total_votes - sum(voting_vector))  # Reminder
#         vr = VotingRecord(municipality, cluster, total_votes, voting_vector)
#         records.append(vr)
#     return records, party_idx_to_name, max_votes
#
#
# def randomize_vector(m, d):
#     return [randint(0, m) for _ in range(d)]
#
#
# class Node:
#     def __init__(self):
#         self.vector = None
#         self.neighbors = []
#
#
# class HexagonalGrid:
#     def __init__(self, size, max_votes):
#         root = Node()
#         root.vector = randomize_vector(max_votes, size)
#         for i in range(DIM):
#             root.neighbors.append(Node())
#         self.nodes = [root]
#         self.leaves = [root]
#         for d in range(size):
#             leaves = self.leaves
#             for leaf in leaves:
#                 for i, neighbor in zip(range(DIM), leaf.neighbors):
#                     if neighbor is None:
#                         new_node = Node()
#                         new_node.vector = randomize_vector(max_votes, size)
#                         for _ in range(DIM):
#                             new_node.neighbors.append(Node())
#                         new_node.neighbors[(i + (DIM / 2)) % DIM] = leaf
#                         leaf.neighbors[i] = new_node
#                         self.nodes.append(new_node)
#                 is_leaf = True
#                 for neighbor in leaf.neighbors:
#                     if neighbor.vector is None:
#                         is_leaf = False
#                         break
#                 if not is_leaf:
#                     self.leaves.remove(leaf)
#
#
# def create_hexagonal(size, max_votes):
#     grid = []
#     for i in range(size):
#         grid.append([randint(0, max_votes) for _ in range(size + i)])
#     for i in range(size - 2, -1, -1):
#         grid.append([randint(0, 2) for _ in range(size + i)])
#
#     for i in grid:
#         print(i)
#
#
# def main():
#     vr, mapper, mv = parse('./Elec_24.csv')
#     grid = create_hexagonal(5, mv)
#
#
# if __name__ == '__main__':
#     main()