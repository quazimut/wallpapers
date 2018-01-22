#!/usr/bin/env python3
# coding=utf-8
#
# Copyright 2018, Mice Pápai
# Created: 2018.01.22. 12:39
#
import os.path
from concurrent.futures import ThreadPoolExecutor
from pprint import pprint

import flickrapi

from util import print_progress, get_files

__author__ = 'Mice Pápai'
__copyright__ = 'Copyright 2018, Mice Pápai'
__credits__ = ['Mice Pápai <mice@gorbekor.hu>']
__license__ = 'All rights reserved'
__version__ = '0.1.0'


with open('.keys') as f:
    api_key, api_secret = f.read().split('\n')[:2]


flickr = flickrapi.FlickrAPI(api_key, api_secret, format='parsed-json')


def authenticate():
    if not flickr.token_valid(perms='write'):
        flickr.get_request_token(oauth_callback='oob')

        authorize_url = flickr.auth_url(perms='write')
        print(authorize_url)

        verifier = str(input('Verifier code: '))

        flickr.get_access_token(verifier)


class FileWithCallback(object):
    def __init__(self, filename, callback):
        self.file = open(filename, 'rb')
        self.callback = callback
        self.len = os.path.getsize(filename)
        self.fileno = self.file.fileno
        self.tell = self.file.tell

    def read(self, size):
        if self.callback:
            self.callback(self.tell() * 100 // self.len)
        return self.file.read(size)


def cb(progress):
    print_progress(progress, 100)


def steema(user):
    return f'<a href="https://steemit.com/@{user}">@{user}</a>'


def upload_img(filename):
    params = {'filename':    filename,
              'title':       filename.split('/')[-1].split('.')[0].replace('-',
                                                                           ' '),
              'description': f'made by {steema("zsh")} and {steema("balzss")}',
              'tags':        'zsh balzss wallpaper "a s"',
              # space delimited / quoted
              'is_public':   1,
              'is_family':   1,
              'is_friend':   1,
              'format':      'etree'}

    params['fileobj'] = FileWithCallback(params['filename'], cb)

    rsp = flickr.upload(**params)
    for child in rsp:
        return child.text  # ugly but works :)))


def get_info(photo_id):
    info = flickr.photos.getInfo(photo_id=photo_id)
    title = info['photo']['title']['_content']
    page_url = info['photo']['urls']['url'][0]['_content']
    sizes = flickr.photos.getSizes(photo_id=photo_id)
    raw_url = sizes['sizes']['size'][-1]['source']
    return {'title':    title,
            'page_url': page_url,
            'raw_url':  raw_url}


def gen_md_link(photo_info):
    parts = []
    device, color, variant, size = photo_info['title'].split(' ')

    if device == 'mobile':
        if size == '1080':
            if variant == 'large':
                parts.append(f'\n<h3>{device.title()} {color.title()}</h3>\n')
            parts.append(f'<div class="pull-{"left" if variant == "large" else "right"}"><img src="{photo_info["raw_url"]}"></div>')
            parts.append(f'<div class="pull-{"left" if variant == "large" else "right"}">Download: <a href="{photo_info["page_url"]}">{size}p</a>  // ')
        elif size == '1440':
            parts.append(f'<a href="{photo_info["page_url"]}">{size}p</a>  // ')
        else:
            parts.append(f'<a href="{photo_info["page_url"]}">4K</a></div>\n{"<hr/>" if variant == "small" else ""}')
    else:
        if size == '1080':
            parts.append(f'### {device.title()} {color.title()} {variant.title()}\n')
            parts.append(f'![{photo_info["title"]}]({photo_info["raw_url"]})\n')
            parts.append(f'Download: [{size}p]({photo_info["page_url"]}) // ')
        elif size == '1440':
            parts.append(f'[{size}p]({photo_info["page_url"]}) // ')
        else:
            parts.append(f'[{size}]({photo_info["page_url"]})\n\n')

    return ''.join(parts)


def main():
    authenticate()
    files = get_files('to_upload')
    files.remove('to_upload/.gitkeep')
    pprint(files)

    futures = []
    with ThreadPoolExecutor(max_workers=4) as e:
        for filename in files:
            futures.append(e.submit(upload_img, filename))

    markdown = ''.join(gen_md_link(get_info(fut.result())) for fut in futures)

    with open('article.md', 'w') as f:
        f.write(markdown)


if __name__ == '__main__':
    main()
