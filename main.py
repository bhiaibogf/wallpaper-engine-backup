from wallpaper_engin_tool import Tool

if __name__ == '__main__':
    tool = Tool()
    tool.check_local_items()
    tool.check_network_items()
    tool.find_deleted_items()
    tool.diff()
    tool.draw_venn()
