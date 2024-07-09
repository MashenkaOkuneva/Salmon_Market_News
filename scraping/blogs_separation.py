# separate articles that are built as "blogs"
# They are additive as new information comes in at different times,
# so we want them separately

# use regularities in artcle structure to split them up and assign them to new dates

import os
import re
from string import punctuation

from useful_items import TIMEZONES, MONTHS, WEEKDAYS, DAYSPERMONTH

months = list(MONTHS.keys())
tz = list(TIMEZONES.keys())

ampm = [
    'am',
    'pm',
    'a\.m\.',
    'p\.m\.'
]

def get_body_link(file , path_to_file='.'):
    '''
    Get the body out of a file
    '''
    with open(os.path.join(path_to_file, file), 'r') as f:
        text = f.read()
        parts = text.split('\n')
        link = parts[2][6:]
        body = parts[4][7:]
    return body, link

def separate(body:str):
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
    parts = re.findall(pattern, body)

    # this removes the journalists name in the end
    for i, part in enumerate(parts):
        if len(part.split('--')[-1].strip().split()) == 2:
            part = ''.join(part.split('--')[:-1])
            parts[i] = part
    return parts

def convert_into_GMT(
    year: int,
    month: str,
    day: int,
    hour: int,
    minute: int,
    timezone:str
):
    '''
    function to convert the local time of blog posts into
    GMT time (the time all other articles are in)

    We have to adjust only the hor part, but then we we have to control
    for switching to another day, month, year
    '''
    timezone = timezone.rstrip()
    # adjust hour
    try:
        hour -= TIMEZONES[timezone]
    except KeyError:
        # i have found this to be an issue at least once
        timezone = timezone + '.'
        hour -= TIMEZONES[timezone]

    # month as number
    try:
        month_no = MONTHS[month]
    # sometimes the '.' is missing when month names are abbreviated
    except KeyError:
        month = month + '.'
        month_no = MONTHS[month]

    # control for moving to next day
    if hour > 23:
        hour -=24
        day += 1
        if day > int(DAYSPERMONTH[month]):
            day = 1
            month_no += 1
            if month_no > 12:
                month_no -= 12
                year += 1

    # control for moving to previous day
    elif hour < 0:
        hour += 24
        day -= 1
        if day < 1:
            month_no -= 1
            if month_no < 1:
                month_no += 12
                year -= 1
    minute = str(minute)
    if len(minute) < 2:
        minute = f'0{minute}'
    date = f'{year}-{month_no}-{day}'
    time = f'{hour}:{minute}'
    return date, time

def new_article(text:str, year:int):
    '''
    Create a new article out of a piece of text extracted with the function above (separate())
    '''
    month_day = re.findall(f'(?:{"|".join(months)})[\s|\S][0-9]*', text)[0]
    day = re.findall('([0-9]+)', month_day)[0]
    month: str = month_day[:-len(day)-1]
    title = re.findall('\s{2}(.+?)\s{2}', text)[0]
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




def main():
    # current directory
    drt = os.getcwd()
    # path to artice text files folder
    path = os.path.join(drt, 'articles/article_text/')
    # dump folder for files that are deleted but kept for safety purposes
    delpath = os.path.join(drt, 'articles/removed/blogs/')
    # all files in that folder
    files = os.listdir(path)

    # create file with all articles that are blogs
    ## DO NOT RUN AGAIN
    # I changed the file manually after creating it this way
    # n = 0
    # with open('blogs.txt', 'w') as blogs:
    #     for file in files:
    #         if 'blog' in file.lower():
    #             blogs.write(file)
    #             blogs.write('\n')
    #             n += 1
    # print(f'there are {n} blog articles')

    # list of articles that are blogs (original run of script)
    # blog_arts = list()
    # for file in files:
    #     if 'blog' in file.lower():
    #         blog_arts.append(file)

    # needed to do it on two more articles, so I created this list manually
    blog_arts = [
        '2019-3-18 Check out what you might have missed at this years Boston Seafood Show.txt'
    ]

    for blog in blog_arts:
        year = int(blog[:4])
        body, link = get_body_link(blog, path)
        articles = separate(body)
        for article in articles:
            try:
                print(article[:100])
                title, date, time, text = new_article(article, year)
                # remove punctuation from title for correct saving
                f_title = ''.join([c for c in title if c not in punctuation])
                filename = f'{date} {f_title}.txt'
                if len(filename) > 100:
                    filename = filename[:96] + '.txt'
                with open(os.path.join(path, filename), 'w') as fn:
                    fn.write(f'DATE: {date} {time}\n')
                    fn.write(f'TITLE: {title}\n')
                    fn.write(f'LINK: {link}\n')
                    fn.write(f'LEAD: \n')
                    fn.write(f'BODY: {text}')
            except Exception as e:
                print(e)
        os.replace(os.path.join(path, blog), os.path.join(delpath, blog))

if __name__ == '__main__':
    main()
