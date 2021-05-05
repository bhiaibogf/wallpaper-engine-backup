"""
使用 BeautifulSoup 模块解析 html 的模块
"""
from bs4 import BeautifulSoup


class HtmlParser:
    """
    用于解析创意工坊网页的类
    """

    def __init__(self, html_text):
        self.__soup = BeautifulSoup(html_text, 'html.parser')

    def parse_page_number(self):
        """
        解析用户订阅的最大页码
        :return: 用户订阅的最大页码
        """
        pages = self.__soup.find_all('a', {'class': 'pagelink'})
        return max([int(page.string) for page in pages])

    def parse_content(self):
        """
        解析订阅页中每一个订阅
        :return: list[订阅 id]，dic{预览图}，dic{标题}
        """
        subscription = []
        images = {}
        titles = {}
        items = self.__soup.find_all('div', {'class': 'workshopItemSubscription'})
        for item in items:
            try:
                item_id = item['id'][12:]
                image = item.img['src'].split('?')[0]
                details = item.div.contents[3]
                title = details.a.div.string

                subscription.append(item_id)
                images[item_id] = image
                titles[item_id] = title
            except TypeError:
                continue
        return subscription, images, titles
