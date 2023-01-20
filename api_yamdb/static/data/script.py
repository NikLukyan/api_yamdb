import csv

# with open("genre.csv", newline='', encoding='utf-8') as csvfile:
#     reader = csv.DictReader(csvfile, delimiter=",")
#
#     for row in reader:
#         print(dict(row))

with open("genre.csv", newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile, dialect='excel', delimiter=",")

    for line in reader:
        print(line)
