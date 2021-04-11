import os


class _LocalParams:
    def __init__(self):
        self.path_to_steamapps = ''

        self.path_to_workshop = ''
        self.path_to_wallpaper_engine_projects = ''
        self.path_to_default = ''
        self.path_to_backup = ''
        self.path_to_wallpaper = ''

    @staticmethod
    def _input_steam_path():
        path_to_steamapps = 'C:/Program Files (x86)/Steam/steamapps/'
        path = input('请输入 Wallpaper Engine 所在的 steam 仓库位置（默认为 C:/Program Files (x86)/Steam/steamapps/）：\n')
        if path:
            path_to_steamapps = path
            if path[-1] != '/' and path[-1] != '\\':
                path_to_steamapps += '/'
        return path_to_steamapps

    def __set_paths(self):
        self.path_to_workshop = self.path_to_steamapps + 'workshop/'
        self.path_to_wallpaper_engine_projects = self.path_to_steamapps + 'common/wallpaper_engine/projects/'
        self.path_to_default = self.path_to_wallpaper_engine_projects + 'defaultprojects/'
        self.path_to_backup = self.path_to_wallpaper_engine_projects + 'backup/'
        self.path_to_wallpaper = self.path_to_workshop + 'content/431960/'

    def __check_paths(self):
        """
        检查是否所有路径都存在

        :return: 存在就返回 True
        """
        for name, path in vars(self).items():
            if os.path.isdir(path):
                continue
            else:
                print('路径 {}({}) 不存在'.format(name, path))
                return False
        return True

    def set_path(self, path):
        self.path_to_steamapps = path
        self.__set_paths()
        if self.__check_paths():
            return False
        else:
            self.set_path(self._input_steam_path())
            return True
