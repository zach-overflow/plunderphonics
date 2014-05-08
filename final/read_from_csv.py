import csv

data = []

with open('mfcc_data.csv', 'r') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
