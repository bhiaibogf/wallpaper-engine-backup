from bs4 import BeautifulSoup


class HtmlParser:
    def __init__(self, html_text):
        self.soup = BeautifulSoup(html_text, 'html.parser')

    def parse_page_number(self):
        pages = self.soup.find_all('a', {'class': 'pagelink'})
        return max([int(page.string) for page in pages])

    def parse_content(self):
        subscription = []
        images = {}
        titles = {}
        items = self.soup.find_all('div', {'class': 'workshopItemSubscription'})
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
