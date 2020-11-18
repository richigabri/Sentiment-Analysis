import urllib
from urllib.parse import urlencode
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
import time
from datetime import date
import sys


def print_data(name,link,description,text):
    print("TITOLO:\n "+name)
    print("LINK:\n ",link)
    print("DESCRIZIONE:\n "+description)
    print("TEST:\n " +title)

class Text():
    def __init__(self, title, link,description,text):
        self.title = title
        self.link = link
        self.description =description
        self.text = text

    def __str__(self):
        return "TITLE: "+self.title +"\n"+"LINK: "+ self.link+"\n"+"DESCRIZIONE: " +self.description +"\n"+"TEXT: " +str(self.text)



def get_search_url(query, page=0, per_page=10, lang='en', area='com', ncr =False,time_period=True, sort_by_date=True):

    params = {
            'nl': lang,
            'q': query.encode('utf8'),
            'start': page * per_page,
            'num': per_page
        }

    # data di inizio(cd_min) e data di fine(cd_max) per la ricerca
    #tbs: cdr:1,cd_min:<m/d/yyyy>,cd_max:<m/d/yyyy>
    cd_min = '3/2/1984'
    cd_max = date.today().strftime("%d/%m/%Y")

    time_mapping = 'cd_min:'+ cd_min+','+'cd_max:'+cd_max

    '''
    time_mapping = {
        'cd_min' :'3/2/1984',
        'cd_max' : date.today().strftime("%d/%m/%Y")

        }
    '''

    tbs_param = []

    if time_period:
        tbs_param.append('cdr:1,'+time_mapping)


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

    https = int(time.time()) % 2 == 0
    bare_url = u"https://www.google.com/search?" if https else u"http://www.google.com/search?"
    url = bare_url + params

    if not ncr:

        if area == 'com':
            url = u"http://www.google.com/search?"

        elif area == 'it':
            url = 'http://www.google.dk/search?'
        else:
            print('invalid  name,  no area found')
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

def _get_title(li):
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

def _get_text(link):
    str = ''
    try:
        soup = BeautifulSoup(urllib.request.urlopen(link).read(),features="lxml")
        divs =soup.find_all("p")
        for div in divs:
            #print(div)
            #SUPPOSIZIONE -> le righe con meno di 50 caratteri non contengono nulla
            if len(div.text.strip()) > 50:
                str= str + div.text.strip()
        return str
    except:
        return ' '

soup = BeautifulSoup(urllib.request.urlopen('https://www.cdt.ch/economia/ticino/inaugurati-gli-uffici-di-lugano-di-assiteca-GH1786549?_sid=1EPScBEP').read()

def search(query,pages=1, lang='en', area='com', ncr=False, void=True, time_period=True, sort_by_date=True, first_page=0):
    """
    query = keyword
    pages = numero di pagine da analizzare
    lang = area di google dove cercare es .com .it

    """
    results = []
    for i in range(first_page + first_page+pages):
        url = get_search_url (query, i,lang=lang, area=area, ncr=ncr, time_period=time_period, sort_by_date=sort_by_date)
        #print(url)
        html = get_html(url)

        if html:
            soup = BeautifulSoup(html, "html.parser")
            divs = soup.findAll("div", attrs={"class": "g"})



            for li in divs:

                title = _get_title(li)

                link = _get_link(li)

                description = _get_description(li)

                text = _get_text(link)

                if void is True:
                    if description is None:
                        continue
                # aggiungo i file trovati in un lista TEXT
                results.append(Text(title,link,description,text))

                #per stampare in fase di debug
                #print_data(name,link,description,text)

    return results
