# articles in blogs that had '--' in the title had only the part before the '--'
# in the title, the rest of the title was in the body. This script fixes that.

import os
import re
import csv
from string import punctuation

from blogs_separation import get_body_link, convert_into_GMT, new_article
from useful_items import TIMEZONES, MONTHS, WEEKDAYS, DAYSPERMONTH

cur_dir = os.getcwd()
blogs_dir = os.path.join(cur_dir, 'articles/removed/blogs')
articles_dir = os.path.join(cur_dir, 'articles/article_text/')
csv_path = str(cur_dir).replace('scraping', 'analysis')


months = list(MONTHS.keys())
tz = list(TIMEZONES.keys())

ampm = [
    'am',
    'pm',
    'a\.m\.',
    'p\.m\.'
]

# same function as in blog separation file, but without the removal of the names
# this is where the errors originally happened
def separate2(body:str):
    '''
    Take body of a blog article as input and separate into subarticles

    Regularity that I use:
        - weekday
        - something in between that I capture
        - a number of ----, often >>10, but not always
    '''
    # define pattern
    pattern = f'([{"|".join(WEEKDAYS + months)}].*?)---'

    # find all occurences
    parts: list[str] = re.findall(pattern, body)
    return parts

blogs = ['2020-1-21 Global Seafood Marketing Conference Strong shrimp farmed salmon outlook plantbased pro.txt'] #os.listdir(blogs_dir)

def fix_affected_articles():
    '''
    Count the number of articles that are affected by the bug
    '''
    #with open(os.path.join(csv_path, 'corrected_titles.csv'), 'w') as f:
        #writer = csv.writer(f)
    for blog in blogs:
        year = int(blog[:4])
        body, _ = get_body_link(blog, blogs_dir)
        parts = separate2(body)
        for part in parts:
            try:
                title, date, time, body = new_article(part, year)
                print(
                    title,
                    date,
                    time,
                    body,
                    '\n'
                )
            except IndexError:
                pass
            if '--' in title:
                # current file name (until --)
                cur_file_name = f"{date} {title.split('--')[0].strip()}.txt"
                    #writer.writerow([cur_file_name, title])
    return None

if __name__ == '__main__':
    fix_affected_articles()