import requests
from urllib.parse import urlparse, urljoin
import re
from bs4 import BeautifulSoup
import os
import logging
from progress.bar import Bar


def download(url, path=''):
    request = requests.get(url)
    logging.info('Request done {}'.format(url))
    request.raise_for_status()
    response = request.text
    complete_file = get_file_name(url)
    folder_files_name = get_dir_name(url)
    full_path = os.path.join(os.getcwd(), path)
    file_path = os.path.join(full_path, complete_file)
    asset_path = os.path.join(full_path, folder_files_name)
    if not os.path.exists(asset_path):
        os.mkdir(asset_path)
    html = download_resource(response, url, asset_path, folder_files_name)
    with open(file_path, 'w') as file:
        file.write(html)
    return file_path


def download_resource(response, url, my_path, folder_files_name):
    soup = BeautifulSoup(response, 'html.parser')
    tags = soup.find_all(['script', 'img', 'link'])
    bar = Bar('process', max=len(tags))
    for tag in tags:
        attribute_name = find_attribute(tag.name)
        short_url = tag.get(attribute_name)
        if short_url is None:
            bar.next()
            continue
        full_url = urljoin(url, short_url)
        if urlparse(full_url).netloc == urlparse(url).netloc:
            request = requests.get(full_url)
            edited_url = urlparse(full_url).netloc + urlparse(full_url).path
            new_file_name = get_file_name(edited_url)
            name = os.path.join(my_path, new_file_name)
            with open(name, 'wb') as file:
                file.write(request.content)
            tag[attribute_name] = os.path.join(folder_files_name, new_file_name)
        bar.next()
    bar.finish()
    return soup.prettify()


def make_file_name(name):
    return re.sub(r'([^a-zA-Z0-9])', '-', name)


def find_attribute(tag):
    if tag == 'link':
        return 'href'
    else:
        return 'src'


def get_file_name(url):
    filename, ext = url_to_slug_and_ext(url)
    return filename + ext


def url_to_slug_and_ext(url):
    result_url_parse = urlparse(url)
    path, ext = os.path.splitext(result_url_parse.path)
    result = make_file_name(result_url_parse.netloc + path)
    return result, ext if ext else '.html'


def get_dir_name(url):
    filename, ext = url_to_slug_and_ext(url)
    return filename + '_files'
