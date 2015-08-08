import deepsix.collection
from deepsix.collection import *
import deepsix.anomalize
from deepsix.anomalize import *

if __name__ == '__main__':
    human_urls = deepsix.collection.flickr.urls_tagged(
        'face',
        max_images=20,
        apikey='Flickr_API_key.txt'
    )

    # human_urls += deepsix.collection.imagenet.urls_tagged(
    #     'n07942152',
    #     max_images=5
    # )

    deepsix.collection.get_images_from_urls(human_urls)
    deepsix.collection.make_square_thumbnails()
    deepsix.anomalize.add_random_lines()
