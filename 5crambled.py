import flet as ft

from home import home_page
from login import login_page
from gallery import gallery_page, get_images


def main(page: ft.Page):
    page.title = "5crambled"
    page.bgcolor = "#000000"
    page.window.maximized = True

    def route_change(route):
        page.views.clear()
        page.views.append(
            ft.View(
                "/",
                controls=login_page(page)
            )
        )
        if page.route == "/home":
            page.views.append(
                ft.View(
                    "/home",
                    controls=home_page(page)
                )
            )
        
        if page.route == "/works":
            get_images()
            page.views.append(
                ft.View(
                    "/works",
                    controls=gallery_page(page)
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