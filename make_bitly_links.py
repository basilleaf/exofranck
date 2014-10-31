import csv
import bitlyapi
from time import sleep
from datetime import datetime
from secrets import BITLY_USER_ID, BITLY_API_KEY

short_url_file = "short_urls.csv"

def shrink_all_urls():
    base_url = "http://exoplanets.seti.org/"

    for slug in all_slugs():

        long_url = base_url + slug

        if long_url in open(short_url_file).read():
            continue  # this url has already been shrunkened!

        b = bitlyapi.BitLy(BITLY_USER_ID, BITLY_API_KEY)

        try:
            res = b.shorten(domain="j.mp", longUrl=long_url)

        except bitlyapi.bitly.APIError:
            # wait an hour and try again
            print "sleeping for an hour... " + str(datetime.now())
            sleep(60*60)  # bitly api limits restart hourly

            b = bitlyapi.BitLy(BITLY_USER_ID, BITLY_API_KEY)
            res = b.shorten(domain="j.mp", longUrl=long_url)

        short_url = res['url']

        with open(short_url_file, "a") as myfile:
            line = "%s,%s" % (short_url, long_url)
            print "updated csv: %s" % line
            myfile.write(line + "\n")

def all_slugs():
    with open('iau_list.csv') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            yield row[0].strip().lower().replace(' ','-')


if __name__ == "__main__":
    shrink_all_urls()
    print "Bye!"

