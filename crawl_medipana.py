import requests
from bs4 import BeautifulSoup
import re
import pandas as pd


def get_url(num):
    url = "http://www.medipana.com/news/news_viewer.asp?NewsNum={}&MainKind=A\
            &NewsKind=103&vCount=100&vKind=1&Page=1&sWord=&Qstring=".format(num)
    return url


content_pattern = '\t|(\n)+|\s\s+'

news_dict = {}
news_dict['link'] = []
news_dict['date'] = []
news_dict['title'] = []
news_dict['content'] = []

errors = []
for num in range(187638, 209499):
    link = get_url(num)
    try:
        res = requests.get(link)
        dom = BeautifulSoup(res.content, 'html5lib')
    except:
        errors.append((num, 'link'))
        continue

    news_dict['link'].append(link)

    try:
        title = dom.find('div', {'class': 'detailL'}).text
        if title:
            news_dict['title'].append(title)
        else:
            news_dict['title'].append('none')
    except:
        errors.append((num, 'title'))
        pass

    try:
        td = dom.find('td', {'width': '180'})
        date = td.find('a').text
        if date:
            news_dict['date'].append(date)
        else:
            news_dict['date'].append('none')
    except:
        errors.append((num, 'date'))
        pass

    try:
        body0 = dom.find('div', {'oncopy': 'javascript:contents_cp();'}).text
        body = re.sub(content_pattern, ' ', body0)
        if body:
            news_dict['content'].append(body)
        else:
            news_dict['content'].append('none')
    except:
        errors.append((num, 'content'))
        pass

    if num % 4000 == 0:
        df = pd.DataFrame(news_dict)
        df.to_csv('./data/medipana/news_medipana_{}.csv'.format(num), encoding='utf-8-sig')