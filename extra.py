from flask import Flask, render_template, request
import requests
from bs4 import BeautifulSoup as bs
from urllib.request import urlopen as uReq, Request
import csv

def listOfTuples(l1, l2):
    return list(map(lambda x, y:(x,y), l1, l2))

def data(searchString):
    headers = {'User - Agent': 'Mozilla / 5.0(Windows NT 6.1) AppleWebKit / 537.36(KHTML, like Gecko) Chrome / 41.0.2228.0 Safari / 537.3'}
    quotes_url = "https://www.brainyquote.com/search_results?q=" + searchString  # preparing the URL to search the product on flipkart
    req = Request(quotes_url
        ,
        data=None,
        headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36'
        }
    )
    html_content = requests.get(quotes_url)
    quotes_html = bs(html_content.content, "html.parser")
    quotes_line = quotes_html.find(id='quotesList')
    job_elems = quotes_line.find_all('div', class_='clearfix')
    quotes_list=[]
    author_list=[]
    for job in job_elems:
        quotes = job.find('a', title='view quote')
        author = job.find("a", title="view author")
        if None in (quotes,author):
            continue
        quotes_list.append(quotes.text)
        author_list.append(author.text)
    # with open('text.csv', 'w') as f:
    #         writer = csv.writer(f, delimiter=',')
    #         writer.writerows(zip(quotes_list, author_list))
    data = listOfTuples(quotes_list,author_list)
    quotes1= data[25][0]
    return quotes1

print(data("love"))