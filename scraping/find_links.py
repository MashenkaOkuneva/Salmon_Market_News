# Find the links to all relevant articles in intrafish.com.
# Search: Salmon
# dates: 01/01/2010 - 25/08/2022
# sections: Salmon, Salmon, Finance, Prices, finance
# all tags

import os
import requests
import bs4
from time import sleep
import random

# first search page
url_wo_offset = "https://www.intrafish.com/archive/?q=salmon&sort=agea&publishdate=01.01.2010-25.08.2022&othersections=Salmon&othersections=Finance&othersections=%5C%20Salmon&othersections=Prices&othersections=finance"
# for following pages of search result, iterate through offset values
# keep it here only for safety
url_w_offset = "https://www.intrafish.com/archive/?offset=10&q=salmon&sort=agea&publishdate=01.01.2010-25.08.2022&othersections=Salmon&othersections=Finance&othersections=%5C%20Salmon&othersections=Prices&othersections=finance"

auth = 'mikaella.zitti@nmbu.no'

def main():
    # current directory
    cur_dir = os.getcwd()
    # path to file with all links
    links_file = os.path.join(cur_dir, 'articles/links.txt')
    with open(links_file, 'w') as f:
        # first page
        page = requests.get(url_wo_offset, auth=(auth, auth))
        soup = bs4.BeautifulSoup(page.content, 'html.parser', from_encoding=page.encoding)
        cards = soup.find_all('div', class_='card-body')

        links = []
        for card in cards:
            link = card.find('a', {'class': 'card-link text-reset'})['href']
            links.append(f'https://www.intrafish.com{link}')

        f.write('\n'.join(links) + '\n')
        print('First page done.')
        sleep(5)

        # following pages
        for off in range(10, 5740, 10):
            url = f"https://www.intrafish.com/archive/?offset={off}&q=salmon&sort=agea&publishdate=01.01.2010-25.08.2022&othersections=Salmon&othersections=Finance&othersections=%5C%20Salmon&othersections=Prices&othersections=finance"
            page = requests.get(url, auth=(auth, auth))
            soup = bs4.BeautifulSoup(page.content, 'html.parser', from_encoding=page.encoding)
            cards = soup.find_all('div', class_='card-body')

            links = []
            for card in cards:
                link = card.find('a', {'class': 'card-link text-reset'})['href']
                links.append(f'https://www.intrafish.com{link}')

            f.write('\n'.join(links) + '\n')
            print(f'Page {int(off/10 + 1)} done.')
            sleep(abs(random.gauss(10, 2.3)))

if __name__ == '__main__':
    main()