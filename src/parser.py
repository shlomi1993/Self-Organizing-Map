# Shlomi Ben-Shushan 311408264


class VotingRecord:

    def __init__(self, municipality, cluster, total_votes, vector):
        self.municipality = municipality
        self.economic_cluster = cluster
        self.total_votes = total_votes
        self.voting_vector = vector

    def __str__(self):
        return f'{self.municipality} ({self.economic_cluster}, ' \
               f'{self.total_votes}): votes{self.voting_vector}'


def parse(file_path):
    with open(file_path, 'r') as f:
        lines = f.readlines()
    parties = lines[0].split(',')[3:]
    zipped = zip(range(len(parties)), parties)
    party_idx_to_name = {int(idx): name for idx, name in zipped}
    voting_records = []
    max_votes = 0
    for line in lines[1:]:
        values = line.split(',')
        municipality = values[0]
        cluster = int(values[1])
        total_votes = int(values[2])
        voting_vector = [int(i) for i in values[3:]]
        local_max = max(voting_vector)
        if local_max > max_votes:
            max_votes = local_max
        # voting_vector.append(total_votes - sum(voting_vector))  # Need reminder?
        vr = VotingRecord(municipality, cluster, total_votes, voting_vector)
        voting_records.append(vr)
    return voting_records, party_idx_to_name, max_votes
