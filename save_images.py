#!/usr/bin/env python3

from argparse import ArgumentParser
from bs4 import BeautifulSoup
from datetime import datetime
from pathlib import Path
from requests import get
from urllib.parse import urljoin, urlparse, unquote_plus

A2B2_URL = 'https://a2b2.org/'

argparser = ArgumentParser('save_images.py')
argparser.add_argument(
    'outpath',
    metavar='PATH',
    help='output directory',
    default=Path(datetime.now().strftime('%Y.%d.%m %H-%M-%S')),
    type=Path,
    nargs='?'
)

args = argparser.parse_args()
soup = BeautifulSoup(get(A2B2_URL).text, 'html.parser')
outpath = args.outpath

print(f'Downloading in {outpath}')
outpath.mkdir(parents=True, exist_ok=True)
section = soup.find('section', id='block-system-main')
urls = [unquote_plus(img['src']) for img in section.find_all('img')]

for url in urls:
    name = Path(urlparse(url).path).name # yeap
    url = urljoin(A2B2_URL, url)
    print(f'Downloading {name}... ', end='')
    bytes = get(url, headers={'User-Agent': '(X11)'}).content
    with open(outpath / name, 'wb') as f:
        f.write(bytes)
        print(f'ok!')
