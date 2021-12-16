from page_loader.parsering import parse_data

from page_loader.downloader import download


def main():
    args = parse_data()
    result = download(
        args.url,
        args.path,
    )
    print(result)


if __name__ == "__main__":
    main()