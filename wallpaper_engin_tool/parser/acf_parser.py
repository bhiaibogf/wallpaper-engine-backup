"""
使用 vdf 模块解析 wallpaper engine 的 acf 配置文件
"""
import vdf


class AcfParser:
    """
    解析本地 acf 文件，获取已安装的/已订阅的项目
    """

    def __init__(self, path_to_file):
        """

        :param path_to_file: acf 文件所在位置
        """
        with open(path_to_file) as file:
            self.__dic = vdf.load(file)

    def get_installed_items(self):
        """
        获取已安装壁纸列表
        :return: 已安装壁纸列表
        """
        return list(self.__dic['AppWorkshop']['WorkshopItemsInstalled'].keys())

    def get_subscribed_items(self):
        """
        获取已订阅壁纸列表
        :return: 已订阅壁纸列表
        """
        return list(self.__dic['AppWorkshop']['WorkshopItemDetails'].keys())
