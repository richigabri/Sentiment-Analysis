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
    open_url(query)
    return ("finitoooo")
    
def open_url(query):
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
        '''


##############################
        text1 = soup.find_all(text=True)

        text = ''
        blacklist = [
            '[document]',
            'noscript',
            'header',
            'html',
            'meta',
            'head', 
            'input',
            'script',
            'style'
            
            'p',
            'li',
            'src'
            
            
            # there may be more elements you don't want, such as "style", etc.
        ]

        for t in text1:
            if t.parent.name not in blacklist:
                text += '{} '.format(t)
                '''
##############################

        # break into lines and remove leading and trailing space on each
        lines = (line.strip() for line in text.splitlines())
        # break multi-headlines into a line each
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        # drop blank lines
        text = '\n'.join(chunk for chunk in chunks if chunk)
        #all in lower case
        text=text.lower()
        
        i=i+1
        print(i)
        namefile = "files/file"+str(i)+".txt"
        
        print("###########################################################")
        text_without_stopword = manipulation.remove_stopword(text,namefile)
        
        print("\n"+url+"\n")
        #valutazione della presenza delle parole chiave
        keys =query.split()
        
        totale_parole = len(text_without_stopword.split())
        print("numero di parole:",totale_parole,"\n")
        for num in range (len(keys)):
            totale_key = text_without_stopword.count(keys[num])
            
            print("numero di occorenze per "+keys[num]+":",totale_key)

            print("percentuale:",(totale_key / totale_parole)*100)
        
        #file = open("files/file"+str(i)+".txt","w")
        #file.write(text)
        #file.close()
       
        
        #print(text)
    return
