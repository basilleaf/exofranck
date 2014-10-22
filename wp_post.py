import csv
from time import sleep
from random import randint
from secrets import WP_USER, WP_PW, WP_XMLRPC_URL
from wordpress_xmlrpc import Client, WordPressPost
from wordpress_xmlrpc.methods.posts import NewPost
from wordpress_xmlrpc.compat import xmlrpc_client
from wordpress_xmlrpc.methods import media


def post_to_wordpress(title, content, slug, more_info_url, local_img_file):

    wp = Client(WP_XMLRPC_URL, WP_USER, WP_PW)

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

    wp.call(NewPost(post))

    print "posted " + title + " as " + post.slug

def post_all_planets():
    c = 0
    labels = ['star','planet','Jup_mass','Earth_mass','Period_day','semi_ajor_axis_au','discovered_year','Constellation_en','Visibility','V_magnitude']
    with open('iau_list.csv') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            this_planet = dict(zip(labels, row))

            title = this_planet['planet']

            slug = title.strip().lower().replace(' ','-')

            content = "<dl>"
            for k,v in this_planet.items():
                content += "<dt>%s:</dt><dd> %s </dd>" % (k, v)
            content += "</dl>"

            post_to_wordpress(title, content, slug, '', '')

            # post 10 at a time then pause for a few minutes
            c = c + 1
            if c > 25:
                print "sleeping..."
                sleep(60*randint(1, 10))
                c = 0


if __name__ == "__main__":
    post_all_planets()

