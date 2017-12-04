import pandas as pd
import threading
import numpy as np
import re
import os
import requests

df_all = pd.read_csv('./data/all_news_1125.csv', encoding='utf-8-sig')
df_label = pd.read_csv('./data/labeled_news.csv', encoding='utf-8-sig')

def check_url(start, end, correct_url):
    print('loop started')
    for i, url in enumerate(df_label.url[start: end]):
        if 'http://www.sisamediin.com' in url:
            correct_url.append(url)
            if i + 1 % 100 == 0:
                print('{}/{}done'.format(i + 1, 1000))
        else:
            try:
                res = requests.get(url)
                correct_url.append(res.url)
                if i+1 % 100 == 0:
                    print('{}/{}done'.format(i+1,1000))
            except:
                if i+1 % 100 == 0:
                    print("{}번,   링크 : {}".format(i, url))
                correct_url.append(url)

correct_url1 = []
correct_url2 = []
correct_url3 = []
correct_url4 = []
correct_url5 = []
correct_url6 = []
correct_url7 = []
correct_url8 = []

t1 = threading.Thread(target=check_url, args=(0,1000,correct_url1))
t2 = threading.Thread(target=check_url, args=(1000,2000,correct_url2))
t3 = threading.Thread(target=check_url, args=(2000,3000,correct_url3))
t4 = threading.Thread(target=check_url, args=(3000,4000,correct_url4))
t5 = threading.Thread(target=check_url, args=(4000,5000,correct_url5))
t6 = threading.Thread(target=check_url, args=(5000,6000,correct_url6))
t7 = threading.Thread(target=check_url, args=(6000,7000,correct_url7))
t8 = threading.Thread(target=check_url, args=(7000,8000,correct_url8))

t1.start()
t2.start()
t3.start()
t4.start()
t5.start()
t6.start()
t7.start()
t8.start()

t1.join()
t2.join()
t3.join()
t4.join()
t5.join()
t6.join()
t7.join()
t8.join()

correct_url1.extend(correct_url2)
correct_url1.extend(correct_url3)
correct_url1.extend(correct_url4)
correct_url1.extend(correct_url5)
correct_url1.extend(correct_url6)
correct_url1.extend(correct_url7)
correct_url1.extend(correct_url8)

print('extended')

with open('./data/new_urls.txt', 'w') as f:
    for url in correct_url1:
        f.write('{}\n'.format(url))

print('text write done')

df_label['new_url'] = correct_url1
df_label.to_csv('./data/labeled_new.csv', encoding='utf-8-sig', index=False)

print('done')