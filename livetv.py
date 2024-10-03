# Anchor extraction from HTML document
from bs4 import BeautifulSoup
from requests import get
from datetime import datetime, timedelta
import time
import locale
import os
from transliterate import translit
from acestream.server import Server
from acestream.engine import Engine
from acestream.stream import Stream
from acestream.search import Search
#from googletrans import Translator
from tor_proxy import tor_proxy
import glob

def wlog(stext):
	"""
	flog = open("log.txt", "a")
	flog.write(datetime.now().strftime("%d/%m/%Y %H:%M:%S" + ' - ' + stext + '\n'))
	flog.close()
	"""
	print(datetime.now().strftime("%d/%m/%Y %H:%M:%S" + ' - ' + stext))

def left(s, n):
    return s[:n]

def getchname(aslink):
    chname = aslink.replace("acestream://", "")
    
    try:
        chname = open("tmp/" + chname + ".ace", "r", encoding='utf-8').readline().strip()
        wlog("C - " + chname)
        
    except:
        #translator = Translator()        
        time.sleep(0.1)
        engine = Engine('acestreamengine', client_console=True)
        time.sleep(0.1)
        server = Server(host='127.0.0.1', port=6878)
        time.sleep(0.1)
        engine.start()
        time.sleep(0.1)
        stream = Stream(server, id=chname)
        time.sleep(0.1)
        stream.start()
        time.sleep(0.1)
        chid = chname
        chname=stream.info.name
        if chname is None:
            chname = chid
        
        """
        search = Search(server, query=chname, group_by_channels=1, show_epg=1)
        search.get(page=0)
        try:
            aceimg = search.results[0].icons[0]['url']
        except:
            aceimg=''    
        aceid = str(search.results[0].items[0].channel_id)      
        """
        
        #chname = translator.translate(chname).text
        time.sleep(0.1)
        
        stream.stop()
        time.sleep(0.1)
        engine.stop()
        time.sleep(0.1)
        
        fileace = open("tmp/" + chid + ".ace", "w", encoding='utf-8')
        fileace.write(chname + '\n')
        #fileace.write(aceimg + '\n')
        #fileace.write(aceid)
        fileace.close()
        
        wlog("N - " + chname)
        time.sleep(0.1)

    totrans = chname
    try:
        translated = translit(totrans,reversed=True)
    except:
        translated = totrans   
        
    return translated        

def getchlogo(aceid):
    with open("tmp/" + aceid + ".ace", "r", encoding='utf-8') as fileace:
        fileace.readline()
        fileace.readline()
        chlogo=fileace.readline()
    return chlogo

wlog("INIZIO")

locale.setlocale(locale.LC_TIME, "it_IT.UTF-8") 
d = datetime.now()

if not os.path.exists("tmp"): 
    os.makedirs("tmp") 

port = tor_proxy()
http_proxy  = f"socks5h://127.0.0.1:{port}"
https_proxy = f"socks5h://127.0.0.1:{port}"
proxies = {"http" : http_proxy, "https" : https_proxy, }
   
strresult = '{' + f'"name":"LiveTv","author":"H0:M0:S0","url": "http://:","image":"https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQ_dgKtA6aKRRqqWsm0fuK_GhC-F4ITX5xXCw&s","groups":['

#for idsport in ['1','2','3','4','5','6','7','12','13','17','19','21','22','27','29','30','31','32','33','37','38','39','41','46','52','54','75','96']:
req = get('https://livetv.sx/it/allupcomingsports', proxies=proxies)
time.sleep(0.1)
result = req.text
soup = BeautifulSoup(result, 'html.parser')
lstlink = ""

upcoming = soup.find('table',{"class":"main"})

for anchor in upcoming.find_all('a'):
    link = anchor.get('href', '/')
    linkfind = left(link,link.find("_"))
    if lstlink.find(linkfind) == -1:
        lstlink += linkfind
        if link.find("/eventinfo") > 0 and anchor.get('class')[0] == "live":
            parent = anchor.parent
            orario = parent.find('span',{"class":"evdesc"}).text.split(' à ')
            data = orario[0]
            ora = orario[1]
            ora = ora[0:ora.find('\r')]

            torneo = orario[1]
            torneo = torneo[torneo.find('(')+1:len(torneo)-1]
            logosport = soup.find('img',{"alt":torneo})
            
            #if data != d.strftime("%d %B"):
            #    continue
                        
            dtevent = datetime.strptime(data + " " + str(d.year) + " " + ora, "%d %B %Y %H:%M")
            #dtevent -= timedelta(hours = 1)
            if d < dtevent:
                diff = dtevent - d  
                if diff.seconds / 60  > 30:
                    break #continue                  
                """
                if diff.days > 0:
                    break
                """
            localfile="tmp/" + link.replace("/","_") + ".html"
            try:                
                try:
                    f = open(localfile, "r", encoding="utf8")
                    for fl in f:
                        strresult += fl
                    wlog("C - " + localfile)    
                    continue
                except:
                    if d > dtevent:
                        diff = d - dtevent  
                        if diff.seconds / 60  > 30:
                            continue
                
                    req2 = get("https://livetv.sx" + link, proxies=proxies)                
                    time.sleep(0.1)
                    result2 = req2.text                
                    with open(localfile, "w", encoding='utf-8') as filew:
                        filew.write(result2)
                    soup2 = BeautifulSoup(open(localfile, encoding="utf8"), 'html.parser')
                #orario = soup2.find('meta',{"itemprop":"startDate"}).get('content')[11:16]
                orario = dtevent.strftime('%H:%M')
                titolo = soup2.find('title').text.replace(" live stream, diffusione di /", " " + orario + ".").strip()
                pos1 = titolo.find("/")
                pos2 = titolo.find(".")
                if pos1 > pos2:
                    titolo = left(titolo,pos1-1)
                else:
                    titolo = titolo.replace(" / LiveTV", "")
                    titolo = left(titolo,titolo.rfind("/")-1)
                titolo = titolo.replace(" Come guardare i.", "")
                #logosport = soup2.find('img',{"alt":titolo[titolo.find(orario)+7:]})
                if logosport is None:        
                    nomesport = soup2.find('span',{"class":"sporttitle"}).text
                    logosport = "https:" +  soup2.find('img',{"alt":nomesport}).get('src')
                    pathlogo = ""
                    logo = soup2.find('img',{"alt":"Classifica"}) 
                    if logo is not None:
                        pathlogo = "https://" + logo.get('src')
                    else:
                        pathlogo = logosport    
                else:
                    pathlogo = "https:" +  logosport.get('src')
                            
                numch = 1
                lstch = ""
                strprintace = ""
                strprint = ""                                                                                       
                for tablink in soup2.find_all('table',{"class":"lnktbj"}):
                    links = tablink.find_all('a')
                    link = links[len(links)-1].get('href','/')
                    logolink = "https:" + tablink.find('img').get('src')
                    bitrate = tablink.find('td',{"class":"bitrate"}).text
                    if link.find("webplayer") != -1 and link.find("t=acestream") == -1:
                        string_format = link.replace(left(link,link.find("?")+1), "")
                        string_format = left(string_format,string_format.find("&lang")).replace("t=","").replace("&c="," ").replace(".php","")
                        
                        if lstch.find(string_format) == -1:
                            lstch += string_format + "|"
                        else:
                            continue    
                        
                        strprint += '{'                                                                    
                        
                        if link.find("youtub") != -1:
                            strprint += f'"name":"{string_format[string_format.find(" ")+1:]}",'
                            link = string_format[string_format.find(" ")+1:]
                            strprint += f'"url":"{"https://www.youtube.com/watch?v=" + link}",'
                            if logolink is None:
                                strprint += f'"image":"https://www.youtube.com/img/desktop/yt_1200.png",'
                            else:
                                strprint += f'"image":"{logolink}",'    
                            strprint += f'"info":"YouTube"'
                        else:
                            if link.find("alieztv") != -1:
                                prefch = "AliezTv"
                            elif link.find("ifr") != -1 or link.find("voodc") != -1:
                                prefch ="WEB"
                            elif link.find("livetvstreampro") != -1:
                                prefch = "LiveTvStreamPro"
                            else:
                                prefch = link
                                    
                            if bitrate != "":
                                prefch += " " + bitrate
                                        
                            strprint += f'"name":"{string_format[string_format.find(" ")+1:].replace("_"," ").capitalize()[0:20]}",'
                            strprint += f'"url":"{"https:" + link}",'
                            if logolink is None:
                                if link.find("alieztv") != -1 or link.find("livetvstreampro") != -1:
                                    strprint += f'"image":"https://ii.apl269.me/img/logo.png",'
                                else:        
                                    strprint += f'"image":"https://play-lh.googleusercontent.com/MQycLjocQbS-WFxlIRaQURhUQVzrwGg8avma7AYc6_x-FIotjr3DIlD_YzLguZ7jofk",'
                            else:
                                strprint += f'"image":"{logolink}",'
                            strprint += f'"info":"{prefch}"'
                        strprint += '},'
                        
                        numch += 1
                        
                    elif link.find("acestream://") != -1:
                        channel = getchname(link)
                         
                        if lstch.find(channel) == -1:
                            lstch += channel + "|"
                        else:
                            continue    

                        logoch = getchlogo(link.replace("acestream://", ""))
                        if logoch != "":
                            logolink = logoch  
                        
                        strprintace += '{'
                        strprintace += f'"name":"{channel}",'
                        if logolink is None:
                            strprintace += f'"image":"https://play-lh.googleusercontent.com/HnxHBfsm9bEahEHxqNt3XzR0WE6zgAViyy7STU_EgkW8Po_0V305z6t6oyu24PLNomxz",'
                        else:
                            strprintace += f'"image":"{logolink}",'
                        strprintace += f'"url":"{link}",'
                        strprintace += f'"info":"AceStream"'
                        strprintace += '},'
                            
                        numch += 1
                    
                    else:

                        channel = "Link " + str(numch)
                         
                        if lstch.find(channel) == -1:
                            lstch += channel + "|"
                        else:
                            continue    
                        
                        strprint += '{'
                        strprint += f'"name":"{channel}",'
                        if logolink is not None:
                            strprint += f'"image":"{logolink}",'
                        strprint += f'"embed":true,'
                        strprint += f'"url":"{link}",'
                        strprint += f'"info":"{link}"'
                        strprint += '},'
                        
                        numch += 1
                            
                strprint = '{' + f'"name":"{titolo}","image":"{pathlogo}","stations":[' + strprintace + strprint + ']},'
                
                if numch > 1:                    
                    strresult += strprint
                    with open(localfile, "w", encoding='utf-8') as filetmp:
                        filetmp.write(strprint)                        
                else:
                    os.remove(localfile)    
                wlog(str(numch-1) + " - " + titolo)        
            except:
                
                try:
                    os.remove(localfile)
                    wlog("!ERRORE! " + localfile)
                except:
                    continue    
                
                continue

#print(open("include1.w3u", "r", encoding="utf8").read())
time.sleep(0.1)
                    
strresult += "]}"

dt = str(datetime.now().time())
dt = dt[:dt.find(".")]

with open("livetv.w3u", "w", encoding='utf-8') as filedone:
	filedone.write(strresult.replace("H0:M0:S0",dt))                        

filem3u = open("livetv.m3u", "w", encoding='utf-8')
filem3u.write('#EXTM3U url-tvg="http://:/search.m3u?xml_epg=1"' + '\n')

files = glob.glob("tmp/*.ace")
for file in files:
    fileace = open(file, encoding="utf8")
    chname = fileace.readline().strip()
    if chname=='' or len(chname) == 40:
        fileace.close()
        os.remove(file)
        continue    
    aceid = fileace.readline().strip()
    if aceid=='':
        engine = Engine('acestreamengine', client_console=True)
        server = Server(host='127.0.0.1', port=6878)
        engine.start()        
        search = Search(server, query=chname, group_by_channels=1, show_epg=1)
        search.get(page=0)
        try:
            aceid = str(search.results[0].items[0].channel_id)
        except:          
            aceid = 'None'
        try:
            aceimg = search.results[0].icons[0]['url']
        except:
            aceimg = 'https://placehold.co/100/lightgray/black.png?font=source-sans-pro&text=' + chname
        fileace.close()    
        fileace = open(file,"w", encoding="utf8")
        fileace.write(chname + '\n')
        fileace.write(aceid + '\n')
        fileace.write(aceimg)
    else:
        aceimg = fileace.readline().strip()            
    fileace.close()

    totrans = chname
    try:
        translated = translit(totrans,reversed=True)
    except:
        translated = totrans   

    title = f'#EXTINF:-1 tvg-id="{aceid}" tvg-logo="{aceimg}",'
    filem3u.write(title + translated + '\n')
    filename = os.path.splitext(os.path.basename(file))[0]
    filem3u.write('http://127.0.0.1:6878/ace/getstream?id=' + filename + '\n')
    
filem3u.close()

localfiles = glob.glob("tmp/*.html")
for localfile in localfiles:
    if ((time.time() - os.path.getctime(localfile)) / 60) > 360:
        os.remove(localfile)

os.system("pkill tor")

wlog("FINE\n")