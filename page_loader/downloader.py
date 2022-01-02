import requests
from urllib.parse import urlparse
import re
from bs4 import BeautifulSoup
import os
import logging


def download(url, path=''):
    request = requests.get(url)
    logging.info('Request done {}'.format(url))
    response = request.text
    complete_file = get_file_name(url)
    folder_files_name = get_dir_name(url)
    full_path = os.path.join(os.getcwd(), path)
    file_path = full_path + complete_file
    asset_path = full_path + folder_files_name
    if not os.path.isdir(asset_path):
        os.mkdir(asset_path)
    html = download_resource(response, url, asset_path, folder_files_name)
    with open(file_path, 'w') as file:
        file.write(html)
    return file_path


def download_resource(response, url, my_path, folder_files_name):
    soup = BeautifulSoup(response, 'html.parser')
    tags = soup.find_all(['script', 'img', 'link'])
    for tag in tags:
        if find_attribute(tag) == 'href':
            short_url = tag.get('href')
        else:
            short_url = tag.get('src')
        if short_url is None:
            continue
        full_url = url + short_url
        if urlparse(short_url).netloc:
            continue
        request = requests.get(full_url)
        edited_url = urlparse(full_url).netloc + urlparse(full_url).path
        new_file_name = get_file_name(edited_url)
        name = os.path.join(my_path, new_file_name)
        with open(name, 'wb') as file:
            file.write(request.content)
        tag['src'] = folder_files_name + '/' + new_file_name
        tag['href'] = folder_files_name + '/' + new_file_name
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
