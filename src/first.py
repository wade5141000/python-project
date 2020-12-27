import csv

with open('src/data/USvideos.csv', newline='', encoding='utf-8') as csvfile:

    rows = csv.reader(csvfile)
    headers = next(rows)
    row1 = next(rows)
    print(headers)
    print(row1[7])

    
    
