import argparse
import logging
import requests
import re
from bs4 import BeautifulSoup

HEADERS = {'User-agent': 'Mozilla/5.0'}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--debug', required=False, action='store_true')
    parser.add_argument('--url', required=True)
    action = parser.add_mutually_exclusive_group(required=True)
    action.add_argument('--link', action='store_true')
    action.add_argument('--version', action='store_true')
    args = parser.parse_args()

    if args.debug:
        log_level = logging.DEBUG
    else:
        log_level = logging.INFO
    logging.basicConfig(format="%(asctime)s %(levelname)s: %(message)s", level=log_level)

    server_page = requests.get(args.url, headers=HEADERS)
    soup = BeautifulSoup(server_page.content, "html.parser")
    download_links = soup.find_all('a')
    for link in download_links:
        attrs = link.attrs
        if 'aria-label' in attrs.keys() and attrs['aria-label'] == 'mincraft version':
            logging.debug(f'Found the aria-label: {attrs["aria-label"]}')
            logging.debug(f'Version Found {link.getText()}')
            name = link.get_text()
            url = attrs['href']

    if args.version:
        version_pattern = re.compile(r'(\d\.\d{1,}\.\d{1,})')
        print(version_pattern.search(name).groups()[0])
    elif args.link:
        print(url)
    pass


if __name__ == '__main__':
    main()
