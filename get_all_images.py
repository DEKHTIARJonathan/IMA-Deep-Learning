"""
Required packages
- flickrapi
- requests
- wget
"""

import deepsix.collection
from deepsix.collection import *

if __name__ == '__main__':
    human_urls = deepsix.collection.flickr.urls_tagged('human', max_images=4, apikey='Flickr_API_key.txt')
    human_urls += deepsix.collection.imagenet.urls_tagged('n07942152', max_images=5)
    deepsix.collection.get_images_from_urls(human_urls, output_folder='downloads')
