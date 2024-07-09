# read all the html files (dumped as txt files in articles/html_files)
# extract actual article text
# export article text as txt file in articles/article_text

import os
import re
import bs4

from string import punctuation
punctuation.replace('$', '')

from useful_items import unicode_dict

def get_main_body(line: str):
    '''
    get the main body of the article
    '''
    # use regex to find the main body of the article
    # part between "body": and "paid"
    body: str = re.findall('"body":(.*?),"paid"', line)[0]
    # unicode decoding:
    # first encode properly in the text
    body = body.encode('utf-8').decode('utf-8')
    # then replace unicode by their ascii equivalent
    for k,v in unicode_dict.items():
        body = body.replace(k, v)
    # get the text out
    soup = bs4.BeautifulSoup(body, "html.parser").text
    # replace html tags and artifacts with a space: a paragraph, a section,
    # text with strong importance, the emphasis element, a non-breaking space,
    # a hyperlink, an underline, bold text, term in italics, item in a list,
    # an unordered list of items
    tags = ['<\\/p\\>', '<\\/div\\>', '<\\/strong\\>', '<\\/em\\>', '\\xc2\\xa0',
            '<\\/a\\>', '<\\/u\\>', '<\\/b\\>', '<\\/i\\>', '<\\/li\\>', '<\\/ul\\>']
    for tag in tags:
        soup = soup.replace(tag, ' ')
    # remove backslashes
    soup = soup.replace('\\', '')
    return soup


def get_lead_text(line: str):
    '''
    Find the lead text of the article
    (the sentence under the title)
    '''
    # cook a soup
    soup = bs4.BeautifulSoup(line, "html.parser")
    # lead text is a meta with name="description"
    lead = soup.find("meta", {'name':"description"}).get('content')
    # replace unicode by their ascii equivalent
    for k,v in unicode_dict.items():
        lead = lead.replace(k, v)
    return lead


def extract_and_save(file:str, filename):
    '''
    Take as input the html code of a website as string

    extract the text of the article and return it as string
    '''
    # take date, title and link first
    parts = file.split('\n')
    date = parts[0]
    title = parts[1]
    link = parts[2]
    # use functions above to extract lead text and main body
    lead = get_lead_text(parts[4])
    body = get_main_body(parts[4])
    # trim filename, if it is longer than 100 characters
    if len(filename) > 100:
        filename = filename[:96] + '.txt'
    export_path = os.path.join(text_path, filename)
    # write into file
    with open(export_path, 'w+', encoding='utf-8') as f:
        f.write(date)
        f.write('\n')
        f.write(title)
        f.write('\n')
        f.write(link)
        f.write('\n')
        f.write('LEAD: ')
        f.write(lead)
        f.write('\n')
        f.write('BODY: ')
        f.write(body)

# path of html files
html_path = os.path.join(os.getcwd(), 'articles/html_files')
# path where text is to be exported
text_path = os.path.join(os.getcwd(), 'articles/article_text')
# all files in html_path
files = os.listdir(html_path)

if __name__ == '__main__':
    # loop through files and extract all texts
    for i, file in enumerate(files):
        filepath = os.path.join(html_path, file)
        with open(filepath, 'r') as f:
            extract_and_save(f.read(), file)
        if i % 100 == 0:
            print(f'{i}/{len(files)}')
    print(f'{i}/{len(files)}: DONE')
