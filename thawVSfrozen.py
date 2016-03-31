"""Parse data from an ugly CSV or Excel file, and render it in
JSON-like form"""

import csv
import matplotlib.pyplot as plt
import matplotlib as mpl
import matplotlib.ticker as mt
import numpy as np

MY_FILE = "../data/indicators.csv"


def parse(raw_file, delimiter):
    """parses a raw CSV file to a json-like object"""
    # open the file
    opened_file = open(raw_file)

    # read the file
    csv_data = csv.reader(opened_file, delimiter=delimiter)

    # setup an empty list
    parsed_data = []

    # skip over the first line of the file for the headers
    fields = csv_data.next()

    """iterate over each row of the csv file, zip together
       field -> value """
    write_file = open('../data/crabs.csv', 'a')
    writer = csv.writer(write_file, delimiter=",")
    for row in csv_data:
        if row[2] == "37.98058" and row[3] == "140.0957":
            writer.writerow([row[1], row[2], row[3],row[4],row[5], row[6], row[7]])


def graph():
    #parse(MY_FILE, ",")
    data = np.recfromcsv('../data/crabs.csv')
    frozen = []
    thawed = []
    x = []
    i = 1
    for row in data:
        frozen.append(row['frozen'])
        thawed.append(row['thawed'])
        x.append(i)
        i += 1
    # create the figure
    fig = plt.figure(figsize=(7, 3))

    plt.title('frozen days vs thawed days')
    plt.plot(x,frozen,color='#669999')
    plt.plot(x, thawed, color='#0099ff')

    fig.savefig('frozenVSthawed.png')


def main():
    graph()


if __name__ == "__main__":
    main()
