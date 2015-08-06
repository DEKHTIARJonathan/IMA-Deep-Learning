import flickrapi
import flickrapi.shorturl as short_url
import wget
import subprocess


def grabKeys(filename):
    '''
    Grab the flickr api keys from an external file. Use it to start up an
    instance of the Flickr API.
    '''
    api_key_file = open(filename)
    api_keys = api_key_file.readlines()
    api_key = api_keys[0].rstrip()
    api_secret = api_keys[1].rstrip()
    flickr = flickrapi.FlickrAPI(api_key, api_secret)

    return flickr


def searchImages(flickr, keywords, image_num):
    '''
    Search for images via the API based on given keywords, return a list
    of a given number of URLs for those keywords.
    '''

    # walk through a search query until we reach image_num images
    i = 0
    image_urls = []
    for photo in flickr.walk(tag_mode='all', tags=keywords):
        if i == image_num:
            break
        photo_id = photo.get('id')
        image_urls.append(short_url.url(photo_id))
        i += 1

    return image_urls


def getImages(image_urls):
    '''
    Download a list of images from urls with wget.
    '''
    for url in image_urls:
        filename = wget.download(url)

        # parse the image url from the website HTML
        bookend_1 = '<meta property="og:image" content="'
        bookend_2 = '"  data-dynamic="true">'
        with open(filename, 'r') as html_file:
            html = html_file.read()
            html_buf = html.split(bookend_1)[1]
            pic_url = html_buf.split(bookend_2)[0]
            pic_url = pic_url.rstrip()

        pic_file = wget.download(pic_url)
        subprocess.call(['mv', pic_file, 'flickr_images/' + pic_file])
        subprocess.call(['rm', filename])


if __name__ == '__main__':

    # test parameters
    flickr = grabKeys('../Flickr_API_key.txt')
    human_urls = searchImages(flickr, 'human', 4)
    getImages(human_urls)
