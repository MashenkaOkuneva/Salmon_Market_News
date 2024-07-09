# There are some articles left from previous text extration attempts
# that have wrong file endings (not '.txt'). This script deletes them.
# Others are duplicates, which are also deleted.

# needs to run only once, some basic post-processing of scraping results

import os

# current directory
drt = os.getcwd()

# path to artice text files folder
path = os.path.join(drt, 'articles/article_text/')
# all files in that folder
files = os.listdir(path)
# dump folder for files that are deleted but kept for safety purposes
delpath = os.path.join(drt, 'articles/removed/')

# delete some invalid or duplicate files
# move others to separate folder (in case we need them again)
for file in files:
    # files that do not end on '.txt'
    if not file.endswith('.txt'):
        os.remove(os.path.join(path, file))
    # monthly top stories and most-reads, live updates, price trackers
    elif (
        'top stor' in file.lower() or
        'LIVE' in file and not 'intrafish live' in file.lower() or
        'live update' in file.lower() or
        'mostread' in file.lower() or
        'most read' in file.lower() or
        'intrafish price tracker' in file.lower() or
        'top headlines' in file.lower()
    ):
        os.replace(os.path.join(path, file), os.path.join(delpath, file))



# delete duplicates with file name lengths > 100
for i, file in enumerate(files):
    if len(file) > 100:
        if files[i-1][:96] == file[:96]:
            os.remove(os.path.join(path, file))

# now for the other direction
# both at the same time creates problems when both files
# before and after that one share the same name
for i, file in enumerate(files):
    if len(file) > 100:
        if files[i+1][:96] == file[:96]:
            os.remove(os.path.join(path, file))




