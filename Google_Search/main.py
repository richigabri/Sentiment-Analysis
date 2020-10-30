from bs4 import BeautifulSoup
import urllib
from urllib.parse import urlencode
from fake_useragent import UserAgent
import time
import requests


def _get_search_url(query, page=0, per_page=10, lang='en', area='com', ncr=False, time_period=False, sort_by_date=False):
    # il numero di pagine non funziona 

    params = {
        'nl': lang,
        'q': query.encode('utf8'),
        'start': page * per_page,
        'num': per_page
    }

    time_mapping = {
        'hour': 'qdr:h',
        'week': 'qdr:w',
        'month': 'qdr:m',
        'year': 'qdr:y'
    }


    tbs_param = []
    # Settare la data
    if time_period and time_period in time_mapping:
        tbs_param.append(time_mapping[time_period])

    if sort_by_date:
        tbs_param.append('sbd:1')
    params['tbs'] = ','.join(tbs_param)

    # No Country Redirect
    if ncr:
        params['gl'] = 'us' # Geographic Location: US
        params['pws'] = '0' # 'pws' = '0' disables personalised search
        params['gws_rd'] = 'cr' # Google Web Server ReDirect: CountRy.

    params = urlencode(params)

    url = u"https://www.google.com/search?" + params
    print(url)

    
    # what I found useful.
    https = int(time.time()) % 2 == 0
    bare_url = u"https://www.google.com/search?" if https else u"http://www.google.com/search?"
    url = bare_url + params

    if not ncr:
        if area == 'com':
            url = u"http://www.google.com/search?"
        
        elif area == 'it':
            url = 'http://www.google.dk/search?'
        else:
            raise AreaError('invalid  name,  no area found')
        url += params
    return url


def get_html(url):
    ua = UserAgent()
    header = ua.random

    try:
        request = urllib.request.Request(url)
        request.add_header("User-Agent", header)
        html = urllib.request.urlopen(request).read()
        return html
    except urllib.error.HTTPError as e:
        print("Error accessing:", url)
        print(e)
        if e.code == 503 and 'CaptchaRedirect' in e.read():
            print("Google is requiring a Captcha. "
                  "For more information check: 'https://support.google.com/websearch/answer/86640'")
        if e.code == 503:
            sys.exit("503 Error: service is currently unavailable. Program will exit.")
        return None
    except Exception as e:
        print("Error accessing:", url)
        print(e)
        return None

def _get_name(li):
    """Return il nome del della pagina."""
    
    a = li.find('span')
    #a = li.find('a')
    
    if a is not None:
        return a.text.strip()
    return None

def _get_link(li):
    """Return il link"""
    try:
        a = li.find("a")
        link = a["href"]
        
    except Exception:
        return None
    
    return link

def _get_description(li):
    """Return la descrizione """
        
    sdiv = li.find("div", attrs={"class": "IsZvec"})
    if sdiv:
        
        stspan = sdiv.find("span", attrs={"class": "aCOpRe"})
        
        if stspan is not None:
            return stspan.text.strip()
    else:
        return None

def  read_link(link):
    try:
        text=""
        soup = BeautifulSoup( urllib.request.urlopen(link).read(),"html.parser")
        divs =soup.find_all("p")
        for div in divs:
            #print(div)
            if len(div.text.strip()) > 50:
                text += div.text.strip() +"\n"
        return text
    except:
        return

def write_file(title,link,description,text, namefile):
    file = open(namefile,"w")
    file.write("TITOLO: "+title +"\n")
    file.write("LINK: "+link+"\n")
    file.write("DESCRIZIONE: "+description+"\n")
    file.write("TESTO: "+text+"\n")
    print("file: "+namefile+" creato")
    file.close()
    return

def search(query, pages=1, lang='en', area='com', ncr=False, void=True, time_period=False, sort_by_date=False, first_page=0):
    """
        query: String to search in google.
        pages: Number of pages where results must be taken.
        area : Area of google homepages.
        first_page : First page.
    """

    
    j = 0
    for i in range(first_page, first_page + pages):
        url = _get_search_url(query, i, lang=lang, area=area, ncr=ncr, time_period=time_period, sort_by_date=sort_by_date)
        
        html = get_html(url)
        #file.write(html)

        if html:
            soup = BeautifulSoup(html, "html.parser")
            divs = soup.findAll("div", attrs={"class": "g"})

            
            for li in divs:

                name = _get_name(li)
                
                link = _get_link(li)
                
                description = _get_description(li)

                page = read_link(link)
                if page is None:
                    page = ""
                                
                if void is True:
                    if description is None:
                        continue
                j += 1
                namefile = "files/file"+str(j)+".txt"

                write_file(name,link,description,page,namefile)
                '''
                print("\n"+"##########################      ",j,"\n")
                print("TITOLO: "+name)
                print("LINK: "+link)
                print("DESCRIZIONE: "+description)
                print("TESTO: "+page)
                '''
                
                #results.append(res)
                #print(results.append(res))
                
    print("\n"+"*******************************")
    print("SONO STATI TROVATI ",j," RISULTATI")
    print("*******************************")
    
    #return results


if __name__ == '__main__' :
    num_page =3
    search("assiteca spa",3)