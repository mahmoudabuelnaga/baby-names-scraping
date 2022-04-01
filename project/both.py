# -*- coding: utf-8 -*-
from time import sleep
from bs4 import BeautifulSoup
import csv
import requests

links = []
items = []

for i in range(1,38):
    endpoint = f"https://baby.webteb.com/baby-names/%D8%A7%D8%B3%D9%85%D8%A7%D8%A1-%D8%A7%D9%88%D9%84%D8%A7%D8%AF-%D9%88%D8%A8%D9%86%D8%A7%D8%AA?pageindex={i}"

    get_response = requests.get(endpoint)
    # print(get_response.content)

    soup = BeautifulSoup(get_response.content, 'lxml')
    # print(soup.prettify())

    section = soup.find('div', {'class':'page-section'})

    for li in section.find_all('li'):
        links.append(li.a['href'])
        print(f'{i}', li.a['href'])


for i, link in zip(range(1,len(links)+1), links):
    url = f"https://baby.webteb.com{link}"

    get_response = requests.get(url)

    soup = BeautifulSoup(get_response.content, 'lxml')

    content = soup.find('div', {'class':'section name'})
    section1 = content.find('div', {'class':'section'})
    name_detail = content.find('div', {'class':'name-details'})
    section2 = name_detail.find('div', {'class':'section'})
    span = section2.find('span', {'class':'latin'})

    item = {}
    if content.h1.text:
        item['arabic_name'] = content.h1.text
    if section1.p.text:
        item['meaning'] = section1.p.text
    if span.text:
        item['english_name'] = span.text

    print(i, content.h1.text, section1.p.text, span.text)

    items.append(item)


filename = '/home/naga/dev/babyNamesScraping/project/both.csv'
with open(filename, 'w', newline='') as f:
    w = csv.DictWriter(f, fieldnames=['arabic_name','meaning', 'english_name'], extrasaction='ignore' , delimiter = ';')
    w.writeheader()
    print(items)
    for item in items:
        w.writerow(item)
        print(item)
    