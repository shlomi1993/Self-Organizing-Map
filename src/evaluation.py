# Shlomi Ben-Shushan 311408264


# File: evaluation.py
# Content: Functions for evaluating the results of the SOM.


import src.parser as parser
import src.som as som
from matplotlib import pyplot as plt


def quantization_error(solution):
    """
    This function calculates the average distance between an input vector and
    the neuron that represents it.
    :param solution: a map from VRs to BMUs.
    :return: the quantization error
    """
    error = 0
    for vr, (bmu, _) in solution.items():
        error += som.RMSD(vr.vector, bmu.neuron)
    return error / len(solution)


def topological_error(solution):
    """
    This function counts the number of BMUs that the second-best neuron is not
    their neighbor (counts "bad" mapping).
    :param solution: a map from VRs to BMUs.
    :return: the topological error
    """
    miss = 0
    for bmu, validator in solution.values():
        if not bmu.is_in(validator.neighbors):
            miss += 1
    return miss / len(solution)


def plot_errors_per_lr(lrs, q_errors, t_errors):
    """
    This function creates a plot portraying the quantization error and the
    topological error for each learning rate. It helps to determine the learning
    rate for a given dataset.
    :param lrs: a list of learning rates.
    :param q_errors: a list of quantization errors.
    :param t_errors: a list of topological errors.
    :return: None.
    """
    fig, (ax1, ax2) = plt.subplots(2, 1, sharex='all')
    fig.suptitle('Error per Learning Rate')
    ax1.set(ylabel='Quantization Error')
    ax1.plot(lrs, q_errors, 'tab:orange')
    ax2.set(xlabel='Learning Rate', ylabel='Topological Error')
    ax2.plot(lrs, t_errors, 'tab:red')
    fig.show()


def plot_errors_per_epoch(q_errors, t_errors):
    """
    This function creates a plot portraying the quantization error and the
    topological error for each calculated epoch.
    :param q_errors: a list of quantization errors.
    :param t_errors: a list of topological errors.
    :return: None.
    """
    x_values = list(range(len(q_errors)))
    fig, (ax1, ax2) = plt.subplots(2, 1, sharex='all')
    fig.suptitle('Error per Epochs')
    ax1.set(ylabel='Quantization Error')
    ax1.plot(x_values, q_errors, 'tab:orange')
    ax2.set(xlabel='Epoch', ylabel='Topological Error')
    ax2.plot(x_values, t_errors, 'tab:red')
    fig.show()


def eval_errors(data, start=0.05, end=1.05, step=0.05, epochs=10, console=None):
    """
    This function evaluates quantization and topological errors on the given
    data for a range of learning rates.
    :param data: parsed and preprocessed data from a given input CSV file.
    :param start: the first learning rate to check.
    :param end: the last learning rate to check.
    :param step: the steps between each learning rate in the range.
    :param epochs: the number of epochs to run (10 is a good number).
    :param console: a Tkinter Text-area to write logs to.
    :return: a log.
    """
    evaluations = []
    lrs, qes, tes = [], [], []
    lr = start
    log = ''
    while lr < end:
        representatives, _ = som.train(data, epochs, lr, 0.1)
        qe = quantization_error(representatives[-1])
        te = topological_error(representatives[-1])
        lrs.append(lr)
        qes.append(qe)
        tes.append(te)
        evaluations.append((lr, qe, te))
        lr += step
        log += f'LR {lr} => QE={round(qe, 4)} and TE={round(te, 4)}\n'
    best_qe = min(evaluations, key=lambda tup: tup[1])
    best_te = min(evaluations, key=lambda tup: tup[2])
    log += f'Best LR by QE is {best_qe[0]} with QE of {round(best_qe[1], 2)} '
    log += f'and TE of {round(best_qe[2], 2)}\n'
    log += f'Best LR by TE is {best_te[0]} with QE of {round(best_te[1], 2)} '
    log += f'and TE of {round(best_te[2], 2)}\n'
    plot_errors_per_lr(lrs, qes, tes)
    if console:
        console.delete('1.0', 'end')
        console.insert('end', log)
    else:
        print(log)
    return log


# This is a useful way to debug without the app.
if __name__ == '__main__':
    parsed = parser.parse('../Elec_24.csv')
    eval_errors(parsed)
