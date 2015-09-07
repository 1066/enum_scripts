#!/usr/bin/python

import requests
import os
import wget
import re
import urllib

url = raw_input('Enter Robots URL' ' e.g. "www.awesomehack.com/robots.txt"\n')
if url[0] == 'w':
    print('Please add http:// next time!')
    url = 'http://'+url
    first_slash = url.index('/')
    remove_slashes = url[first_slash+2:]
    last_slash = remove_slashes.index('/')
    truncate_url = remove_slashes[:last_slash]
else:
    first_slash = url.index('/')
    remove_slashes = url[first_slash+2:]
    last_slash = remove_slashes.index('/')
    truncate_url = remove_slashes[:last_slash]
with requests.Session() as s:
    s = s.get(url)
    url_text = s.text

regex = re.compile('(Allow: )(.+)')
repl = '\\1'
text = regex.sub(repl, url_text)

# Find all instances of the Disallow pages
regex = re.compile('(Disallow: )(/.+)')
repl = '\\2'
text = regex.sub(repl, text)
robots = re.findall('^/.+', text, flags=re.MULTILINE)
# Get rid of any Duplicate robots files
remove_duplicate = list(set(robots))

url_count = len(remove_duplicate)
url_count = set(range(1, url_count +1))
new_url_list = []

for path in remove_duplicate:
    new_url = truncate_url + path
    new_url = 'http://' + new_url
    new_url_list.append(new_url)

new_url_list = [x.encode('UTF8') for x in new_url_list]
robots_dict = dict(zip(url_count, new_url_list))


list_cache = {}
bad_urls = []
def list(choice):
    if choice == 'list':
        good_urls = []
        for item in robots_dict.items():
            r = requests.get(item[1])
            if r.status_code == 200:
                good_urls.append(item[1])
            url_number = range(1, len(good_urls)+1)
            good_url_dict = dict(zip(url_number, good_urls))
            list_cache.update(good_url_dict)
            if r.status_code != 200:
                bad_urls.append(item[1])
        if bool(bad_urls) == True:
            for item in list_cache.items():
                print item
            see_bad()
        else:
            for item in list_cache.items():
                print item
    elif choice.isdigit():
        choice = int(choice)
        if not list_cache.get(choice):
           print "You need to run list first"

        else:
            full_url = []
            name = []
            choice = int(choice)
            for url in list_cache.values():
                regex = re.compile('(.+)(\.\w+)(/)(.+)')
                repl = '\\4'
                file_name = regex.sub(repl, url)
                file_name = file_name.replace('/', '')
                full_url.append(url)
                name.append(file_name)
            urllib.urlretrieve(full_url[choice -1], name[choice -1])

def download_all():
    good_urls = []
    good_url_number = []

    for item in robots_dict.items():
        r = requests.get(item[1])
        if r.status_code == 200:
            good_urls.append(item[1])
            good_url_number.append(item[0])

    for url in good_urls:
        regex = re.compile('(.+)(\.\w+)(/)(.+)')
        repl = '\\4'
        file_name = regex.sub(repl, url)
        file_name = file_name.replace('/', '')
        urllib.urlretrieve(url, file_name)

def help():
    print 'OPTIONS: \n' \
          'Help == Help\n' \
          'list == List all robots.txt Disallow Directories that are accessible (200 response codes)\n' \
          'bad == List all robots.txt files that are not accessible or received anything but a 200 response code\n' \
          'download all == Download all robots.txt files that are accessible\n' \
          'exit == exit program\n'


rejected_dict_cache = {}
def bad_requests():
    rejected_codes = []
    rejected_urls = []
    for item in robots_dict.items():
        r = requests.get(item[1])
        if r.status_code != 200:
            rejected_codes.append(r.status_code)
            rejected_urls.append(item[1])
            rejected_dict = dict(zip(rejected_urls, rejected_codes))
            rejected_dict_cache.update(rejected_dict)
    for item in rejected_dict.items():
            print item

def see_bad():
        print
        print 'Enter corresponding number with URL to download or type "download all" to download every "good" url'
        print
        get_bad = raw_input('Some directories/files from the robots file on ' + url + ' have received "bad" error codes. Would you like to see what they are? y/n\n')
        if get_bad == 'y':
            bad_requests()
print
print'Looks like there are ' + str(len(remove_duplicate)) +  ' Disallow: pages on ' + url
print 'OPTIONS: Help for help, list to see all robot pages available, download all to download all robots pages and exit() to exit' \

while True:
    choice = raw_input('>')

    if choice == 'exit':
        break

    if choice == 'help':
        help()
        continue

    if choice == 'bad':
        if bool(rejected_dict_cache) == True:
            for item in rejected_dict_cache.items():
               print item
        else:
            print 'There may not be any bad responses. Try running list first.'
        continue

    if choice == 'download all':
        download_all()
        continue

    if choice == 'list':
        if bool(list_cache) == False:
            list(choice)
        else:
            for item in list_cache.items():
                print item
        continue

    if choice.isdigit():
        list(choice)

        continue

