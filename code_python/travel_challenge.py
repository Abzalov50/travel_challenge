"""Optimization model of the Travel Challenge.

Author: Arnold N'GORAN (arnoldngoran at gmail.com)
Date:   25/01/2020
"""
import numpy as np
import pandas as pd


# Data
V = 80  # Travel speed (km/h)
dataset = pd.read_csv

# Extract useful parts of the dataset and add a row for my initial location as
# the first row of the dataset
add = lambda key,v: np.insert(dataset[key], 0, v)
dataset = pd.DataFrame({'unique_number': add('unique_number', 0),
                        'name_en': add('name_en', 'Bayonne City Hall'),
                        'danger': add('danger', 0),
                        'longitude':add('longitude', -1.47),
                        'latitude':add('latitude', 43.49),
                        'category':add('category', None)})
N = len(dataset)   # Number of sites

# Add a `score' column
score = np.array(N)
dataset['score'] = dataset['

T = 3 * 7 * 24   # Total number of hours of holidays
dt = 6   # Length of time spent in a site (hours)
