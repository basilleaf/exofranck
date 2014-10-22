import csv
import urllib2

def check_all_links():
    with open('short_urls.csv') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            for url in row:
                try:
                    urllib2.urlopen(urllib2.Request(url))
                    print "ok: %s" % url
                except:
                    print "not found --> %s " % url
                    return

    print "All links ok, Bye!"

if __name__ == "__main__":
    check_all_links()