#!/usr/bin/python

import re
import requests
import socket
#Grab all subdomains from a given host
url = raw_input("Enter the URL you would like to scrape\n")
if url[0] == 'w':
    print('Please add http:// next time!')
    url = 'http://'+url
with requests.Session() as s:
    s = s.get(url)
    url_text = s.text

first_slash = url.index('/')
remove_slashes = url[first_slash+2:]
first = url.index('.')
url = url[first:]
second = url.index('.') + 1
url = url[second:]
regex = '[A-Za-z0-9_\.-]*\.*' + url

subs = (re.findall(regex, url_text))
subs = [x.encode('UTF8') for x in subs]
subs = set(subs)

for sub in subs:
   print sub


