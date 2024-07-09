# One blog uses two hyphens (--) as separators between articles,
# so the usual rule of 3 or more cannot be used here. Two doesn't work either
# because they are used in texts as well.

# Mostly this script will use functions from the blogs_separation.py file,
# but the separate() function has to be written differently for this one blog.

import os
import re
from string import punctuation

from useful_items import TIMEZONES, MONTHS, WEEKDAYS
from blogs_separation import get_body_link, convert_into_GMT

months = list(MONTHS.keys())
tz = list(TIMEZONES.keys())

ampm = [
    'am',
    'pm',
    'a\.m\.',
    'p\.m\.'
]

def separate3(blog):
    '''
    Take body of a blog article as input and separate into subarticles

    Regularity that I use:
        - weekday as beginning
        - stop before weekday of the next one
    '''
    parts = [blog]
    for mo in ['Oct.', 'Nov.']:
        for weekday in WEEKDAYS:
            for i, article in enumerate(parts):
                parts[i] = article.split(f'{weekday}, {mo}')
            parts = [item for sublist in parts for item in sublist]
    # first item in parts list is the text before the first article
    return parts

def new_article2(text:str, year:int):
    '''
    Create a new article out of a piece of text extracted with the function above (separate())
    '''
    month_day = re.findall(f'(?:{"|".join(months)})[\s|\S][0-9]*', text)[0]
    day = re.findall('([0-9]+)', month_day)[0]
    month: str = month_day[:-len(day)-1]
    title: str = re.findall('\s{2,50}(.+?)\s{2}', text)[0]
    title.strip()
    try:
        t_zone = re.findall(f'({"|".join(tz)})', text)[0]
    except IndexError:
        t_zone = 'GMT'
    full_time:str = re.findall(f'{day}[,|.]* (.*?) [{t_zone}|\s\s]', text)[0]
    # In cases of full-hour times (e.g. 11am), I might have
    # done some manual adjustments in the article files...
    time:str = re.findall('([0-9]*[.|:][0-9]*)', full_time)[0]
    am_pm = full_time[len(time):].strip()
    # sometimes there's a dot instead of a colon
    time = time.replace('.', ':')
    hour, minute = time.split(':')
    hour = int(hour)
    minute = int(minute)
    if 'p' in am_pm:
        hour += 12
    day = int(day)
    date, time = convert_into_GMT(year, month, day, hour, minute, t_zone)
    body = text[text.find(title)+len(title)+1:]
    return title, date, time, body

if __name__ == '__main__':
    # current directoy
    drt = os.getcwd()
    # directory of blog
    blogpath = os.path.join(drt, 'articles/removed/blogs/')
    # directory to save the separated articles
    destination_known = os.path.join(drt, 'articles/article_text/')

    # separate etc.
    body, link = get_body_link(
        '2019-10-30 Catch up on the China Fisheries and Seafood Expo.txt',
        blogpath
    )
    # Also done on the articles below. Needed some manual adjustments
    # 2018-6-3 Tuna 2018 blog Recap on three busy days in Bangkok.txt
    # 2018-6-3 Thaifex 2018 blog Tuna and shrimp suppliers step away from EU markets.txt
    # 2020-1-21 Global Seafood Marketing Conference Strong shrimp farmed salmon outlook plantbased pro.txt
    # 2018-6-15 AquaVision 2018 Move over salmon Its time for shrimp.txt
    # 2018-6-22 SeaWeb Seafood Summit 2018 blog The feed of the future.txt
    # 2019-3-12 North Atlantic Seafood Forum RoundUp Radical salmon farming concepts Mowi name change .txt
    # 2016-1-22 GSMC 2016 blog Whitefishs social issues.txt
    # 2017-1-24 GSMC 2017 blog Recap on all the news from the event.txt
    # 2017-9-13 IntraFish Seafood Investor Forum Is diversification key for attracting investments.txt
    # 2017-9-19 World Seafood Congress 2017 blog Certification digitization and opening new markets.txt
    # 2017-3-13 North Atlantic Seafood Forum Recap on all the news from the event.txt
    # 2017-10-12 Humber Seafood Summit 2017 How do we sell more fish.txt
    # 2017-11-7 China show blog Ecuadorian shrimp prices hike 15 ahead of Chinese New Year.txt
    # 2018-9-18 IntraFish Investor Forum Recap on a full day of talks.txt
    # 2016-3-9 Boston Show blog Recap on three hectic days here.txt
    # 2019-10-30 Catch up on the China Fisheries and Seafood Expo.txt
    parts = separate3(body)
    for part in parts:
        part = part.strip()
        if part[0] == '3':
            part = "Oct. " + part
        elif part[0] == "1":
            part = "Nov. " + part
        title, date, time, body = new_article2(part, 2016)
        # remove punctuation from title for correct saving
        f_title = ''.join([c for c in title if c not in punctuation])
        filename = f'{date.strip()} {f_title.strip()}.txt'
        print(filename)
        print(date, time)
        print(title)
        print(body)
        print('\n')
        if len(filename) > 100:
            filename = filename[:96] + '.txt'
        with open(os.path.join(destination_known, filename), 'w') as fn:
            fn.write(f'DATE: {date} {time}\n')
            fn.write(f'TITLE: {title}\n')
            fn.write(f'LINK: {link}\n')
            fn.write(f'LEAD: \n')
            fn.write(f'BODY: {body}')