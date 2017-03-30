import re
import requests
from lxml import html
import pandas as pd 

class SpiderMain(object):
    def __init__(self,sid,startYear,endYear,journal):
        self.headers={
            'Origin':'https://apps.webofknowledge.com',
            'Referer':'https://apps.webofknowledge.com/UA_GeneralSearch_input.do?product=UA&search_mode=GeneralSearch&SID=R1ZsJrXOFAcTqsL6uqh&preferencesSaved=',
            'User-Agent':"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.94 Safari/537.36",
            'Content-Type':'application/x-www-form-urlencoded'
        }
        self.form_data={
            'fieldCount':1,
            'action':'search',
            'product':'WOS',
            'search_mode':'GeneralSearch',
            'SID':sid,
            'max_field_count':25,
            'formUpdated':'true',
            'value(input1)':journal,
            'value(select1)':'SO',
            'value(hidInput1)':'',
            'limitStatus':'collapsed',
            'ss_lemmatization':'On',
            'ss_spellchecking':'Suggest',
            'SinceLastVisit_UTC':'',
            'SinceLastVisit_DATE':'',
            'period':'Range Selection',
            'range':'ALL',
            'period':'Year Range',
            'startYear':startYear,
            'endYear':endYear,
            'editions':'SCI',
            'update_back2search_link_param':'yes',
            'ssStatus':'display:none',
            'ss_showsuggestions':'ON',
            'ss_query_language':'auto',
            'ss_numDefaultGeneralSearchFields':1,
            'ss_query_language':'',
            'rs_sort_by':'PY.D;LD.D;SO.A;VL.D;PG.A;AU.A'
        }
#        self.form_data2={
#            'product':'WOS',
#            'prev_search_mode':'CombineSearches',
#            'search_mode':'CombineSearches',
#            'SID':sid,
#            'action':'remove',
#            'goToPageLoc':'SearchHistoryTableBanner',
#            'currUrl':'https://apps.webofknowledge.com/WOS_CombineSearches_input.do?SID='+sid+'&product=WOS&search_mode=CombineSearches',
#            'x':48,
#            'y':9,
#            'dSet':1
#		}

    #the first step is to get all the links of papers from a query
    #the second step is to get all detailed info of papers

        
    def craw_first_step(self, root_url,sid):
        urls = [] #links for all papers
        s = requests.Session()
        r = s.post(root_url,data=self.form_data,headers=self.headers)
        tree = html.fromstring(r.content)
        new_sid = re.findall(r'SID=\w+&',r.url)[0].replace('SID=','').replace('&','')
            
        #get the total number of pages of a query result
        num_pages = tree.xpath('//span[@id="pageCount.top"]/text()')[0] #done
        
#        new_url = tree.xpath('//a[@class="smallV110"]/@href') #done
#        new_url = list(set(new_url))
#        urls.append(new_url)

        for i in range(1,int(num_pages)+1):
            #create all urls on a specific page
            url = 'https://apps.webofknowledge.com/summary.do?product=WOS&parentProduct=WOS&search_mode=GeneralSearch&parentQid=&qid=8&SID='+sid+'&&update_back2search_link_param=yes&page='+str(i)
            new_r = s.get(url,headers=self.header)
            new_tree = html.fromstring(new_r.content)
            
            #get urls in a page                                           
            new_url = new_tree.xpath('//a[@class="smallV110"]/@href') #done
            new_url =list(set(new_url))
            urls.append(new_url)
        return(urls)


    def craw_second_step(links):   #done
        journals = []
        pub_months = []
        pub_years = []
        titles = []
        authors = []
        corres_authors = []
        corres_addresses = []
        abstracts = []
        
        for url in links:
            s = requests.Session()
            r = s.get(url)
            tree = html.fromstring(r.content)
            #get abstract
            abstract = tree.xpath('(//div[@class="block-record-info"])[2]/p/text()') #done
            abstract = [re.sub(r'\(C\) \d{4} Elsevier Ltd. All rights reserved.','',x) for x in abstract]
            #get title
            title = tree.xpath('(//div[@class="title"])/value/text()') #done
            #get authors
            author = tree.xpath('(//a[@title="Find more records by this author"])/text()') # done
            #get corresponding author
            corres_author = tree.xpath('(//div[@class="block-record-info"])[4]/p[1]/text()') #done
            corres_author = [x for x in corres_author if x!='\n']
            corres_author = [re.sub(r' \(reprint author\) ','',x) for x in corres_author]
            #get corresponding address
            corres_address = tree.xpath('(//td[@class="fr_address_row2"])[1]/text()') #done
            #get publication year and month
            pub_year = tree.xpath('(//p[@class="FR_field"])[5]/value/text()') 
            pub_month = re.sub(r'\d{4}','',pub_year[0])
            pub_year = re.sub(r'[a-zA-Z]{3}\s','',pub_year[0]) #done
            #get the journal name
            journal = tree.xpath('(//span[@class="hitHilite"])[1]/text()')  #done
            
            journals.append(journal)
            pub_years.apeend(pub_year)
            pub_months.append(pub_month)
            titles.append(title)
            authors.append(author)
            corres_authors.append(corres_author)
            corres_addresses.append(corres_address)
            abstracts.append(abstract)
        
        res = pd.DataFrame(links,journals,pub_years,pub_months,titles,authors,corres_authors,corres_addresses,abstract)
        
        return(res)
             

    

if __name__=="__main__":
    root_url = 'https://apps.webofknowledge.com/WOS_GeneralSearch.do'
    #sid='W1OZtZW2eSwnTmvSLev'
    journal = 'transportation research part c emerging technologies'
    start_Year = 2001
    end_Year = 2016

    root='http://www.webofknowledge.com/'
    s=requests.get(root)
    sid=re.findall(r'SID=\w+&',s.url)[0].replace('SID=','').replace('&','')


    obj_spider = SpiderMain(sid,start_Year,end_Year,journal)
    obj_links = obj_spider.craw_first_step(root_url,sid)
    result = obj_spider.craw_second_step(obj_links)
    
