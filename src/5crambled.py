import flet as ft

from home import home_page
from login import login_page
from gallery import gallery_page, remove_local
from urllib.parse import urlparse, parse_qs

def main(page: ft.Page):
    page.title = "5crambled"
    page.bgcolor = "#000000"
    page.window.maximized = True
    page.theme_mode = ft.ThemeMode.LIGHT

    def route_change(route):
        remove_local()
        url = urlparse(route.data)
        query_params = parse_qs(url.query)
        try:
            uid = query_params['uid'][0]
        except:
            uid = 'anonymous'
        try:
            data = parse_qs(query_params['data'][0])['data']
        except:
            data = None

        page.views.clear()
        page.views.append(
            ft.View(
                "/",
                controls=login_page(page)
            )
        )
        if url.path == "/home":
            hp = home_page(page, uid, data)
            page.views.append(
                ft.View(
                    "/home",
                    controls=hp.build_gui()
                )
            )
        
        if url.path == "/works":
            a = gallery_page(page, uid)
            # print(a, uid)
            page.views.clear()
            page.views.append(
                ft.View(
                    "/works",
                    controls=a
                )
            )
        page.update()

    def view_pop(view):
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)

    page.on_route_change = route_change
    page.on_view_pop = view_pop
    page.go(page.route)

ft.app(main)