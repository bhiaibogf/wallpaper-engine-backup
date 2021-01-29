import os
import shutil
import sys
import threading

import requests


def parse_workshop_acf():
    """
    解析 wallpaper engine 用于创意工坊的配置文件
    :return: None
    """

    print('正在解析 wallpaper engine 用于创意工坊的配置文件（注意其中仍包含已经从创意工坊消失的壁纸）')

    # 解析文件项目
    def parser(items):
        file.readline()
        while True:
            line = file.readline()
            if line == '\t}\n':
                break
            items.append(line[3:-2])
            while True:
                if file.readline() == '\t\t}\n':
                    break

    with open(path_to_workshop + 'appworkshop_431960.acf') as file:
        # 找到已安装壁纸的开始位置
        while True:
            text = file.readline()
            if text == '\t\"WorkshopItemsInstalled\"\n':
                break

        parser(installed_items)
        print('\t已安装 {} 个壁纸'.format(len(installed_items)))

        # 找到已订阅壁纸的开始位置
        file.readline()

        parser(subscribed_items)
        print('\t已订阅 {} 个壁纸'.format(len(subscribed_items)))

    diff = set(subscribed_items).difference(set(installed_items))
    if diff:
        print('\t有 {} 个壁纸待下载'.format(len(diff)))
        op = input('\t是否等待壁纸下完后再继续运行脚本（Y/n）')
        if op != 'n':
            sys.exit()


def check_local_items():
    """
    检查储存在本地的壁纸文件
    :return: None
    """

    print('正在扫描本地文件')

    local_items.extend(os.listdir(path_to_wallpaper))
    default_items.extend(os.listdir(path_to_default))
    backup_items.extend(os.listdir(path_to_backup))

    print('\t本地有 {} 个壁纸文件（包含 {} 个官方壁纸，{} 个创意工坊壁纸，{} 个壁纸备份）'
          .format(len(default_items) + len(local_items) + len(backup_items),
                  len(default_items), len(local_items), len(backup_items)))

    # 有时已经取消订阅的壁纸可能仍未删除，以下代码可以帮你查看或删除这些壁纸
    diff = set(local_items).difference(set(installed_items))
    if not diff:
        print('\t本地无多余壁纸文件')
    else:
        op = input('\t是否在资源管理器中查看多余的 {} 个本地文件 (y/N)'.format(len(diff)))
        if op == 'y':
            for item in diff:
                path_to_item = path_to_wallpaper + item
                print(path_to_item)
                os.system("explorer.exe " + path_to_item.replace('/', '\\'))

        op = input('\t是否清除多余的本地文件 (y/N)')
        if op == 'y':
            for item in diff:
                path_to_item = path_to_wallpaper + item
                shutil.rmtree(path_to_item)
            print('清除了 {} 个壁纸文件'.format(len(diff)))

    # 查看目前备份情况
    diff2 = set(installed_items).difference(set(local_items))
    diff3 = diff2.difference(set(backup_items))
    print('\t有 {} 个订阅无本地文件，其中 {} 个已经备份'.format(len(diff2), len(diff2) - len(diff3)))


def find_deleted_items():
    """
    通过尝试访问创意工坊页面，来判断对应的壁纸是否已经消失，这些消失的壁纸虽然仍在本地存有，但其不会显示在软件中，需要将其备份后才能继续使用
    :return: None
    """

    print('正在查询网页')

    url = "https://steamcommunity.com/sharedfiles/filedetails/"

    proxy = input('\t请输入你使用的代理类型（socks5/http）（默认为 socks5）：')
    if not proxy:
        proxy = 'socks5'
    ip = input('\t请输入你代理服务器的 ip（默认为 127.0.0.1）：')
    if not ip:
        ip = '127.0.0.1'
    port = input('\t请输入你代理服务器的端口（默认为 1080）：')
    if not port:
        port = '1080'

    proxies = {
        'http': proxy + '://' + ip + ':' + port,
        'https': proxy + '://' + ip + ':' + port
    }

    def look_up(item):
        params = {"id": item}
        try:
            result = requests.get(url=url, params=params, proxies=proxies)
            if result.text.find('Error') != -1:
                deleted_items.append(item)
        except:
            pass

    threads = []
    for item in local_items:
        thread = threading.Thread(target=look_up, args=(item,))
        thread.start()
        threads.append(thread)
    for thread in threads:
        thread.join()

    if not deleted_items:
        print('\t恭喜你，你没有订阅消失')
        return

    print('\t有 {} 个订阅已消失'.format(len(deleted_items)))

    op = input('\t是否备份已经消失的订阅 (y/N)')
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
        print('\t已备份 {} 个壁纸'.format(cnt))


if __name__ == '__main__':
    path_to_steamapps = 'C:/Program Files (x86)/Steam/steamapps/'
    path = input(
        '请输入 Wallpaper Engine 所在的 steam 仓库位置（默认为 C:/Program Files (x86)/Steam/steamapps/）：\n')
    if path:
        path_to_steamapps = path
        if path[-1] != '/' and path[-1] != '\\':
            path_to_steamapps += '/'

    path_to_workshop = path_to_steamapps + 'workshop/'
    installed_items = []
    subscribed_items = []

    path_to_wallpaper_engine_projects = path_to_steamapps + 'common/wallpaper_engine/projects/'
    path_to_default = path_to_wallpaper_engine_projects + 'defaultprojects/'
    default_items = []
    path_to_backup = path_to_wallpaper_engine_projects + 'backup/'
    backup_items = []
    path_to_wallpaper = path_to_workshop + 'content/431960/'
    local_items = []

    deleted_items = []

    parse_workshop_acf()
    check_local_items()
    find_deleted_items()
