import flet as ft
from my_control import Control

def build_map_tool_view(control: Control):
    return ft.Column(
        [
            ft.Text("Map Tool (Under Construction)", style=ft.TextThemeStyle.HEADLINE_MEDIUM),
            ft.Text("This section will allow you to visualize and manage locations."),
        ]
    )