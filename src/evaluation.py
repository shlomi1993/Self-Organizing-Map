# Shlomi Ben-Shushan 311408264


import src.parser as parser
import src.som as som


def quantization_error(data):
    return sum(rep.distance for rep in data.values()) / len(data)


def topological_error(data):
    miss = 0
    for rep in data.values():
        if not rep.cell.is_in(rep.validator.cell.neighbors):
            miss += 1
    return miss / len(data)


def eval_errors(data):
    evaluations = []
    lrs = [round(i * 0.1, 2) for i in range(1, 11)]  # [round(i * 0.05, 2) for i in range(1, 21)]
    dcs = [0.1]  # [round(i * 0.1, 2) for i in range(1, 11)]
    for lr in lrs:
        for d in dcs:
            representatives, _ = som.train(data, epochs=10, learning_rate=lr, decay=d)
            qe = quantization_error(representatives)
            te = topological_error(representatives)
            print(f'{lr}/{d} => QE={round(qe, 4)}, TE={round(te, 4)}')
            evaluations.append((lr, d, qe, te))
    best_qe = min(evaluations, key=lambda tup: tup[2])
    best_te = min(evaluations, key=lambda tup: tup[3])
    print(f'Best LR/D by QE is {best_qe[0]}/{best_qe[1]} with QE of {best_qe[2]} and TE of {best_qe[3]}')
    print(f'Best LR/D by TE is {best_te[0]}/{best_te[1]} with QE of {best_te[2]} and TE of {best_te[3]}')


if __name__ == '__main__':
    parsed = parser.parse('../Elec_24.csv')
    eval_errors(parsed)

