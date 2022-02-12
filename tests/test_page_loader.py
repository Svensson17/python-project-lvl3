import os
from urllib.parse import urljoin
import tempfile
import pytest
from page_loader.downloader import download

HTML_FILE_NAME = 'site-com-blog-about.html'
BASE_URL = 'https://site.com/'
PAGE_PATH = '/blog/about'
PAGE_URL = urljoin(BASE_URL, PAGE_PATH)
ASSETS = [
    {
        'format': 'css',
        'url_path': '/blog/about/assets/styles.css',
        'file_name': 'site-com-blog-about-assets-styles.css',
    },
    {
        'format': 'svg',
        'url_path': '/photos/me.jpg',
        'file_name': 'site-com-photos-me.jpg',
    },
    {
        'format': 'js',
        'url_path': '/assets/scripts.js',
        'file_name': 'site-com-assets-scripts.js',
    },
    {
        'format': 'html',
        'url_path': '/blog/about',
        'file_name': 'site-com-blog-about.html',
    },
]
ASSETS_DIR_NAME = 'site-com-blog-about_files'


def get_fixture_data(filename):
    return read(get_fixtures_path(filename))


def read(filepath, mode='r'):
    with open(filepath, mode) as file:
        result = file.read()
    return result


def get_fixtures_path(filename):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(current_dir, 'fixtures', filename)


def test_page_loader(requests_mock):
    content = get_fixture_data(HTML_FILE_NAME)
    requests_mock.get(PAGE_URL, text=content)
    for asset in ASSETS:
        assets_url = urljoin(BASE_URL, asset['url_path'])
        expected_asset_path = get_fixtures_path(os.path.join('expected', ASSETS_DIR_NAME, asset['file_name']))
        expected_asset_content = read(expected_asset_path, 'rb')
        asset['content'] = expected_asset_content
        requests_mock.get(assets_url, content=expected_asset_content)
    with tempfile.TemporaryDirectory() as temp_dirname:
        assert not os.listdir(temp_dirname)
        output_file_path = download(PAGE_URL, temp_dirname)
        assert len(os.listdir(temp_dirname)) == 2
        assert len(os.listdir(os.path.join(temp_dirname, ASSETS_DIR_NAME))) == 4
        html_file_path = os.path.join(temp_dirname, HTML_FILE_NAME)
        assert html_file_path == output_file_path
        html_content = read(html_file_path)
        expected_html_content = read(output_file_path)
        assert html_content == expected_html_content


def test_storage_errors(requests_mock):
    requests_mock.get(PAGE_URL)
    with pytest.raises(Exception):
        assert download(PAGE_URL, '/sys')
        assert download(PAGE_URL, 'error')


@pytest.mark.parametrize('code', [404, 500])
def test_response_with_error(requests_mock, code):
    requests_mock.get(PAGE_URL, status_code=code)
    with tempfile.TemporaryDirectory() as temp_dirname:
        with pytest.raises(Exception):
            assert download(PAGE_URL, temp_dirname)

