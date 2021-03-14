import requests
import requests.utils
from bs4 import BeautifulSoup


class NetworkWallpaperChecker:
    def __init__(self, proxies, cookies):
        self.proxies = proxies
        self.cookies = cookies
        self.subscription = []

    def page_parser(self, html_text):
        soup = BeautifulSoup(html_text, 'html.parser')
        pages = soup.find_all('a', {'class': 'pagelink'})
        return max([int(page.string) for page in pages])

    def html_parser(self, html_text):
        soup = BeautifulSoup(html_text, 'html.parser')
        items = soup.find_all('div', {'class': 'workshopItemSubscription'})
        for item in items:
            try:
                item_id = item['id'][12:]
                img = item.img['src'].split('?')[0]
                details = item.div.contents[3]
                title = details.a.div.string
                self.subscription.append(item_id)
            except TypeError:
                continue

    def html_downloader(self):
        session = requests.Session()
        requests.utils.add_dict_to_cookiejar(session.cookies, self.cookies)
        url = 'https://steamcommunity.com/id/bhiaibogf/myworkshopfiles/'
        params = {
            'appid': '431960',
            'browsefilter': 'mysubscriptions',
            'numperpage': 30
        }
        rst = session.get(url, params=params, proxies=self.proxies)
        pages = self.page_parser(rst.text)
        for page in range(1, pages + 1):
            print('正在查询第{}页'.format(page))
            params['p'] = page
            rst = session.get(url, params=params, proxies=self.proxies)
            self.html_parser(rst.text)
        # with open('html/p1.html', 'wb') as file:
        #     file.write(rst.content)
