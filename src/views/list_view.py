import flet as ft

def list_view(page: ft.Page):
    return ft.Row(
        spacing=0,
        controls=[
            ft.Container(
                content=ft.Text("List View", size=20, weight="bold"),
                margin=ft.margin.only(left=-40),
                expand=True,
            ),
        ],
        vertical_alignment=ft.CrossAxisAlignment.START,
        expand=True
    )
