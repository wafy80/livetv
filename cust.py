from time import sleep
from unidecode import unidecode
import requests
from bs4 import BeautifulSoup
import json
import re
import html

def trascochid(chid):
    with open('cust.json', 'r') as f:
        switcher = json.load(f)
    newchid = switcher.get(chid, "")
    return newchid

def get_shift(chid):
    tsh="+0000"    
    return tsh

def fixepg(epgch, epgline):    
    if epgline.lower().find('<title lang="zh">') > -1:
        totrans=epgline.replace('⋗','->').replace(' lang="zh"','')
        totrans=get_cont_tag(totrans, 'title')[0]
        try:
            translated = unidecode(totrans)
        except:
            translated = totrans    
        translated = html.escape(translated)
        epgline = f"<title>{translated}</title>"
    return epgline

def get_cat(chname):
    if trascochid(chname):
        categories = 'Cust'
    elif chname.lower().find("amazon") > -1 or \
            chname.lower().find("magenta") > -1 or \
            chname.lower().find("rtl+") > -1 or \
            chname.lower().find("eurosport360") > -1 or \
            chname.lower().find("elcano") > -1  or \
            chname.lower().find("visita") > -1  or \
            chname.lower().find("pimple") > -1 or \
            chname.lower().find("acetop") > -1 or \
            chname.lower().find("nash sport") > -1 :
        categories = 'PPV'
    elif chname.lower().find("4k") > -1 or \
            chname.lower().find("uhd") > -1 or \
            chname.lower().find("ultra") > -1 :
        categories = '4K'
    elif chname.lower().find("adult") > -1 or \
            chname.lower().find("porn") > -1 or \
            chname.lower().find("redtraffic") > -1:
        categories = '18+'
    elif (chname.lower().find("sport") > -1) or \
            chname.lower().find("dazn") > -1  or \
            chname.lower().find("espn") > -1  or \
            (chname.lower().find("match") > -1 and chname.lower().find("[ru]") > -1) or \
            chname.lower().find("setanta live") > -1 or \
            chname.lower().find("amazon") > -1 or \
            chname.lower().find("nba ") > -1  or \
            chname.lower().find("skysp") > -1 or \
            chname.lower().find("m. ") > -1 or \
            (chname.lower().find("futbol") > -1 and chname.lower().find("[ru]") > -1) :   
        categories = 'Sport'    
    else:
        endtit = chname.find("[")   
        if endtit > -1:   
            categories = chname[endtit+1:chname.find("]")]
        else:
            endtit = chname.find("(")   
            if endtit > -1:   
                categories = chname[endtit+1:chname.find(")")]
            else:
                categories = ''    

    if categories != 'Sport' and \
            categories != 'RU' and \
            categories != 'DE' and \
            categories != 'PL' and \
            categories != '18+' and \
            categories != 'PPV' and \
            categories != 'Cust' and \
            categories != '4K' :
        categories = ''

    return categories

def get_first_image(query):
    query = query.replace(' ', '+')
    url = f"https://www.google.com/search?q={query}&tbm=isch"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"}    
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    images = soup.find_all('img')    
    if images:
        return images[1]['src']  # The first image is usually a Google logo, so we take the second one
    else:
        return None    

def get_cont_tag(testo, tag):
    pattern = rf'<{tag}>(.*?)</{tag}>'
    matches = re.findall(pattern, testo)
    return matches