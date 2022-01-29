from page_loader.parsering import parse_data
from page_loader.downloader import download
import logging
import sys


def main():
    args = parse_data()
    logging.basicConfig(level=logging.INFO)
    try:
        result = download(
            args.url,
            args.path
        )
        print(result)
    except Exception as e:
        logging.error(e)
        sys.exit(1)


if __name__ == "__main__":
    main()
