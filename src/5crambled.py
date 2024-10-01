import flet as ft

from home import HomePage
from login import LoginPage
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
        login = LoginPage(page)
        page.views.append(
            ft.View(
                "/",
                controls=login.build_page()
            )
        )
        if url.path == "/home":
            home = HomePage(page, uid, data)
            page.views.append(
                ft.View(
                    "/home",
                    controls=home.build_page()
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