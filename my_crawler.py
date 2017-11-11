# 메디파나뉴스 크롤링 -> 방화벽
url = 'http://www.medipana.com/news/news_list_new.asp?MainKind=B&NewsKind=103&vCount=12&vKind=1'
site = 'http://www.medipana.com/news/'

gisa_links = []

res = requests.get(url)
dom = BeautifulSoup(res.content, 'html5lib')
pages = dom.findAll('tbody')

for page in pages:
    try:
        if 'news_viewer' in page.find('a').attrs['href']:
            if (site + page.find('a').attrs['href']) not in gisa_links:
                if len(page.find('a').attrs['href']) > 100:
                    gisa_links.append(site + page.find('a').attrs['href'])
    except:
        pass

for gisa_link in gisa_links:
    res = requests.get(gisa_link)
    dom = BeautifulSoup(res.content, 'html5lib')
    # title = dom.find('div',{'class':'detailL'})
    print (dom.text)

    # stitle = dom.find('a',{'class':'top_middle_title1'}).get_text()
    # content = dom.find('td',{'id':'articleBody'}).get_text()
    # print(title, stitle)