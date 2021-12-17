import requests
from urllib.parse import urlparse
import re
from bs4 import BeautifulSoup


def download(url, path):
    request = requests.get(url)
    response = request.text
    with open('url', 'w') as file:
        file.write(response)
    parced_url = urlparse(url)
    file_name = parced_url.netloc
    new_file_name = re.sub(r'([^a-zA-Z0-9])', '-', file_name)
    result = path + new_file_name + '.html'
    return result

def download_page():
    request = requests.get(url)
    soup = BeautifulSoup(request, 'html.parser')







