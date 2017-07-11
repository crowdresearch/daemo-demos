import csv
import sys
import math
from collections import defaultdict
import numpy as np

roles = ['professor', 'entrepreneur', 'scientist', 'engineer']

def computeAdjacency(graduates):
    statistics = defaultdict(lambda : defaultdict(float))

    for role1 in roles:
        for role2 in roles:
            has_role1 = [graduate['is_' + role1]==1 for graduate in graduates]
            has_role2 = [graduate['is_' + role2]==1 for graduate in graduates]

            total_role1 = np.sum(has_role1)
            total_both = np.sum(np.logical_and(has_role1, has_role2))
            statistics[role1][role2] = float(total_both)/total_role1

    return statistics

def reportPercentages(statistics, output_csv):
    with open(output_csv, 'w') as f:
        adjacencyCSV = csv.DictWriter(f, fieldnames=["source", "target", "weight"])
        adjacencyCSV.writeheader()
        for role1 in roles:
            for role2 in roles:
                print("%s who are %s: %.2f") % (role1, role2, statistics[role1][role2])
                to_write = {"source": role1, "target": role2, "weight": statistics[role1][role2]}
                adjacencyCSV.writerow(to_write)



if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: adjacency.py inputCSV.csv outputCSV.csv")
        sys.exit(0)
    inputCSV = sys.argv[1]
    outputCSV = sys.argv[2]

    graduates = []
    with open(inputCSV, 'r') as f:
        graduatesCSV = csv.DictReader(f)
        for row in graduatesCSV:
            graduate = dict()
            graduate['is_professor'] = int(row['is_professor'])
            graduate['is_entrepreneur'] = int(row['is_entrepeneur'])
            graduate['is_scientist'] = int(row['is_scientist'])
            graduate['is_engineer'] = int(row['is_engineer'])
            graduates.append(graduate)

    statistics = computeAdjacency(graduates)
    reportPercentages(statistics, outputCSV)
