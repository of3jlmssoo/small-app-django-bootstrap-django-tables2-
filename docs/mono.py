import csv
import random

with open('./FEK_download.csv', encoding='shift_jis') as f:
    reader = csv.reader(f)
    l = [row for row in reader]

print(len(l))
while True:
    print(l[random.randint(0, len(l) - 1)][1])
    input()
