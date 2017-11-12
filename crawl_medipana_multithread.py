import threading
import requests
from bs4 import BeautifulSoup
import re
import pandas as pd


def get_url(num):
    url = "http://www.medipana.com/news/news_viewer.asp?NewsNum={}&MainKind=A\
            &NewsKind=103&vCount=100&vKind=1&Page=1&sWord=&Qstring=".format(num)
    return url

def crawl(start, end):
    content_pattern = '\t|(\n)+|\s\s+'

    news_dict = {}
    news_dict['link'] = []
    news_dict['date'] = []
    news_dict['title'] = []
    news_dict['content'] = []

    # for num in range(187638, 209499):
    for num in range(start, end):
        link = get_url(num)
        try:
            res = requests.get(link)
            dom = BeautifulSoup(res.content, 'html5lib')
        except:
            indicator = (num, 'link')
            print ("ERROR: " + str(indicator))
            continue

        news_dict['link'].append(link)

        try:
            title = dom.find('div', {'class': 'detailL'}).text
            if title:
                news_dict['title'].append(title)
            else:
                news_dict['title'].append('none')
        except:
            news_dict['title'].append('none')
            indicator = (num, 'title')
            print ("ERROR: " + str(indicator))
            pass

        try:
            td = dom.find('td', {'width': '180'})
            date = td.find('a').text
            if date:
                news_dict['date'].append(date)
            else:
                news_dict['date'].append('none')
        except:
            news_dict['date'].append('none')
            indicator = (num, 'date')
            print ("ERROR: " + str(indicator))
            pass

        try:
            body0 = dom.find('div', {'oncopy': 'javascript:contents_cp();'}).text
            body = re.sub(content_pattern, ' ', body0)
            if body:
                news_dict['content'].append(body)
            else:
                news_dict['content'].append('none')
        except:
            news_dict['content'].append('none')
            indicator = (num, 'content')
            print ("ERROR: " + str(indicator))
            pass

        if num % 100 == 0:
            print ("    {} done".format(num))

        try:
            if num % 1000 == 0:
                df = pd.DataFrame(news_dict)
                df.to_csv('./data/medipana/medipana_{}_{}.csv'.format(start, num), encoding='utf-8-sig')
                print("SUCCESS: [{}] to[{}] saved".format(start, num))
        except:
            print ("ERROR: [{}] to[{}] not saved".format(start, num))
            pass

        if num % 50 == 0:
            print ("[{}] done".format(num))

    df = pd.DataFrame(news_dict)
    df.to_csv('./data/medipana/news_medipana_{}_{}.csv'.format(start, end), encoding='utf-8-sig')
    print ('news_medipana_{}_{}.csv saved'.format(start,end))


t_1 = threading.Thread(target=crawl, args=(187638,190000))
t_2 = threading.Thread(target=crawl, args=(190000,195000))
t_3 = threading.Thread(target=crawl, args=(195000,200000))
t_4 = threading.Thread(target=crawl, args=(200000,205000))
t_5 = threading.Thread(target=crawl, args=(205000,209499))


t_1.start()
t_2.start()
t_3.start()
t_4.start()
t_5.start()