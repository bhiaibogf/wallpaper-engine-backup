import threading

import requests


class DeletedWallpaperChecker:
    def __init__(self, proxies):
        self.deleted_items = []
        self.proxies = proxies

    def look_up(self, item):
        url = "https://steamcommunity.com/sharedfiles/filedetails/"
        params = {"id": item}
        try:
            result = requests.get(url=url, params=params, proxies=self.proxies)
            if result.text.find('Error') != -1 or result.text.find('错误') != -1:
                self.deleted_items.append(item)
        except:
            self.look_up(item)

    def check(self, items):
        threads = []
        for item in items:
            thread = threading.Thread(target=self.look_up, args=(item,))
            thread.start()
            threads.append(thread)
        for thread in threads:
            thread.join()

        if not self.deleted_items:
            print('\t恭喜你，你没有订阅消失')
            return

        print('\t有 {} 个订阅已消失'.format(len(self.deleted_items)))
