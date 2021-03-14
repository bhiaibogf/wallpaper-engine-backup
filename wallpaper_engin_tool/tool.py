from wallpaper_engin_tool import *


class Tool:
    def __init__(self):
        self.__params = Params()
        self.__acf_parser = AcfParser(self.__params.path_to_workshop + 'appworkshop_431960.acf')
        self.__local_wallpaper_checker = LocalWallpaperChecker(self.__params)
        self.__deleted_wallpaper_checker = DeletedWallpaperChecker(self.__params.proxies)
        self.__network_wallpaper_checker = NetworkWallpaperChecker(self.__params.proxies, self.__params.cookies)

    def parse_workshop_acf(self):
        """
        解析 wallpaper engine 用于创意工坊的配置文件
        :return: None
        """
        print('正在解析 wallpaper engine 用于创意工坊的配置文件（注意其中仍包含已经从创意工坊消失的壁纸）')

        print('\t已安装 {} 个壁纸'.format(len(self.__acf_parser.installed_items)))
        print('\t已订阅 {} 个壁纸'.format(len(self.__acf_parser.subscribed_items)))

        self.__acf_parser.check()

    def check_local_items(self):
        """
        检查储存在本地的壁纸文件
        :return: None
        """

        print('正在扫描本地文件')

        self.__local_wallpaper_checker.list_items()
        self.__local_wallpaper_checker.check_rongyu(self.__acf_parser.subscribed_items)
        self.__local_wallpaper_checker.check_backup(self.__acf_parser.subscribed_items)

    def find_deleted_items(self):
        """
        通过尝试访问创意工坊页面，来判断对应的壁纸是否已经消失，这些消失的壁纸虽然仍在本地存有，但其不会显示在软件中，需要将其备份后才能继续使用
        :return: None
        """

        print('正在检查本地订阅')
        self.__deleted_wallpaper_checker.check(self.__local_wallpaper_checker.local_items)
        local_deleted = self.__deleted_wallpaper_checker.deleted_items
        if local_deleted:
            op = input('\t是否备份已经消失的订阅 (y/N)')
            if op == 'y':
                self.__local_wallpaper_checker.backup(local_deleted)

        print('正在检查账户订阅')
        self.__network_wallpaper_checker.html_downloader()
        self.__deleted_wallpaper_checker.deleted_items = []
        self.__deleted_wallpaper_checker.check(self.__network_wallpaper_checker.subscription)
        network_deleted = self.__deleted_wallpaper_checker.deleted_items
        op = input('\t是否下载已经消失的订阅的预览图 (y/N)')
        if op == 'y':
            self.__network_wallpaper_checker.backup(network_deleted)
