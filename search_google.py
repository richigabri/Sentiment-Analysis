from googlesearch import search
import urllib
from urllib.request import urlopen
from bs4 import BeautifulSoup
import manipulation

my_results_list=[]

def found_link(query):
    
    for i in search(query,        # The query you want to run
                #tld = 'com',  # The top level domain
                lang = 'it',  # The language
                num = 3,     # Number of results per page
                #start = 0,    # First result to retrieve
                stop = 3,  # Last result to retrieve 
                pause =4.0,  # Lapse between HTTP requests
               ):
                my_results_list.append(i)
                print(i)
    open_url()
    return ("finitoooo")
    
def open_url():
    i=0
    for results in my_results_list:
        url = results
       
       
        html = urlopen(url).read()
        
       
        soup = BeautifulSoup(html, features="html.parser") 
        
        # kill all script and style elements
        for script in soup(["script", "style"]):
            script.extract()    # rip it out

        # get text
        text = soup.get_text()
        # break into lines and remove leading and trailing space on each
        lines = (line.strip() for line in text.splitlines())
        # break multi-headlines into a line each
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        # drop blank lines
        text = '\n'.join(chunk for chunk in chunks if chunk)
        #all in lower case
        text=text.lower()
        namefile = "files/file"+str(i)+".txt"
        print(url+"\n")
        
        text_without_stopword = manipulation.remove_stopword(text,namefile)
        totale_parole = len(filtered_sentence.split())
        totale_key = filtered_sentence.count("assiteca")
        print("numero di parole:",totale_parole+"\n")
        print("numero di occorenze:",totale_key+"\n")

        print("percentuale:",(totale_key / totale_parole)*100+"\n")
        
        #file = open("files/file"+str(i)+".txt","w")
        #file.write(text)
        #file.close()
        i=i+1
        
        #print(text)
    return