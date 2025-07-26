import flet as ft
from my_control import Control

def build_timeline_editor_view(control: Control):
    return ft.Column(
        [
            ft.Text("Gamified Timeline Editor (eventChain) (Under Construction)", style=ft.TextThemeStyle.HEADLINE_MEDIUM),
            ft.Text("This section will allow you to visualize and manage the event chain."),
        ]
    )