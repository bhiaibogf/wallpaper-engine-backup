import json
import os

from wallpaper_engin_tool.utils._local_params import _LocalParams
from wallpaper_engin_tool.utils._network_params import _NetworkParams


class Params(_LocalParams, _NetworkParams):
    def __init__(self):
        super(Params, self).__init__()

        if os.path.isfile('config.json'):
            self.__load()
        else:
            self.__input()
            self.__save()
        self._update_path()

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

    def __input(self):
        self.path_to_steamapps = self._get_steam_path()
        self.proxies = self._get_proxies()
        self.cookies = self._get_cookies()
