from page_loader.downloader import download
from page_loader.downloader import download_images

def test_loader():
    expected_html = open('./tests/fixtures/test.html', 'r').read()
    assert expected_html == download()

def test_image_loader():
    expected_item = open('./tests/fixtures/test.html', 'r').read()
    assert expected_item == download_images()





