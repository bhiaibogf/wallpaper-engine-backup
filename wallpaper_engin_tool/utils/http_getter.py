import requests
import requests.utils


class HttpGetter:
    def __init__(self, proxies, cookies):
        self.__proxies = proxies

        self.__session = requests.Session()
        requests.utils.add_dict_to_cookiejar(self.__session.cookies, cookies)

    def get(self, url, params=None):
        try:
            result = self.__session.get(url=url, params=params, proxies=self.__proxies)
            if not result:
                raise Exception
            return result
        except Exception:
            return self.get(url, params)
