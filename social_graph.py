import flet as ft
from my_control import Control

def build_social_graph_view(control: Control):
    return ft.Column(
        [
            ft.Text("Social Graph (Under Construction)", style=ft.TextThemeStyle.HEADLINE_MEDIUM),
            ft.Text("This section will allow you to visualize and manage character relationships."),
        ]
    )