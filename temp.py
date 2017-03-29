import os 
from bs4 import BeautifulSoup as bs
import requests
from requests_file import FileAdapter
from lxml import etree
os.chdir(r'H:')

all_links = []

#with open('sci.txt','r',encoding='UTF-8') as f:
 #   d = f.readlines()
#f.close()

def all_query_results()

url = 'http://apps.webofknowledge.com/full_record.do?product=INSPEC&search_mode=GeneralSearch&qid=3&SID=U2T7k6duHYpLazuIZ5J&page=1&doc=10'
s= requests.Session()
s.mount('file://',FileAdapter())
d = s.get('file:///H:/single_paper.html')
#d = s.get(url)
htmlparser = etree.HTMLParser()
#soup = etree.parse(d.text)
soup = bs(d.text,'lxml')
tree.xpath('//*[@id="records_form"]/div/div/div/div[1]/div/div[3]/p[5]/value')

#get the number of pages for a query result
num_pages = soup.find('span',{'id':'pageCount.top'}).get_text() 
#print(num_pages)

#extract the title and link of papers
titles_links = soup.find_all('a',{'class':'smallV110'})
links = ['apps.webofknowledge.com'+x['href'] for x in titles_links]
all_links.append(links)
titles = [x.get_text() for x in titles_links]

#authors = soup.find_all('span',{'class':'label'})

#extract the journal names
journals = soup.find_all('span',{'class':'hitHilite'})
journals = [x.get_text() for x in journals]
print(links)
#print(titles)
#print(authors[1])
#print(journals)
