# -*- coding: utf-8 -*-
"""
Created on Sun Apr 16 20:41:57 2017

@author: Jay
"""

from bs4 import BeautifulSoup
import re
import requests


def run(url):

    fin=open('tags.txt','r') # input file
    fw=open('questions.txt','w') # output file
    log=open('log.txt','w') # log file
    
    c = 1 #just a counter for questions scraped
    vote_cutoff = -1 #vote threshold
    pageNum=41 # number of pages to collect
    
    for line in fin: #for each tag 
        html=None
        tag=line.lower().strip()
        print(tag)
        log.write('tag: ')
        log.write(tag+'\n')
        for n in range(pageNum):    
            if n == 0: continue
            pageLink=url+tag+'-interview-questions&n='+str(n) # make the page url

            for i in range(5): # try 5 times
                try:
                    #use the browser to access the url
                    response=requests.get(pageLink,headers = { 'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36', })
                    html=response.content # get the html
                    break # we got the file, break the loop
                except Exception as e:# browser.open() threw an exception, the attempt to get the response failed
                    print ('failed attempt',i)
                    #time.sleep(2) # wait 2 secs
    				
    		
            if not html:continue # couldnt get the page, ignore
            
            soup = BeautifulSoup(html.decode('ascii', 'ignore'),'lxml') # parse the html 
    
            questions=soup.findAll('li', {'class':re.compile('question')}) # get all the review divs
    
            for question in questions:
                if question == questions[0]:
                    print('Page '+str(n))
                    log.write('Page '+str(n)+'\n')
                votes,text='NA','NA' # initialize votes and text 
                votes = int(question.find('div', {'class':re.compile("votesNetQuestion")}).text)
                if votes > vote_cutoff :
                    text = question.find('p').text.replace("\r", " ").replace("\n", " ")
                    fw.write(tag + "\t\t\t\t\t" + text +'\n\n')
                    c=c+1
        print('Total Questions Scraped:'+str(c))
        log.write('Total Questions Scraped:'+str(c)+'\n')
    fw.close()
    log.close()

if __name__=='__main__':
    url='https://www.careercup.com/page?pid='
    run(url)
