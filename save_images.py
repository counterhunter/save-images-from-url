from bs4 import BeautifulSoup
from pathlib import Path
import requests
import os
import datetime

from urllib.parse import urlparse, unquote
from os.path import basename


def url_to_name(url):
    return basename(unquote(urlparse(url).path))


# GENERATE OUTPUT FOLDER NAME
def gen_folder_name():
    
    # get time now
    time = datetime.datetime.now()
    folder_name = time.strftime("%d.%m.%Y, %Hh%Mm%Ss")

    return folder_name


# CREATE OUTPUT FOLDER
def folder_create(folder_name):
    
    # folder creation
    folder_path = Path(__file__).parent.resolve() / folder_name
    os.mkdir(folder_path)

    return Path(folder_path)


# DOWNLOAD ALL IMAGES FROM THAT URL
def download_images(urls):

    headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:100.0) Gecko/20100101 Firefox/100.0'}
    count = 0
 
    # print total images found in URL
    # print(f"Total {len(images)} Image Found!")
    
    for url in urls:
        
        r = requests.get(url, headers=headers)
        if r.ok:
            yield r.content


def save_images(images, path):

    for name, bytes in images:
        print(path / name)
        with open(path / name, "wb+") as f:
            f.write(bytes)


# MAIN FUNCTION START
def main():

    # content of URL
    r = requests.get("https://a2b2.org/")

    if r.ok:

        # Parse HTML Code
        soup = BeautifulSoup(r.text, 'html.parser')
    
        # find all images in URL
        urls = [i["src"] for i in soup.findAll('img')]
        names = [url_to_name(u) for u in urls]
    
        # Call folder create function
        folder_name = gen_folder_name()
        path = folder_create(folder_name)
        
        # Download images
        images = zip(names, download_images(urls)) 
        save_images(images, path)
 

# CALL MAIN FUNCTION
main()
