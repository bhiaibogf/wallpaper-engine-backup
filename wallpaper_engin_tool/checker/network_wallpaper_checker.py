import os
import re

from ..parser import HtmlParser


class NetworkWallpaperChecker:
    def __init__(self, user_id, http_getter):
        self.__user_id = user_id
        self.__http_getter = http_getter

        self.subscription = []
        self.images = {}
        self.titles = {}

    def html_downloader(self):
        url = 'https://steamcommunity.com/id/{}/myworkshopfiles/'.format(self.__user_id)
        params = {
            'appid': '431960',
            'browsefilter': 'mysubscriptions',
            'numperpage': 30
        }
        result = self.__http_getter.get(url, params)
        html_parser = HtmlParser(result.text)
        max_page = html_parser.parse_page_number()

        for page_number in range(1, max_page + 1):
            print('\r\t正在查询第 {}/{} 页'.format(page_number, max_page), end='')
            params['p'] = page_number
            result = self.__http_getter.get(url, params)
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
                result = self.__http_getter.get(self.images[item])
                with open(path, 'wb') as file:
                    file.write(result.content)
