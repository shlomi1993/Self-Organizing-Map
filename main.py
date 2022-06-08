# Shlomi Ben-Shushan 311408264


import sys
import src.parser as parser
import src.som as som
import src.display as display
from prettytable import PrettyTable


def main():
    
    # Get input
    input_file = sys.argv[1]
    print_flag = sys.argv[2] if len(sys.argv) > 2 else None
    
    # Parse & Train
    data = parser.parse(input_file)
    results, positions = som.train(data, epochs=10, learning_rate=0.1)
    
    # Analyze results
    cells = {}
    towns = {}
    for vr, rn in results.items():
        if rn.pos in cells.keys():
            cells[rn.pos].append(vr)
        else:
            cells[rn.pos] = [vr]
        towns[vr.municipality] = (vr.economic_cluster, rn)
    clusters = {}
    for p in positions:
        if p in cells.keys():
            vrs = cells[p]
            average_cluster = sum(vr.economic_cluster for vr in vrs) / len(vrs)
            clusters[p] = round(average_cluster)
        else:
            clusters[p] = 0

    # Print upon request
    if print_flag == '1':
        t = PrettyTable()
        t.align = 'l'
        t.field_names = ['Town', 'Cluster', 'Cell']
        for town, (cluster, cell) in towns.items():
            t.add_row([town, cluster, cell.pos])
        print(t)
    elif print_flag == '2':
        t = PrettyTable()
        t.align = 'l'
        t.field_names = ['Representative', 'Towns (cluster)']
        for pos, vrs in cells.items():
            towns_str = ''
            for vr in vrs:
                towns_str += f'{vr.municipality} ({vr.economic_cluster}), '
            towns_str = towns_str[:-2]
            t.add_row([str(pos), towns_str])
        print(t)

    # Display SOM using Tkinter
    hd = display.HexagonalDisplay(clusters=clusters, size=5)
    hd.display()


if __name__ == '__main__':
    main()


# Todo: Verify formulas -- 9/6
# Todo: Implement evaluation functions -- 10/6
# Todo: Play with hyper-params (epochs, lr, decay, neighborhood) -- 10/6
# Todo: Add explanations as labels to Tkinter -- 11/6
# Todo: Document the code -- 12/6
# Todo: Write report -- 13/6
