import csv

term_list = []

with open('term_report.csv') as file:
    reader = csv.reader(file)
    for row in reader:
        term_list.append(row)  # noqa: E101

print(term_list[1])
