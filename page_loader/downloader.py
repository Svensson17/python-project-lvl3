import requests
from urllib.parse import urlparse
import re


def download(url, path):
    result = requests.get(url)
    html = result.text
    with open('url', 'w') as file:
        file.write(html)
    parced_url = urlparse(url)
    file_name = parced_url.netloc
    new_file_name = re.sub(r'([^a-zA-Z0-9])', '-', file_name)
    result = path + new_file_name + '.html'
    return result





