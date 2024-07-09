# download the raw html files, to avoid losing the subscription before scraping is done

import os
import requests
import bs4
from time import sleep
from datetime import datetime
import random
from string import punctuation
punctuation.replace('-', '')

# login data
auth = ('mikaella.zitti@nmbu.no', 'mikaella.zitti@nmbu.no')

# to transform month name into number (e.g. 'January' -> 1)
# useful later when storing by dates
month_numbers = {
    'January': '1',
    'February': '2',
    'March': '3',
    'April': '4',
    'May': '5',
    'June': '6',
    'July': '7',
    'August': '8',
    'September': '9',
    'October': '10',
    'November': '11',
    'December': '12'
}
def main():
    # current directory
    cur_dir = os.getcwd()
    # path to file with all links
    links_file = os.path.join(cur_dir, 'articles/links.txt')
    # html path
    html_path = os.path.join(cur_dir, 'articles/html/')
    while True:
        # evaluate current hour to set time
        if datetime.now().hour == 2:

            # open text file with links to articles
            with open(links_file, 'r') as f:
                links = f.read().split('\n')

            # first link is a test page, remove it
            links.pop(0)
            print('\n')
            # download the html files and store
            for link in links:
                # open page
                if not bool(link):
                    continue
                page = requests.get(link, auth=auth)
                # parse with beautiful soup for easy access to title and date
                soup = bs4.BeautifulSoup(page.content, 'html.parser', from_encoding=page.encoding)
                # title and date
                title = soup.title.string.split('|')[0]
                title_filename = ''.join(c for c in title if c not in punctuation).rstrip(' ')# need to trim excessively long titles because files cannot be that long
                if len(title_filename) > 125:
                    print('title filename too long:')
                    print(title_filename)
                    title_filename = title_filename[:125]
                    print('trimmed to:')
                    print(title_filename)
                    print('\n')
                # transform date for chronological order in folder
                try: # throws error sometimes
                    date_list = soup.find('span', class_='pr-3').text.split()
                except AttributeError as ae:
                    print(ae)
                    print(f'in link: {link}')
                    print(f'title: {title}')
                    print('trying again...')
                    print('\n')
                    # sleep for a moment and the restart from the request
                    sleep(90)
                    page = requests.get(link, auth=auth)
                    soup = bs4.BeautifulSoup(page.content, 'html.parser', from_encoding=page.encoding)
                    title = soup.title.string.split('|')[0]
                    title_filename = ''.join(c for c in title if c not in punctuation).rstrip(' ')
                    date_list = soup.find('span', class_='pr-3').text.split()
                date = '-'.join(
                    [
                        date_list[2],
                        month_numbers[date_list[1]],
                        date_list[0]
                    ]
                )
                # create string out of page content
                html_str = str(page.content)
                # create file name
                filename = f'{date} {title_filename}.txt'
                # file path
                file_path = os.path.join(html_path, filename)
                # write file and save
                with open(file_path, 'w+', encoding='utf-8') as f:
                    f.write(f'DATE: {date} {date_list[3]} \n')
                    f.write(f'TITLE: {title} \n')
                    f.write(f'LINK: {link} \n')
                    f.write(f'HTML: \n {html_str}')
                # give server some time so it doesn't crash
                # extra slow because I run it in the background during daytime
                print(f'DOWNLOADED and SAVED: {date} {title_filename}')
                print('\n')
                sleep(abs(random.gauss(10, 2.5)))
            break
        # give program time not to evaluate if-condition gazillions of times
        # check only every half hour
        sleep(1800)


if __name__ == '__main__':
    main()
    print('DONE')
