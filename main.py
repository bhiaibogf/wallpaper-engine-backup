import os
import shutil
import requests

path_to_steamapps = 'C:/Program Files (x86)/Steam/steamapps/'
installed_items = []
subscribed_items = []
local_items = []
deleted_items = []


def check_local_items():
    def parser(items):
        file.readline()
        while True:
            text = file.readline()
            if text == '\t}\n':
                break
            items.append(text[3:-2])
            while True:
                if file.readline() == '\t\t}\n':
                    break

    with open(path_to_workshop + 'appworkshop_431960.acf') as file:
        while True:
            text = file.readline()
            if text == '\t\"WorkshopItemsInstalled\"\n':
                break

        parser(installed_items)
        print('已安装 {} 个壁纸'.format(len(installed_items)))

        file.readline()

        parser(subscribed_items)
        print('已订阅 {} 个壁纸'.format(len(subscribed_items)))

    diff = set(subscribed_items).difference(set(installed_items))
    print('有 {} 个壁纸待下载'.format(len(diff)))

    local_items.extend(os.listdir(path_to_wallpaper))
    print('本地有 {} 个壁纸文件'.format(len(local_items)))

    diff = set(local_items).difference(set(installed_items))
    if not diff:
        print('本地无冗余壁纸文件')
        return

    op = input('是否在资源管理器中查看多余的本地文件 (y/N)')
    if op == 'y':
        for item in diff:
            path_to_item = path_to_wallpaper + item
            os.system("explorer.exe " + path_to_item)

    op = input('是否清除多余的本地文件 (y/N)')
    if op == 'y':
        for item in diff:
            path_to_item = path_to_wallpaper + item
            shutil.rmtree(path_to_item)
        print('清除了 {} 个壁纸文件'.format(len(diff)))


def find_deleted_items():
    url = "https://steamcommunity.com/sharedfiles/filedetails/"

    proxy = input('请输入你使用的代理类型（socks5/http），默认为 socks5')
    if not proxy:
        proxy = 'socks5'
    ip = input('请输入你代理服务器的 ip，默认为 127.0.0.1')
    if not ip:
        ip = '127.0.0.1'
    port = input('请输入你代理服务器的端口，默认为 1080')
    if not port:
        port = '1080'
    proxies = {
        'http': proxy + '://' + ip + ':' + port,
        'https': proxy + '://' + ip + ':' + port
    }

    for item in local_items:
        params = {"id": item}
        result = requests.get(url=url, params=params, proxies=proxies)
        if result.text.find('Error') != -1:
            deleted_items.append(item)
    print('有 {} 个订阅已消失'.format(len(deleted_items)))

    if not deleted_items:
        return

    path_to_backup = path_to_steamapps + 'common/wallpaper_engine/projects/backup/'
    op = input('是否备份已经消失的订阅 (y/N)')
    if op == 'y':
        if not os.path.isdir(path_to_backup):
            os.mkdir(path_to_backup)
        cnt = 0
        for item in deleted_items:
            if not os.path.isdir(path_to_backup + item):
                shutil.move(path_to_wallpaper + item, path_to_backup)
                cnt += 1
            else:
                shutil.rmtree(path_to_wallpaper + item)
        print('已备份 {} 个壁纸'.format(cnt))


if __name__ == '__main__':
    path = input('请输入 Wallpaper Engine 所在的 steam 仓库位置，（默认为 C:/Program Files (x86)/Steam/steamapps/）\n')
    if path:
        path_to_steamapps = path
        if path[-1] != '/' and path[-1] != '\\':
            path_to_steamapps += '/'
    path_to_workshop = path_to_steamapps + 'workshop/'
    path_to_wallpaper = path_to_workshop + 'content/431960/'

    check_local_items()
    find_deleted_items()
