import csv
import sys
import math
from collections import defaultdict
import numpy as np

BOOTSTRAP_SAMPLE_PROPORTION = 0.666
BOOTSTRAP_NUM_SAMPLES = 10000
ALPHA = 0.05
YEAR_RANGE = (1980, 2020)

roles = ['professor', 'entrepreneur', 'scientist', 'engineer']

def runBootstrap(graduates, min_year, max_year):
    statistics = defaultdict(list)
    if min_year is None and max_year is None:
        filtered = graduates
        print('%d graduates included with no year filter') % (len(filtered))

    else:
        filtered = [grad for grad in graduates if (grad['year'] >= min_year and grad['year'] <= max_year)]
        print('%d out of %d graduates included in filter (%d-%d)') % (len(filtered), len(graduates), min_year, max_year)

    for i in range(BOOTSTRAP_NUM_SAMPLES):
        if i%1000 == 0:
            print('Bootstrap sample ' + str(i+1))

        sample = np.random.choice(filtered,
            int(math.ceil(BOOTSTRAP_SAMPLE_PROPORTION)*len(filtered)))

        # calculate the mean for each role for this sample
        for role in roles:
            sample_role = [graduate['is_' + role] for graduate in sample]
            statistics[role].append(np.mean(sample_role))

    for role in roles:
        print(role)
        reportCI(statistics[role])

def reportCI(proportions):
    mean = np.percentile(proportions, 50)
    lower_bound = np.percentile(proportions, ALPHA/2 * 100)
    upper_bound = np.percentile(proportions, (1.0-(ALPHA/2))*100)
    print("%.2f (%.2f - %.2f)") % (mean, lower_bound, upper_bound)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: bootstrap.py inputCSV.csv")
        sys.exit(0)
    inputCSV = sys.argv[1]

    graduates = []
    with open(inputCSV, 'r') as f:
        graduatesCSV = csv.DictReader(f)
        for row in graduatesCSV:
            graduate = dict()
            graduate['is_professor'] = int(row['is_professor'])
            graduate['is_entrepreneur'] = int(row['is_entrepeneur'])
            graduate['is_scientist'] = int(row['is_scientist'])
            graduate['is_engineer'] = int(row['is_engineer'])
            graduate['year'] = None
            if row['Education.EndYear'] != '':
                graduate['year'] = int(row['Education.EndYear'])
            graduates.append(graduate)

    for i in range(YEAR_RANGE[0], YEAR_RANGE[1], 10):
        runBootstrap(graduates, i, i+9)

    #and once more with no year ranges, including the people who didn't report any graduation year
