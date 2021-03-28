from matplotlib import pyplot as plt
from venn import venn

from .checker import LocalWallpaperChecker, DeletedWallpaperChecker, NetworkWallpaperChecker
from .utils import Params, HttpGetter


class Tool:
    def __init__(self):
        params = Params()
        http_getter = HttpGetter(params.proxies, params.cookies)

        self.__local_wallpaper_checker = LocalWallpaperChecker(params)
        self.__deleted_wallpaper_checker = DeletedWallpaperChecker(http_getter)
        self.__network_wallpaper_checker = NetworkWallpaperChecker(http_getter)

    def check_local_items(self):
        """
        解析 wallpaper engine 用于创意工坊的配置文件, 检查储存在本地的壁纸文件
        :return: None
        """

        print('正在解析 wallpaper engine 用于创意工坊的配置文件（包含已从创意工坊消失的壁纸）')
        print('\t已安装 {} 个壁纸'.format(len(self.__local_wallpaper_checker.installed_items)))
        print('\t已订阅 {} 个壁纸'.format(len(self.__local_wallpaper_checker.subscribed_items)))
        self.__local_wallpaper_checker.checked_uninstalled()

        print('正在扫描本地文件')
        self.__local_wallpaper_checker.list_items()
        self.__local_wallpaper_checker.check_undeleted()
        self.__local_wallpaper_checker.check_backup()

    def check_network_items(self):
        print('正在查询账户订阅情况')
        self.__network_wallpaper_checker.html_downloader()
        print('\n\t你订阅了 {} 个壁纸'.format(len(self.__network_wallpaper_checker.subscription)))

    def find_deleted_items(self):
        """
        通过尝试访问创意工坊页面，来判断对应的壁纸是否已经消失，这些消失的壁纸虽然仍在本地存有，但其不会显示在软件中，需要将其备份后才能继续使用
        :return: None
        """

        print('正在检查本地订阅')
        self.__deleted_wallpaper_checker.check(self.__local_wallpaper_checker.local_items, 0)
        if self.__deleted_wallpaper_checker.local_deleted_items:
            op = input('\t是否备份已经消失的订阅 (y/N)')
            if op == 'y':
                self.__local_wallpaper_checker.backup(self.__deleted_wallpaper_checker.local_deleted_items)

        print('正在检查账户订阅')
        self.__deleted_wallpaper_checker.check(self.__network_wallpaper_checker.subscription, 1)
        if self.__deleted_wallpaper_checker.network_deleted_items:
            op = input('\t是否下载已经消失的订阅的预览图 (y/N)')
            if op == 'y':
                self.__network_wallpaper_checker.backup(self.__deleted_wallpaper_checker.network_deleted_items)

    def draw_venn(self):
        dct = {
            'local_items': set(self.__local_wallpaper_checker.local_items),
            'backup_items': set(self.__local_wallpaper_checker.backup_items),
            'network_items': set(self.__network_wallpaper_checker.subscription),
            'deleted_items': set(self.__deleted_wallpaper_checker.network_deleted_items),
        }
        venn(dct)

        plt.draw()
        plt.show()

    @staticmethod
    def __diff(list1, list2):
        return set(list1).difference(set(list2))

    def diff(self):
        diff_backup_subscribed = self.__diff(self.__local_wallpaper_checker.backup_items,
                                             self.__local_wallpaper_checker.subscribed_items)
        print('你备份了 {} 个完全消失的壁纸, 他们是: \n\t{}'.format(len(diff_backup_subscribed), diff_backup_subscribed))
        diff_deleted_backup = self.__diff(self.__deleted_wallpaper_checker.network_deleted_items,
                                          self.__local_wallpaper_checker.backup_items)
        print('你损失了 {} 个消失的壁纸, 他们是: \n\t{}'.format(len(diff_deleted_backup), diff_deleted_backup))
        diff_local_network = self.__diff(self.__local_wallpaper_checker.local_items,
                                         self.__network_wallpaper_checker.subscription)
        print('你有 {} 个壁纸订阅异常, 他们是: \n\t{}'.format(len(diff_local_network), diff_local_network))
