from wallpaper_engin_tool import Tool

if __name__ == '__main__':
    tool = Tool()
    tool.parse_workshop_acf()
    tool.check_local_items()
    tool.find_deleted_items()
