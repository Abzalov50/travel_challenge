"""Optimization model of the Travel Challenge.

Author: Arnold N'GORAN (arnoldngoran at gmail.com)
Date:   25/01/2020
"""
import sys
from math import pi, sqrt, sin, cos, asin

from pytravelchallenge.solver import SCIP

import numpy as np
import pandas as pd


# Solver's parameters
solver_name = 'SCIP'

############# Data
V = 80  # Travel speed (km/h)
# The first row of `dataset' is my initial location
# It is sorted so that the `Cultural' sites are first,
# then the `Natural' ones, finally the `Mixed' ones.
# It contains a column `score' that gives the score
# of each site.
# Latitude and Longitude have been converted into radians
dataset = pd.read_csv('../whc-sites-2019-light-sorted.csv',
                      encoding = "ISO-8859-1")

# `matrix_sites_country' is a binary matrix, where the rows
# represent the sites, and the columns represent the countries.
# The goal of this matrix is to allow to score the country visited,
# and score them only once.
# The sum of one column is the total number of sites located
# in the country represented by that column.
matrix_sites_country = pd.read_csv('../matrix-site-country.csv',
                                   encoding = "ISO-8859-1")

K = len(matrix_sites_country.keys())  # Number of countries
N = len(dataset)   # Number of sites

# Number of `Cultural' sites
Nc = len(dataset[dataset['category'] == 'Cultural'])
# Number of `Natural' sites
Nn = len(dataset[dataset['category'] == 'Natural'])
# Number of `Mixed' sites
Nm = len(dataset[dataset['category'] == 'Mixed'])

# Normally, N = Nc + Nm + Nn - 1

T = 3 * 7 * 24   # Total number of hours of holidays
dt = 6   # Length of time spent in a site (hours)

# Distance matrix
# Distance between 2 sites has been calculated
# using Heaversine formula, defined by the following function:
def heaversine(lat1, lat2, long1, long2):
    R = 6371   # Earth radius in km
    return 2 * R * (asin(sqrt((sin(0.5 * (lat2 - lat1)))**2
                              + cos(lat1)*cos(lat2) * (sin(0.5 * (long2 - long1)))**2)))

D = pd.read_csv('../matrix_distance.csv')
D = D.values
def dist(i,j):
    if i <= j:
        return D[i,j]
    else:
        return D[i,j]

############# Variables
solver = sys.modules[__name__].__getattribute__(solver_name)

print('##### Creating optimization MODEL...')
m = solver('Travel Challenge')
m.set_param('limits/gap', 1e-3)

print('\n##### Creating optimization VARIABLES...')
# Site visited? 1 if yes, otherwise 0
x = {i: m.add_var(lb=0, vtype=m.BINARY, name='x_%s' % i)
     for i in range(N)}

# Has path (i->j) been taken to visit site `j'?
# 1 if so, otherwise 0
y = {(i,j): m.add_var(lb=0, vtype=m.BINARY, name='y_%s_%s' % (i,j))
     for i in range(N) for j in range(N)}

# Country visited score
z = {i: m.add_var(lb=0, vtype=m.BINARY, name='z_%s' % i)
     for i in range(N)}

print('\n##### Setting optimization CONSTRAINTS...')
############# Constraints
for i in range(N):
    # No path between the same point or site
    m.add_constr(y[i,i] == 0, name='no_path_%s_%s' % (i,i))

    # For a specific departure, we can only end up in but one site
    m.add_constr(m.quicksum(y[i,j] for j in range(N)) <= 1,
                 name='uniq_dest_%s' % i)

    # Even though it is not forbidden, we should not do a round-trip
    # between 2 sites, because a reward only once
    """
    for j in range(N):
        m.add_constr(y[i,j] + y[j,i] <= 1,
                     name='no_roundtrip_%s_%s' % (i,j))
    """

# An arrival at a site, means that it is visited.
# There may be only one departure for a given destination
for j in range(1, N):
    m.add_constr(m.quicksum(y[i,j] for i in range(N)) == x[j],
                 name='uniq_depart_%s' % j)    

# Site 0 is the departure and the arrival of the journey
m.add_constr(m.quicksum(y[i,0] for i in range(N)) == 1,
             name='arrival')
m.add_constr(m.quicksum(y[0,j] for j in range(N)) == 1,
             name='departure')

# Ensure that a country visited is rewarded only once
msc = matrix_sites_country
for j, key in enumerate(msc):
    m.add_constr(m.quicksum(msc[key][i] * x[i] for i in range(N))
                 >= z[j], name='countr_reward_%s' % key)

# Holidays duration budget
m.add_constr(m.quicksum((dist(i,j) / V + dt) * y[i,j]
                        for i in range(N) for j in range(N))
             <= T, name='duration_budget')

# There must be an equal number of `Cultural' and 'Natural' sites.
# 'Mixed' sites count for both
"""
m.add_constr(m.quicksum(x[i] for i in range(1, Nc+1))
             == m.quicksum(x[i] for i in range(Nc+1,Nc+Nm+1)),
             name='eq_nb_site_type')
"""
########## Objective function
print('\n##### Setting OBJECTIVE...')
m.set_objective(m.quicksum(dataset['score'][i] * x[i]
                           for i in range(N))
                + 2 * m.quicksum(z[j] for j in range(K)))


if __name__ == '__main__':
    m.optimize()
