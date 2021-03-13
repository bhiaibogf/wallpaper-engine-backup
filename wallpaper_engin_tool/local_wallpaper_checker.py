import os
import shutil


class LocalWallpaperChecker:
    def __init__(self, params):
        self.params = params
        self.default_items = os.listdir(params.path_to_default)
        self.backup_items = os.listdir(params.path_to_backup)
        self.local_items = os.listdir(params.path_to_wallpaper)

    def list_items(self):
        print('\t本地有 {} 个壁纸文件（包含 {} 个官方壁纸，{} 个创意工坊壁纸，{} 个壁纸备份）'
              .format(len(self.default_items) + len(self.local_items) + len(self.backup_items),
                      len(self.default_items), len(self.local_items), len(self.backup_items)))

    def check_rongyu(self, subscribed_items):
        # 有时已经取消订阅的壁纸可能仍未删除，以下代码可以帮你查看或删除这些壁纸
        diff = set(self.local_items).difference(set(subscribed_items))
        if not diff:
            print('\t本地无多余壁纸文件')
        else:
            op = input('\t是否在资源管理器中查看多余的 {} 个本地文件 (y/N)'.format(len(diff)))
            if op == 'y':
                for item in diff:
                    path_to_item = self.params.path_to_wallpaper + item
                    # print(path_to_item)
                    os.system("explorer.exe " + path_to_item.replace('/', '\\'))

            op = input('\t是否清除多余的本地文件 (y/N)')
            if op == 'y':
                for item in diff:
                    path_to_item = self.params.path_to_wallpaper + item
                    shutil.rmtree(path_to_item)
                print('清除了 {} 个壁纸文件'.format(len(diff)))

    def check_backup(self, subscribed_items):
        # 查看目前备份情况
        diff2 = set(subscribed_items).difference(set(self.local_items))
        diff3 = diff2.difference(set(self.backup_items))
        print('\t有 {} 个订阅无本地文件，其中 {} 个已经备份'.format(len(diff2), len(diff2) - len(diff3)))

    def backup(self, deleted_items):
        if not os.path.isdir(self.params.path_to_backup):
            os.mkdir(self.params.path_to_backup)
        cnt = 0
        for item in deleted_items:
            if not os.path.isdir(self.params.path_to_backup + item):
                shutil.move(self.params.path_to_wallpaper + item, self.params.path_to_backup)
                cnt += 1
            else:
                shutil.rmtree(self.params.path_to_wallpaper + item)
        print('\t已备份 {} 个壁纸'.format(cnt))
