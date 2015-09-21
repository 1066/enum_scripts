#!/usr/bin/python

import requests
import os
import wget
import re
import urllib

class Url():
    def __init__(self):
        self.url = raw_input('Enter Robots URL' ' e.g. "www.awesomehack.com/robots.txt"\n')
        text_url = ''
        truncate_url = ''
        self.robots = set()
        self.url_count = 1
        self.url_range = []
        self.final_url_list = []
        self.robots_dict = {}

    def get_url(self):
        if self.url[0] == 'w':
            print('Please add http:// next time!')
    	    self.url = 'http://'+self.url
        return self.url


    def remove_slashes(self):
        first_slash = self.url.index('/')
        remove_slashes = self.url[first_slash+2:]
        last_slash = remove_slashes.index('/')
        self.truncate_url = remove_slashes[:last_slash]
        return self.truncate_url


    def make_request(self):
        with requests.Session() as s:
            s = s.get(self.url)
            self.url_text = s.text
            return self.url_text

    def remove_allow(self):
        url_text = self.url_text
        regex = re.compile('(Allow: )(.+)')
        repl = '\\1'
        text = regex.sub(repl, url_text)
        # Find all instances of the Disallow pages
        regex = re.compile('(Disallow: )(/.+)')
        repl = '\\2'
        text = regex.sub(repl, text)
        robots = re.findall('^/.+', text, flags=re.MULTILINE)
        # Get rid of any Duplicate robots files
        self.robots = robots
        self.url_count = len(self.robots)
        self.url_range = set(range(1, self.url_count +1))
        for path in self.robots:
            new_url = self.truncate_url + path
            new_url = 'http://' + new_url
            self.final_url_list.append(new_url)
        self.final_url_list = [x.encode('UTF8') for x in self.final_url_list]
        self.robots_dict = dict(zip(self.url_range, self.final_url_list))



list_cache = {}
bad_urls = []

def list(choice):
    if choice == 'list':
        good_urls = []
        for item in u.robots_dict.items():
            r = requests.get(item[1])
            if r.status_code == 200:
                good_urls.append(item[1])
            url_number = range(1, len(good_urls)+1)
            good_url_dict = dict(zip(url_number, good_urls))
            list_cache.update(good_url_dict)
            if r.status_code != 200:
                bad_urls.append(item[1])
        if bool(bad_urls) == True:
            for key,value in list_cache.items():
                print key,value
            see_bad()
        else:
            for key,value in list_cache.items():
                print key,value

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

    for item in u.robots_dict.items():
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
    print 'OPTIONS: \n\n' \
          'Help == Help\n' \
          'list == List all robots.txt Disallow Directories that are accessible (200 response codes)\n' \
          'bad == List all robots.txt files that are not accessible or received anything but a 200 response code\n' \
          'download all == Download all robots.txt files that are accessible\n' \
          'exit == exit program\n' \
          'new url == enumerate another URL ' \
          'see all == see all robots.txt Disallow Directories'
    print


rejected_dict_cache = {}
def bad_requests():
    rejected_codes = []
    rejected_urls = []
    for item in u.robots_dict.items():
        r = requests.get(item[1])
        if r.status_code != 200:
            rejected_codes.append(r.status_code)
            rejected_urls.append(item[1])
            rejected_dict = dict(zip(rejected_urls, rejected_codes))
            rejected_dict_cache.update(rejected_dict)
    for item in rejected_dict.items():
        print item[0],item[1]


def see_bad():
        print
        print 'Enter corresponding number with URL to download or type "download all" to download every "good" url'
        print
        get_bad = raw_input('Some directories/files from the robots file on the domain: ' + u.url + ' have received "bad" error codes. Would you like to see what they are? y/n\n')
        if get_bad == 'y':
            try:
                if bool(rejected_dict_cache) == False:
                    bad_requests()

                elif bool(rejected_dict_cache) == True:
                    for item rejected_dict_cache.items():
                        print item[0],item[1]

            except:print 'No Bad Requests Found'


u = Url()
u.get_url()
u.remove_slashes()
u.make_request()
u.remove_allow()


def see_all():
    final_list = u.final_url_list
    for url in final_list:
        print url

def show_disallow():
    print
    print'Looks like there are ' + str(u.url_count) +  ' Disallow: pages on the domain: ' + u.url
    #print 'OPTIONS: Help for help, list to see all robot pages available, download all to download all robots pages and exit() to exit' \
    help()

show_disallow()



while True:
    choice = raw_input('>')

    if choice == 'exit':
        break

    if choice == 'help':
        help()
        continue

    if choice == 'bad':
        try:
            if bool(rejected_dict_cache) == False:
                bad_requests()


            elif bool(rejected_dict_cache) == True:
                for key,value in rejected_dict_cache.items():
                    print key,value

        except:print 'No Bad Requests Found'

        continue

    if choice == 'download all':
        download_all()
        continue

    if choice == 'list':
        if bool(list_cache) == False:
            list(choice)

        else:
            for key,value in list_cache.items():
                print key, value

        continue

    if choice.isdigit():
        list(choice)

    if choice == 'new url':
        u = Url()
        u.get_url()
        u.remove_slashes()
        u.make_request()
        u.remove_allow()
        show_disallow()
        list_cache.clear()
        rejected_dict_cache.clear()

    if choice == 'see all':
        see_all()

    continue





