import argparse


def parse_data():
    parser = argparse.ArgumentParser(description='Page download')
    parser.add_argument('url')
    parser.add_argument('-o', dest='path')
    return parser.parse_args()
