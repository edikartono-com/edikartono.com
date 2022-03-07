from posts.views import ProcessMenu

menus = ProcessMenu()

def main_menu(context):
    main = menus.main_menu()
    return {'main_menu': main}

def page_menu(context):
    page = menus.page_menu()
    return {'page_menu': page}