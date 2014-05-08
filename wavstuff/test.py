import csv
from numpy import array

data = []

with open('mfcc_data.csv', 'rb') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        data.append([row[0], array(map(lambda e : float(e), row[1:]))])

print data[0]
print data[1]
