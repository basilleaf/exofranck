import qrcode
import csv
import os

def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as ex:
        if ex.errno!=errno.EEXIST:
            raise

def make_codes():
    with open('short_urls.csv') as csvfile:
        reader = csv.reader(csvfile)
        for short_url,long_url,count in reader:
            path = long_url.replace('http://exoplanets.seti.org/','')
            img = qrcode.make(short_url)
            img.save('qrcodes/%s.png'%path)

if __name__ == "__main__":
    mkdir_p('qrcodes')
    make_codes()
