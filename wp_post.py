import csv
import requests
import jinja2
from json import dumps, loads
from time import sleep
from random import randint
from secrets import WP_USER, WP_PW, WP_XMLRPC_URL
from wordpress_xmlrpc import Client, WordPressPost
from wordpress_xmlrpc.methods.posts import NewPost, GetPosts, EditPost
from wordpress_xmlrpc.compat import xmlrpc_client
from wordpress_xmlrpc.methods import media

wp = Client(WP_XMLRPC_URL, WP_USER, WP_PW)
all_posts = wp.call(GetPosts({'number':500}))

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


def create_the_content(this_planet):

    templateLoader = jinja2.FileSystemLoader( searchpath="/" )
    templateEnv = jinja2.Environment( loader=templateLoader )
    TEMPLATE_FILE = "/users/lballard/projects/exofranck/post_template.html"
    template = templateEnv.get_template( TEMPLATE_FILE )

    context = {}
    context['title'] = this_planet['planet']
    context['slug'] = context['title'].strip().lower().replace(' ','-')
    context['this_planet'] = this_planet

    # fetch the lookUP json feed
    lookUP_name = this_planet['lookUP_name'].replace(' ','+')
    url = "http://www.strudel.org.uk/lookUP/json/?name=%s" % lookUP_name
    lookUP_json = loads(requests.get(url).text)

    # wikisky image
    context['wikisky_link'] = lookUP_json['image']['href']
    context['wikisky_src'] = lookUP_json['image']['src']

    # virtualsky embed
    ra = lookUP_json['ra']['decimal']
    dec = lookUP_json['dec']['decimal']
    star = this_planet['lookUP_name'].replace(' ', '+')
    embed_url = "http://lcogt.net/virtualsky/embed/?projection=gnomic&ra=%s&dec=%s&showdate=false&showposition=false&constellationlabels=true&constellationboundaries=true&fov=50&objects=%s" % (ra, dec, star)
    context['virtualsky_url'] = embed_url

    content = template.render(context)

    return context['slug'], context['title'], content


def get_iau_list():
    labels = ['star','lookUP_name','planet','Jup_mass','Earth_mass','Period_day','semi_ajor_axis_au','discovered_year','Constellation_en','Visibility','V_magnitude']
    with open('iau_list.csv') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:

            this_planet = dict(zip(labels, row))
            yield this_planet


def post_all_planets():
    c = 0

    for this_planet in get_iau_list():

        slug, title, content = create_the_content(this_planet)

        add_or_edit_wp_post(title, content, slug, '', '')

        print "http://exoplanets.seti.org/%s" % slug

        c = c + 1
        if c > 25:
            timer = 60*randint(1, 3)
            print "sleeping... %s" % str(timer/60)
            sleep(timer)
            c = 0


if __name__ == "__main__":
    post_all_planets()
    print "Bye!"

