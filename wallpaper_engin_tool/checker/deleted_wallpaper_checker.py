import threading


class DeletedWallpaperChecker:
    def __init__(self, http_getter):
        self.__http_getter = http_getter

        self.local_deleted_items = []
        self.network_deleted_items = []
        self.deleted_items = [self.local_deleted_items, self.network_deleted_items]

    def look_up(self, item, where):
        url = "https://steamcommunity.com/sharedfiles/filedetails/"
        params = {"id": item}
        result = self.__http_getter.get(url=url, params=params)
        if result.text.find('Error') != -1 or result.text.find('错误') != -1:
            self.deleted_items[where].append(item)

    def check(self, items, where):
        threads = []
        for item in items:
            thread = threading.Thread(target=self.look_up, args=(item, where))
            thread.start()
            threads.append(thread)
        for thread in threads:
            thread.join()

        if not self.deleted_items[where]:
            print('\t恭喜你，你没有订阅消失')
            return

        print('\t有 {} 个订阅已消失'.format(len(self.deleted_items[where])))
