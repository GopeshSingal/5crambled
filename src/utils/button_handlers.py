import flet as ft

def handle_key(e: ft.KeyboardEvent, button_row, color_picker, color_palette, state, page, grid_size, cp):
    match e.key:
        case "Z" if e.ctrl or e.meta:
            if e.shift:
                state.unrevert_state(e)
            else:
                state.revert_state(e)
        case "A" if e.ctrl or e.meta:
            button_row.controls[4].selected = not button_row.controls[4].selected
            button_row.update()
            fill_button_clicked(e, state, button_row)
        case "D" if e.ctrl or e.meta:
            button_row.controls[5].selected = not button_row.controls[5].selected
            button_row.update()
            dropper_button_clicked(e, state, button_row)
        case "R" if e.ctrl or e.meta:
            reset_canvas(e, grid_size, state, cp, page)
        case "1":
            color_picker.color = color_palette.palette.controls[0].controls[0].icon_color
            color_palette.palette.controls[0].controls[0].selected = True
            color_palette.palette.controls[0].controls[0].focus()
            color_palette.palette.controls[0].controls[0].update()
            page.update()
        case "2":
            color_picker.color = color_palette.palette.controls[0].controls[1].icon_color
            color_palette.palette.controls[0].controls[1].selected = True
            color_palette.palette.controls[0].controls[1].focus()
            color_palette.palette.controls[0].controls[1].update()
            page.update()
        case "3":
            color_picker.color = color_palette.palette.controls[0].controls[2].icon_color
            color_palette.palette.controls[0].controls[2].selected = True
            color_palette.palette.controls[0].controls[2].focus()
            color_palette.palette.controls[0].controls[2].update()
            page.update()
        case "4":
            color_picker.color = color_palette.palette.controls[0].controls[3].icon_color
            color_palette.palette.controls[0].controls[3].selected = True
            color_palette.palette.controls[0].controls[3].focus()
            color_palette.palette.controls[0].controls[3].update()
            page.update()
        case "5":
            color_picker.color = color_palette.palette.controls[0].controls[4].icon_color
            color_palette.palette.controls[0].controls[4].selected = True
            color_palette.palette.controls[0].controls[4].focus()
            color_palette.palette.controls[0].controls[4].update()
            page.update()
        case "6":
            color_picker.color = color_palette.palette.controls[0].controls[5].icon_color
            color_palette.palette.controls[0].controls[5].selected = True
            color_palette.palette.controls[0].controls[5].focus()
            color_palette.palette.controls[0].controls[5].update()
            page.update()
        case "7":
            color_picker.color = color_palette.palette.controls[0].controls[6].icon_color
            color_palette.palette.controls[0].controls[6].selected = True
            color_palette.palette.controls[0].controls[6].focus()
            color_palette.palette.controls[0].controls[6].update()
            page.update()

def fill_button_clicked(e, state, button_row):
    if state.fill:
        state.fill = False
        e.control.selected = not e.control.selected
        e.control.update()
    else:
        state.fill = True
        button_row.controls[5].selected = False
        button_row.update()
        state.dropper = False
        e.control.selected = not e.control.selected
        e.control.update()

def dropper_button_clicked(e, state, button_row):
    if state.dropper:
        state.dropper = False
        e.control.selected = not e.control.selected
        e.control.update()
    else:
        state.dropper = True
        button_row.controls[4].selected = False
        button_row.update()
        state.fill = False
        e.control.selected = not e.control.selected
        e.control.update()

def reset_canvas(e, grid_size, state, cp, page):
    state.save_state()
    for i in range(grid_size):
        for j in range(grid_size):
            cp.shapes[(int)(i + j * grid_size)].paint.color = "#ffffff"
    page.update()