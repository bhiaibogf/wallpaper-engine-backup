import sys


class AcfParser:
    """
    解析本地 acf 文件，获取已安装的/已订阅的项目
    """

    def __init__(self, path_to_file):
        """

        :param path_to_file: acf 文件所在位置
        """
        self.file = open(path_to_file)
        self.installed_items = self.__get_installed_items()
        self.subscribed_items = self.__get_subscribed_items()

    def __parser(self):
        items = []
        self.file.readline()
        while True:
            line = self.file.readline()
            # 该类型的项目全部读完
            if line == '\t}\n':
                break
            items.append(line[3:-2])
            # 跳过项目中除了编号的条目
            while True:
                if self.file.readline() == '\t\t}\n':
                    break
        return items

    def __get_installed_items(self):
        # 找到已安装壁纸的开始位置
        while True:
            text = self.file.readline()
            if text == '\t\"WorkshopItemsInstalled\"\n':
                break
        return self.__parser()

    def __get_subscribed_items(self):
        # 找到已订阅壁纸的开始位置
        self.file.readline()
        return self.__parser()

    def check(self):
        diff = set(self.subscribed_items).difference(set(self.installed_items))
        if diff:
            print('\t有 {} 个壁纸待下载'.format(len(diff)))
            op = input('\t是否等待壁纸下完后再继续运行脚本（Y/n）')
            if op != 'n':
                sys.exit()

    def __del__(self):
        self.file.close()
