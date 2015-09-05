#!/usr/bin/python

import requests
import os
import wget
import re
import urllib

#url = raw_input('Enter Robots URL' 'e.g. "www.awesomehack.com/robots.txt"\n')
url = 'https://www.pinterest.com/robots.txt'
if url[0] == 'w':
    print('Please add http:// next time!')
    url = 'http://'+url

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

names_of_dirs = []
for string in robots:
     remove_forward_slash = string.replace('/', ' ')
     no_spaces = remove_forward_slash.replace(' ', '')
     names_of_dirs.append(no_spaces)

names_of_dirs = [x.encode('UTF8') for x in names_of_dirs]

robots_dict = dict(zip(url_count, new_url_list))

url_names_dict = dict(zip(url_count, names_of_dirs))


def download_all():
    good_urls = []
    good_url_number = []
    good_url_dirs = []

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
          'all == Download all robots.txt files that are accessible\n' \
          'exit == exit program\n'

#def download_invidual(choice):
#    choice = int(choice)
 #   r = requests.get(robots_dict.get(choice))
  #  if r.status_code == 200:
   #     urllib.urlretrieve(robots_dict.get(choice), url_names_dict.get(choice))

def list():
    good_urls = []
    for item in robots_dict.items():
        r = requests.get(item[1])
        if r.status_code == 200:
            good_urls.append(item[1])
        url_number = range(1, len(good_urls)+1)
        good_url_dict = dict(zip(url_number, good_urls))
    for item in good_url_dict.items():
        print item




def bad_requests():
    rejected_codes = []
    rejected_urls = []
    for item in robots_dict.items():
        r = requests.get(item[1])
        if r.status_code != 200:
            rejected_codes.append(r.status_code)
            rejected_urls.append(item[1])
            rejected_dict = dict(zip(rejected_urls, rejected_codes))

    for item in rejected_dict.items():
        print item

print 'OPTIONS: Help for help, all to download all robots pages, list to see all robot pages available, exit() to exit'

while True:
   # try:
    choice = raw_input('>')

    if choice == 'exit':
        break

    if choice == 'help':
        help()
        continue


    if choice == 'bad':
        bad_requests()
        continue


    if choice == 'all':
        download_all()
        continue

    if choice == 'list':
        list()
        print
        print 'To Download type in the number corrosponding with the URL or type ALL to download every Robots file with a 200 response_code'
        print
        get_bad = raw_input('Some directories/files from the robots file on ' + url + ' have received bad error codes. Would you like to see what they are? y/n\n')
        if get_bad == 'y':
            bad_requests()

        elif get_bad == 'n':
            continue


    if choice.isdigit():
        pass
            #regex = re.compile('(.+)(\.\w+)(/)(.+)')
            #repl = '\\4'
            #file_name = regex.sub(repl, url)
            #file_name = file_name.replace('/', '')
        #    urllib.urlretrieve(good_url_dict.item[choice], url)

    continue

   # except:
    #        print 'Sorry ' + str(choice) + ' is not a valid option please try again'



