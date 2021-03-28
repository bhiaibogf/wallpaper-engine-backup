import json
import os


class Params:
    def __init__(self):
        if os.path.isfile('config.json'):
            self.__load()
        else:
            self.__input()
            self.__save()
        self.__update_path()

    def __save(self):
        with open('config.json', 'w') as file:
            json.dump(self.path_to_steamapps, file)
            file.write('\n')
            json.dump(self.proxies, file)
            file.write('\n')
            json.dump(self.cookies, file)

    def __load(self):
        with open('config.json', 'r') as file:
            self.path_to_steamapps = json.loads(file.readline())
            self.proxies = json.loads(file.readline())
            self.cookies = json.loads(file.readline())

    def __update_path(self):
        self.path_to_workshop = self.path_to_steamapps + 'workshop/'
        self.path_to_wallpaper_engine_projects = self.path_to_steamapps + 'common/wallpaper_engine/projects/'
        self.path_to_default = self.path_to_wallpaper_engine_projects + 'defaultprojects/'
        self.path_to_backup = self.path_to_wallpaper_engine_projects + 'backup/'
        self.path_to_wallpaper = self.path_to_workshop + 'content/431960/'

    def __input(self):
        self.path_to_steamapps = self.__get_steam_path()
        self.proxies = self.__get_proxies()
        coo = self.__get_cookies()

        self.cookies = self.__cookies_phaser(coo)

    @staticmethod
    def __get_proxies():
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
    def __get_cookies():
        cookies = input('请输入你登录 steam 后的 cookies：\n')
        return cookies

    @staticmethod
    def __get_steam_path():
        path_to_steamapps = 'C:/Program Files (x86)/Steam/steamapps/'
        path = input('请输入 Wallpaper Engine 所在的 steam 仓库位置（默认为 C:/Program Files (x86)/Steam/steamapps/）：\n')
        if path:
            path_to_steamapps = path
            if path[-1] != '/' and path[-1] != '\\':
                path_to_steamapps += '/'
        return path_to_steamapps

    @staticmethod
    def __cookies_phaser(cookies_string):
        cookies = {}
        for line in cookies_string.split('; '):
            name, value = line.split('=')
            cookies[name] = value
        return cookies

    def update_path(self):
        self.path_to_steamapps = self.__get_steam_path()
        self.__update_path()
        self.__save()

    def update_proxies(self):
        self.proxies = self.__get_proxies()
        self.__save()

    def update_cookies(self):
        self.cookies = self.__get_cookies()
        self.__save()
