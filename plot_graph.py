import flet as ft
from my_control import Control

def build_plot_graph_view(control: Control):
    return ft.Column(
        [
            ft.Text("Interactive Bulletin Board (Plot Graph) (Under Construction)", style=ft.TextThemeStyle.HEADLINE_MEDIUM),
            ft.Text("This section will allow you to visualize and manage the plot graph."),
        ]
    )