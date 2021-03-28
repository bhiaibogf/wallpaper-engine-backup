class _LocalParams:
    def __init__(self):
        self.path_to_steamapps = ''

        self.path_to_workshop = ''
        self.path_to_wallpaper_engine_projects = ''
        self.path_to_default = ''
        self.path_to_backup = ''
        self.path_to_wallpaper = ''

    def _update_path(self):
        self.path_to_workshop = self.path_to_steamapps + 'workshop/'
        self.path_to_wallpaper_engine_projects = self.path_to_steamapps + 'common/wallpaper_engine/projects/'
        self.path_to_default = self.path_to_wallpaper_engine_projects + 'defaultprojects/'
        self.path_to_backup = self.path_to_wallpaper_engine_projects + 'backup/'
        self.path_to_wallpaper = self.path_to_workshop + 'content/431960/'

    @staticmethod
    def _get_steam_path():
        path_to_steamapps = 'C:/Program Files (x86)/Steam/steamapps/'
        path = input('请输入 Wallpaper Engine 所在的 steam 仓库位置（默认为 C:/Program Files (x86)/Steam/steamapps/）：\n')
        if path:
            path_to_steamapps = path
            if path[-1] != '/' and path[-1] != '\\':
                path_to_steamapps += '/'
        return path_to_steamapps

    def update_path(self):
        self.path_to_steamapps = self._get_steam_path()
        self._update_path()
        self.__save()
