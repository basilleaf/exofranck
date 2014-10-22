import csv
import urllib2

with open('short_urls.csv') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        for url in row:
          f = urllib2.urlopen(urllib2.Request(url))
          print "ok: %s" % url

print "All links ok, Bye!"