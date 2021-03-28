import os
import re

import requests
import requests.utils

from ..parser import HtmlParser


class NetworkWallpaperChecker:
    def __init__(self, proxies, cookies):
        self.__proxies = proxies
        self.__cookies = cookies
        self.subscription = []
        self.images = {}
        self.titles = {}

    def html_downloader(self):
        session = requests.Session()
        requests.utils.add_dict_to_cookiejar(session.cookies, self.__cookies)
        url = 'https://steamcommunity.com/id/bhiaibogf/myworkshopfiles/'
        params = {
            'appid': '431960',
            'browsefilter': 'mysubscriptions',
            'numperpage': 30
        }
        result = session.get(url, params=params, proxies=self.__proxies)
        html_parser = HtmlParser(result.text)
        max_page = html_parser.parse_page_number()

        for page_number in range(1, max_page + 1):
            print('\r\t正在查询第 {}/{} 页'.format(page_number, max_page), end='')
            params['p'] = page_number
            result = session.get(url, params=params, proxies=self.__proxies)
            html_parser = HtmlParser(result.text)
            subscription, images, titles = html_parser.parse_content()
            self.subscription.extend(subscription)
            self.images.update(images)
            self.titles.update(titles)

    def backup(self, deleted_items):
        if not os.path.isdir('bak'):
            os.mkdir('bak')
        for item in deleted_items:
            filename = '[{}]{}.jpg'.format(item, self.titles[item])
            safe_filename = re.compile(r'[/:*?"<>|\\]').sub('-', filename)
            path = 'bak/' + safe_filename
            if not os.path.isfile(path):
                print('\t正在下载桌面 {} 的预览图'.format(item))
                result = requests.get(self.images[item])
                with open(path, 'wb') as file:
                    file.write(result.content)
