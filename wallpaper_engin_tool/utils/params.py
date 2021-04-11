import json
import os

from wallpaper_engin_tool.utils._local_params import _LocalParams
from wallpaper_engin_tool.utils._network_params import _NetworkParams


class Params(_LocalParams, _NetworkParams):
    def __init__(self):
        super(Params, self).__init__()

        if os.path.isfile('config.json'):
            dirty = self.__load()
        else:
            self.__input()
            dirty = True

        if dirty:
            self.__save()

    def __save(self):
        with open('config.json', 'w') as file:
            json.dump(self.path_to_steamapps, file)
            file.write('\n')
            json.dump(self.proxies, file)
            file.write('\n')
            json.dump(self.cookies, file)
        print('已更新储存信息')

    def __load(self):
        dirty = False
        with open('config.json', 'r') as file:
            dirty |= self.set_path(json.loads(file.readline()))

            dirty |= self.set_proxies(json.loads(file.readline()))
            dirty |= self.set_cookies(json.loads(file.readline()))
        return dirty

    def __input(self):
        self.set_path(self._input_steam_path())
        self.set_proxies(self._input_proxies())
        self.set_cookies(self._input_cookies())

    def __str__(self):
        info = ''
        for name, value in vars(self).items():
            info += '{}: {}\n'.format(name, value)
        return info
