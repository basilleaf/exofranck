import os.path
import csv
import requests
import jinja2
import collections
from make_bitly_links import all_slugs
from json import dumps, loads
from time import sleep
from random import randint
from secrets import WP_USER, WP_PW, WP_XMLRPC_URL
from wordpress_xmlrpc import Client, WordPressPost
from wordpress_xmlrpc.methods.posts import NewPost, GetPosts, EditPost
from wordpress_xmlrpc.compat import xmlrpc_client
from wordpress_xmlrpc.methods import media
import urllib, cStringIO

debug = False

wp = Client(WP_XMLRPC_URL, WP_USER, WP_PW)
all_posts = wp.call(GetPosts({'number':500}))

# column labels for the iau csv
iau_labels = ['star','lookUP_name','planet','Jup_mass','Earth_mass','Period_day','semi_ajor_axis_au','discovered_year','Constellation_en','Visibility','V_magnitude']

def get_wp_post_id(slug):

    for p in all_posts:
        if p.slug == slug:
            return p.id
    return False


def add_or_edit_wp_post(title, content, slug, more_info_url, local_img_file):

    # first upload the image
    if local_img_file:
        data = {
            'name': local_img_file.split('/')[-1],
            'type': 'image/jpg',  # mimetype
        }

        # read the binary file and let the XMLRPC library encode it into base64
        with open(local_img_file, 'rb') as img:
            data['bits'] = xmlrpc_client.Binary(img.read())
        response = wp.call(media.UploadFile(data))
        attachment_id = response['id']

    # now post the post and the image
    post = WordPressPost()
    post.post_type = 'post'  # stupid effing theme
    post.title = title
    post.content = content
    post.post_status = 'publish'
    post.slug = slug

    if local_img_file:
        post.thumbnail = attachment_id

    if not get_wp_post_id(slug):
        # this is a new post
        wp.call(NewPost(post))
        msg = "posted"

    else:
        # this post exists, update it
        post.id = get_wp_post_id(slug)
        wp.call(EditPost(post.id, post))
        msg = "edited"

    print "%s %s as %s" % (msg, title, post.slug)


def get_planet_status(star_slug):
    """ returns the 3rd column of short_urls.csv for this star, which
        indicates how many planets need names and whether star needs name too
        """
    with open('short_urls.csv') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            star = row[1].split('/').pop()
            if star_slug == star:
                return row[2].strip()

def fetch_all_images_from_lookUP():
    """ this missed the list below (twice) but they do exist
    """
    # all_slugs = all_slugs()
    all_slugs = ['bd-10-3166',
                'bd-17-63',
                'corot-2',
                'corot-4',
                'moa-2007-blg-192-l',
                'moa-2007-blg-400-l',
                'ogle-05-071l',
                'ogle-05-169l',
                'ogle-05-390l',
                'ogle235-moa53',
                'ogle2-tr-l9',
                'ogle-tr-10',
                'ogle-tr-111',
                'ogle-tr-113',
                'ogle-tr-132',
                'ogle-tr-182',
                'ogle-tr-211',
                'ogle-tr-56',
                'wasp-11-hat-p-10',
                'ogle-06-109l',
                'ogle-06-109l',
                'psr-1257-12',
                'psr-1257-12',
                'psr-1257-12']
    for slug in all_slugs:

        # fetch the lookUP json feed
        lookUP_name = slug.replace('-','+')
        url = "http://www.strudel.org.uk/lookUP/json/?name=%s" % lookUP_name
        lookUP_json = loads(requests.get(url).text)

        # wikisky image
        try:
            img = lookUP_json['image']['src']
            file = cStringIO.StringIO(urllib.urlopen(img).read())
            img = Image.open(file)
            img.save('images/%s.jpeg' % slug)

        except KeyError:
            print "no image for %s" % slug

def get_planets(slug):
    planets = []
    for this_planet in get_iau_list():
        if slug == this_planet['star'].strip().lower().replace(' ','-'):
            planets.append(this_planet)

    return planets



def create_the_content(this_planet):

    templateLoader = jinja2.FileSystemLoader( searchpath="/" )
    templateEnv = jinja2.Environment( loader=templateLoader )
    TEMPLATE_FILE = "/users/lballard/projects/exofranck/post_template.html"
    template = templateEnv.get_template( TEMPLATE_FILE )

    context = {}
    context['title'] = this_planet['star']
    context['star'] = this_planet['star']
    context['slug'] = context['star'].strip().lower().replace(' ','-')
    context['this_planet'] = this_planet

    # planet count/star naming status
    planet_status = get_planet_status(context['slug'])
    star_needs_name = True
    if planet_status == '1-sans-star':
        planet_count = 1
        star_needs_name = False
    else:
        planet_count = int(planet_status)

    context['planet_count'] = planet_count
    context['star_needs_name'] = star_needs_name

    # fetch the lookUP json feed
    lookUP_name = this_planet['lookUP_name'].replace(' ','+')
    url = "http://www.strudel.org.uk/lookUP/json/?name=%s" % lookUP_name
    lookUP_json = loads(requests.get(url).text)

    # wikisky image
    try:
        context['wikisky_link'] = lookUP_json['image']['href']
        context['wikisky_src'] = lookUP_json['image']['src']
    except KeyError:
        print "no image for %s" % this_planet

    # virtualsky embed
    try:
        ra = lookUP_json['ra']['decimal']
        dec = lookUP_json['dec']['decimal']
        star = this_planet['lookUP_name'].replace(' ', '+')
        embed_url = "http://lcogt.net/virtualsky/embed/?projection=gnomic&ra=%s&dec=%s&showdate=false&showposition=false&constellationlabels=true&constellationboundaries=true&fov=50&objects=%s" % (ra, dec, star)
        context['virtualsky_url'] = embed_url
    except KeyError:
        print "no image for %s" % this_planet

    context['simbad_link'] = "http://simbad.u-strasbg.fr/simbad/sim-basic?Ident=%s&submit=SIMBAD+search" % lookUP_name
    context['simbad_link'] = "http://simbad.u-strasbg.fr/simbad/sim-basic?Ident=%s" % lookUP_name

    context['planets'] = get_planets(context['slug'])

    content = template.render(context)

    content = ' '.join([s.strip() for s in content.splitlines()]).strip()

    return context['slug'], context['title'], content


def get_iau_list():
    with open('iau_list.csv') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:

            this_planet = dict(zip(iau_labels, row))
            yield this_planet


def post_all_systems():
    c = 0

    posted = []
    for this_planet in get_iau_list():

        slug, title, content = create_the_content(this_planet)

        if slug in posted:
            continue  # this has already been posted

        posted.append(slug)

        # check for an image
        image_file = ''
        img_path = "images/%s.jpeg" % slug
        if os.path.isfile(img_path):
            image_file = img_path

        image_file = ''  # just editing posts at this point, no new ones
        add_or_edit_wp_post(title, content, slug, '', image_file)

        print "http://exoplanets.seti.org/%s" % slug

        if debug: break

        c = c + 1
        if c > 25:
            timer = 60*randint(1, 3)
            print "sleeping... %s" % str(timer/60)
            sleep(timer)
            c = 0


if __name__ == "__main__":
    post_all_systems()
    print "Bye!"

