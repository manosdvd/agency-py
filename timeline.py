import flet as ft
from my_control import Control

def build_timeline_view(control: Control):
    return ft.Column(
        [
            ft.Text("Lore & World History Timeline (Under Construction)", style=ft.TextThemeStyle.HEADLINE_MEDIUM),
            ft.Text("This section will allow you to visualize and manage historical events."),
        ]
    )