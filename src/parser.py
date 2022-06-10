# Shlomi Ben-Shushan 311408264


import numpy as np


class VotingRecord:

    def __init__(self, town, cluster, vector):
        self.town = town
        self.cluster = cluster
        self.vector = vector

    def __str__(self):
        return f'{self.town} ({self.cluster}): votes{self.vector}'


def parse(file_path):
    with open(file_path, 'r') as f:
        lines = f.readlines()
    parties = lines[0].split(',')[3:]
    zipped = zip(range(len(parties)), parties)
    mapper = {int(idx): name for idx, name in zipped}
    mapper[len(mapper)] = 'others'
    voting_records = []
    max_votes = 0
    for line in lines[1:]:
        values = line.split(',')
        municipality = values[0]
        cluster = int(values[1])
        total = int(values[2])
        arr = [int(i) for i in values[3:]]
        arr.append(total - sum(arr))
        vector = np.array(arr)
        max_votes = max(max_votes, max(vector))
        voting_records.append(VotingRecord(municipality, cluster, vector))
    return voting_records, mapper, max_votes
