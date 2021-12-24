import requests
from urllib.parse import urlparse
import re
from bs4 import BeautifulSoup
import os


def download(url, path):
    request = requests.get(url)
    response = request.text
    parsed_url = urlparse(url)
    edited_url = parsed_url.netloc
    folder_files_name = make_new_file_name(edited_url) + '_files'
    my_path = os.getcwd()
    my_path = os.path.join(my_path, folder_files_name)
    if not os.path.isdir(folder_files_name):
        os.mkdir(folder_files_name)
    complete_file = path + make_new_file_name(edited_url) + '.html'
    html = download_image(response, url, edited_url, my_path, folder_files_name)
    with open(complete_file, 'w') as file:
        file.write(html)
    return complete_file


def download_image(response, url, edited_url,  my_path, folder_files_name):
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
        parsed_url = urlparse(full_url)
        edited_url = parsed_url.netloc + parsed_url.path
        new_file_name = make_new_file_name(edited_url)
        name = os.path.join(my_path, new_file_name)
        with open(name, 'wb') as file:
            file.write(request.content)
        tag['src'] = folder_files_name + '/' + new_file_name
    return soup.prettify()


def make_new_file_name(short_url):
    parsed_short_url = urlparse(short_url)
    file_name = os.path.basename(parsed_short_url.path)
    name = os.path.splitext(file_name)[0]
    extension = os.path.splitext(file_name)[1]
    new_name = re.sub(r'([^a-zA-Z0-9])', '-', name)
    return new_name + extension


def find_attribute(tag):
    if tag == 'link':
        return 'href'
    else:
        return 'src'
