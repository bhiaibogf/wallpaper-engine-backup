class AcfParser:
    """
    解析本地 acf 文件，获取已安装的/已订阅的项目
    """

    def __init__(self, path_to_file):
        """

        :param path_to_file: acf 文件所在位置
        """
        with open(path_to_file) as file:
            self.lines = file.readlines()
        self.idx = 0

    def __parse(self):
        items = []
        self.idx += 1
        while True:
            self.idx += 1
            # 该类型的项目全部读完
            if self.lines[self.idx] == '\t}\n':
                break
            items.append(self.lines[self.idx][3:-2])
            # 跳过项目中除了编号的条目
            while True:
                self.idx += 1
                if self.lines[self.idx] == '\t\t}\n':
                    break
        return items

    def get_installed_items(self):
        # 找到已安装壁纸的开始位置
        while True:
            self.idx += 1
            text = self.lines[self.idx]
            if text == '\t\"WorkshopItemsInstalled\"\n':
                break
        return self.__parse()

    def get_subscribed_items(self):
        # 找到已订阅壁纸的开始位置
        self.idx += 1
        return self.__parse()
