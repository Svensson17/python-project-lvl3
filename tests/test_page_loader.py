from page_loader.downloader import download


def test_loader():
    expected_html = open('./tests/fixtures/test.html', 'r').read()
    assert expected_html == download()







