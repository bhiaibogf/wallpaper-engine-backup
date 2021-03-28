class _NetworkParams:
    def __init__(self):
        self.proxies = None
        self.cookies = ''

    @staticmethod
    def _get_proxies():
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

    @staticmethod
    def _get_cookies():
        cookies_string = input('请输入你登录 steam 后的 cookies：\n')
        cookies = {}
        for line in cookies_string.split('; '):
            name, value = line.split('=')
            cookies[name] = value
        return cookies

    def update_proxies(self):
        self.proxies = self._get_proxies()
        self.__save()

    def update_cookies(self):
        self.cookies = self._get_cookies()
        self.__save()
