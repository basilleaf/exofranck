import csv
import requests
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

    title = this_planet['planet']
    slug = title.strip().lower().replace(' ','-')

    # fetch the lookUP json feed
    lookUP_name = this_planet['lookUP_name'].replace(' ','+')
    url = "http://www.strudel.org.uk/lookUP/json/?name=%s" % lookUP_name
    lookUP_json = loads(requests.get(url).text)

    content = "<dl>"
    for k,v in this_planet.items():
        content += "<dt>%s:</dt><dd> %s </dd>" % (k, v)
    content += "</dl>"

    content += """
                <div class = "%s">
                    %s
                <div>
            """ % ('lookUP_json', str(lookUP_json))

    return slug, title, content


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

        # post 10 at a time then pause for a few minutes
        c = c + 1
        if c > 25:
            timer = 60*randint(1, 3)
            print "sleeping... %s" % str(timer/60)
            sleep(timer)
            c = 0


if __name__ == "__main__":
    post_all_planets()
    print "Bye!"

