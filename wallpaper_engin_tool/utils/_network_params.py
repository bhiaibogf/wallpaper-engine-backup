import requests


class _NetworkParams:
    def __init__(self):
        self.proxies = None
        self.cookies = ''
        self.user_id = ''

    @staticmethod
    def _input_proxies():
        proxy = input('请输入你使用的代理类型（socks5/http）（默认为 socks5）：')
        if not proxy:
            proxy = 'socks5'
        ip = input('请输入你代理服务器的 ip（默认为 127.0.0.1）：')
        if not ip:
            ip = '127.0.0.1'
        port = input('请输入你代理服务器的端口（默认为 1080）：')
        if not port:
            port = '1080'
        proxies = {
            'http': proxy + '://' + ip + ':' + port,
            'https': proxy + '://' + ip + ':' + port
        }
        return proxies

    @property
    def __check_proxies(self):
        try:
            requests.head('https://www.google.com', proxies=self.proxies)
            return True
        except Exception:
            print('代理信息 {} 有误'.format(self.proxies))
            return False

    def set_proxies(self, proxies):
        self.proxies = proxies
        if self.__check_proxies:
            return False
        else:
            self.set_proxies(self._input_proxies())
            return True

    @staticmethod
    def _input_cookies():
        cookies_string = input('请输入你登录 steam 后的 cookies：\n')
        cookies = {}
        for line in cookies_string.split('; '):
            name, value = line.split('=')
            cookies[name] = value
        return cookies

    def __check_cookies(self):
        try:
            session = requests.Session()
            requests.utils.add_dict_to_cookiejar(session.cookies, self.cookies)
            result = session.head('https://steamcommunity.com/my', proxies=self.proxies)
            session.close()

            location = result.headers['Location'].split('/')
            state = location[3]
            if state == 'id':
                self.user_id = location[4]
                print('你好 {}，欢迎使用 Wallpaper Engine Tool'.format(self.user_id))
            elif state == 'login':
                raise Exception
            else:
                raise Exception
            return True
        except Exception:
            print('cookies 过期')
            return False

    def set_cookies(self, cookies):
        self.cookies = cookies
        if self.__check_cookies():
            return False
        else:
            self.set_cookies(self._input_cookies())
            return True
