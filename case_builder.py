import flet as ft
from my_control import Control

def build_case_builder_view(control: Control):
    """
    Builds the UI for the Case Builder view.
    """
    
    victim_dropdown = ft.Dropdown(
        label="Victim",
        options=[ft.dropdown.Option(char.id, char.fullName) for char in control.world_data.characters],
        value=control.case_data.caseMeta.victim if control.case_data.caseMeta else None,
        on_change=lambda e: control.update_case_meta('victim', e.control.value)
    )

    culprit_dropdown = ft.Dropdown(
        label="Culprit",
        options=[ft.dropdown.Option(char.id, char.fullName) for char in control.world_data.characters],
        value=control.case_data.caseMeta.culprit if control.case_data.caseMeta else None,
        on_change=lambda e: control.update_case_meta('culprit', e.control.value)
    )

    crime_scene_dropdown = ft.Dropdown(
        label="Crime Scene",
        options=[ft.dropdown.Option(loc.id, loc.name) for loc in control.world_data.locations],
        value=control.case_data.caseMeta.crimeScene if control.case_data.caseMeta else None,
        on_change=lambda e: control.update_case_meta('crimeScene', e.control.value)
    )

    murder_weapon_dropdown = ft.Dropdown(
        label="Murder Weapon",
        options=[ft.dropdown.Option(item.id, item.name) for item in control.world_data.items],
        value=control.case_data.caseMeta.murderWeapon if control.case_data.caseMeta else None,
        on_change=lambda e: control.update_case_meta('murderWeapon', e.control.value)
    )

    core_mystery_details = ft.TextField(
        label="Core Mystery Solution Details",
        multiline=True,
        min_lines=3,
        value=control.case_data.caseMeta.coreMysterySolutionDetails if control.case_data.caseMeta else "",
        on_change=lambda e: control.update_case_meta('coreMysterySolutionDetails', e.control.value)
    )


    return ft.Column(
        [
            ft.Text("Define the Crime", style=ft.TextThemeStyle.HEADLINE_MEDIUM),
            victim_dropdown,
            culprit_dropdown,
            crime_scene_dropdown,
            murder_weapon_dropdown,
            core_mystery_details,
            ft.ElevatedButton(text="Save Case", on_click=lambda e: control.save_data())
        ]
    )
