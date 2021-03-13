class Params:
    def __init__(self):
        # self.path_to_steamapps = 'C:/Program Files (x86)/Steam/steamapps/'
        self.path_to_steamapps = self.__get_steam_path()
        self.update_path()
        self.proxies = self.__get_proxies()

    def update_path(self):
        self.path_to_workshop = self.path_to_steamapps + 'workshop/'
        self.path_to_wallpaper_engine_projects = self.path_to_steamapps + 'common/wallpaper_engine/projects/'
        self.path_to_default = self.path_to_wallpaper_engine_projects + 'defaultprojects/'
        self.path_to_backup = self.path_to_wallpaper_engine_projects + 'backup/'
        self.path_to_wallpaper = self.path_to_workshop + 'content/431960/'

    def __get_proxies(self):
        proxy = input('\t请输入你使用的代理类型（socks5/http）（默认为 socks5）：')
        if not proxy:
            proxy = 'socks5'
        ip = input('\t请输入你代理服务器的 ip（默认为 127.0.0.1）：')
        if not ip:
            ip = '127.0.0.1'
        port = input('\t请输入你代理服务器的端口（默认为 1080）：')
        if not port:
            port = '1080'
        proxies = {
            'http': proxy + '://' + ip + ':' + port,
            'https': proxy + '://' + ip + ':' + port
        }
        return proxies

    def __get_steam_path(self):
        path_to_steamapps = 'C:/Program Files (x86)/Steam/steamapps/'
        path = input(
            '请输入 Wallpaper Engine 所在的 steam 仓库位置（默认为 C:/Program Files (x86)/Steam/steamapps/）：\n')
        if path:
            path_to_steamapps = path
            if path[-1] != '/' and path[-1] != '\\':
                path_to_steamapps += '/'
        return path_to_steamapps
