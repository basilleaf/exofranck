import csv
import collections
from make_bitly_links import all_slugs
"""
the short_urls.csv needs a field to indicate how many planets in this system
after short_urls.csv is created, run this to add that column
"""

# for each url in the original urls list
stars = []
all_slugs = all_slugs()  # slug for each star

counter=collections.Counter(all_slugs)

stars = []
with open('short_urls.csv.bak') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        star = row[1].split('/').pop()
        count = counter[star]
        row.append(str(count))
        print (',').join(row)

