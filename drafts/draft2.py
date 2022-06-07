# # Shlomi Ben-Shushan 311408264
#
#
# from random import randint
#
#
# DIM = 6
#
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
#     party_idx_to_name = { int(idx): name for idx, name in zipped }
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
# def create_hexagonal(size, max_votes):
#     grid = []
#     for i in range(size):
#         grid.append([randint(0, 9) for _ in range(size + i)])
#     for i in range(size - 2, -1, -1):
#         grid.append([randint(0, 9) for _ in range(size + i)])
#
#     msg = ''
#     for i, row in zip(range(size), grid[:size]):
#         msg += ' ' * (size - i - 1) + str(row).replace(', ', ' ').replace('[', '').replace(']', '') + '\n'
#     for i, row in zip(range(1, size), grid[size:]):
#         msg += ' ' * (i) + str(row).replace(', ', ' ').replace('[', '').replace(']', '') + '\n'
#     print(msg)
#
#     return grid
#
#
# def get_neighbors(hexagonal, i, j):
#
#     size = 5
#
#     up = []
#     mid = []
#     down = []
#
#     if i % 2:
#
#
#
#
#
#     # try:
#     #     hexagonal[i][j]
#     # except IndexError:
#     #     print('indexes out of hexagonal ranges')
#     #
#     # msg = f'neighbors of grid[{i}][{j}] ({hexagonal[i][j]}) are:'
#     #
#     # msg += '\nup:'
#     # if 0 < i:
#     #     if j < len(hexagonal[i - 1]):
#     #         msg += ' ' + str(hexagonal[i - 1][j])
#     #     if i < size and i % 2 == 0:
#     #         if j > 0:
#     #             msg += ' ' + str(hexagonal[i - 1][j - 1])
#     #     else:
#     #         if j < len(hexagonal[i - 1]):
#     #             msg += ' ' + str(hexagonal[i - 1][j + 1])
#     #
#     # msg += '\nmiddle:'
#     # if j > 0:
#     #     msg += ' ' + str(hexagonal[i][j - 1])
#     # if j + 1 < len(hexagonal[i]):
#     #     msg += ' ' + str(hexagonal[i][j + 1])
#     #
#     # msg += '\ndown:'
#     # if i < len(hexagonal) - 1:
#     #     if j < len(hexagonal[i + 1]):
#     #         msg += ' ' + str(hexagonal[i + 1][j])
#     #     if i % 2:
#     #         if j > 0:
#     #             msg += ' ' + str(hexagonal[i + 1][j - 1])
#     #     else:
#     #         if j + 1 < len(hexagonal):
#     #             msg += ' ' + str(hexagonal[i + 1][j + 1])
#     #
#     # print(msg)
#
#
# def main():
#     vr, mapper, mv = parse('./Elec_24.csv')
#     grid = create_hexagonal(5, mv)
#     get_neighbors(grid, 0, 0)
#     get_neighbors(grid, 4, 0)
#     get_neighbors(grid, 8, 0)
#     # get_neighbors(grid, 8, 4)
#     # get_neighbors(grid, 4, 8)
#     # get_neighbors(grid, 0, 4)
#
#
# if __name__ == '__main__':
#     main()