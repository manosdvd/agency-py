import flet as ft
from my_control import Control
import schemas
import plot_graph
import timeline_editor

def build_case_builder_view(control: Control, asset_to_select_id: Optional[str] = None):
    """
    Builds the UI for the Case Builder view.
    """

    case_meta_tab = ft.Column(
        [
            ft.Text("Define the Crime", style=ft.TextThemeStyle.HEADLINE_MEDIUM),
                victim_dropdown = ft.Dropdown(
        label="Victim",
        options=[ft.dropdown.Option(char.id, char.fullName) for char in control.world_data.characters],
        value=control.case_data.caseMeta.victim if control.case_data.caseMeta else None,
        on_change=lambda e: control.update_case_meta('victim', e.control.value),
        tooltip="The character who is the victim of the crime."
    )
            culprit_dropdown = ft.Dropdown(
        label="Culprit",
        options=[ft.dropdown.Option(char.id, char.fullName) for char in control.world_data.characters],
        value=control.case_data.caseMeta.culprit if control.case_data.caseMeta else None,
        on_change=lambda e: control.update_case_meta('culprit', e.control.value),
        tooltip="The character who committed the crime."
    )
            crime_scene_dropdown = ft.Dropdown(
        label="Crime Scene",
        options=[ft.dropdown.Option(loc.id, loc.name) for loc in control.world_data.locations],
        value=control.case_data.caseMeta.crimeScene if control.case_data.caseMeta else None,
        on_change=lambda e: control.update_case_meta('crimeScene', e.control.value),
        tooltip="The primary location where the crime took place."
    )

            murder_weapon_dropdown = ft.Dropdown(
        label="Murder Weapon",
        options=[ft.dropdown.Option(item.id, item.name) for item in control.world_data.items],
        value=control.case_data.caseMeta.murderWeapon if control.case_data.caseMeta else None,
        on_change=lambda e: control.update_case_meta('murderWeapon', e.control.value),
        tooltip="The item used to commit the crime."
    )

            core_mystery_details = ft.TextField(
        label="Core Mystery Solution Details",
        multiline=True,
        min_lines=3,
        value=control.case_data.caseMeta.coreMysterySolutionDetails if control.case_data.caseMeta else "",
        on_change=lambda e: control.update_case_meta('coreMysterySolutionDetails', e.control.value),
        tooltip="Detailed explanation of how the mystery is solved."
    )
            ft.Checkbox(label="Murder Weapon Hidden", value=control.case_data.caseMeta.murderWeaponHidden if control.case_data.caseMeta else False, on_change=lambda e: control.update_case_meta('murderWeaponHidden', e.control.value), tooltip="Is the murder weapon hidden or not immediately obvious?"),
            ft.Dropdown(
                label="Means Clue",
                options=[ft.dropdown.Option(c.clueId, c.clueSummary) for c in control.case_data.clues],
                value=control.case_data.caseMeta.meansClue if control.case_data.caseMeta else None,
                on_change=lambda e: control.update_case_meta('meansClue', e.control.value), tooltip="The clue that reveals the means by which the crime was committed."
            ),
            ft.Dropdown(
                label="Motive Clue",
                options=[ft.dropdown.Option(c.clueId, c.clueSummary) for c in control.case_data.clues],
                value=control.case_data.caseMeta.motiveClue if control.case_data.caseMeta else None,
                on_change=lambda e: control.update_case_meta('motiveClue', e.control.value), tooltip="The clue that reveals the motive for the crime."
            ),
            ft.Dropdown(
                label="Opportunity Clue",
                options=[ft.dropdown.Option(c.clueId, c.clueSummary) for c in control.case_data.clues],
                value=control.case_data.caseMeta.opportunityClue if control.case_data.caseMeta else None,
                on_change=lambda e: control.update_case_meta('opportunityClue', e.control.value), tooltip="The clue that reveals the opportunity the culprit had."
            ),
            ft.TextField(label="Red Herring Clues (comma-separated)", value=", ".join(control.case_data.caseMeta.redHerringClues) if control.case_data.caseMeta else "", on_change=lambda e: control.update_case_meta('redHerringClues', [s.strip() for s in e.control.value.split(',')]), tooltip="Comma-separated list of clue IDs that are red herrings."),
            ft.Dropdown(
                label="Narrative Viewpoint",
                options=[ft.dropdown.Option(v) for v in schemas.CaseMeta.__annotations__['narrativeViewpoint'].__args__],
                value=control.case_data.caseMeta.narrativeViewpoint if control.case_data.caseMeta else None,
                on_change=lambda e: control.update_case_meta('narrativeViewpoint', e.control.value), tooltip="The narrative perspective of the story."
            ),
            ft.Dropdown(
                label="Narrative Tense",
                options=[ft.dropdown.Option(t) for t in schemas.CaseMeta.__annotations__['narrativeTense'].__args__],
                value=control.case_data.caseMeta.narrativeTense if control.case_data.caseMeta else None,
                on_change=lambda e: control.update_case_meta('narrativeTense', e.control.value), tooltip="The grammatical tense of the narrative."
            ),
            core_mystery_details,
            ft.Row([
                ft.TextField(label="Opening Monologue", multiline=True, min_lines=3, value=control.case_data.caseMeta.openingMonologue if control.case_data.caseMeta else "", on_change=lambda e: control.update_case_meta('openingMonologue', e.control.value), expand=True, tooltip="The opening monologue of the story."),
                ft.IconButton(icon=ft.icons.STARS, on_click=lambda e: control.generate_with_ai(control.case_data.caseMeta, 'openingMonologue')),
            ]),
            ft.Row([
                ft.TextField(label="Ultimate Reveal Scene Description", multiline=True, min_lines=3, value=control.case_data.caseMeta.ultimateRevealSceneDescription if control.case_data.caseMeta else "", on_change=lambda e: control.update_case_meta('ultimateRevealSceneDescription', e.control.value), expand=True, tooltip="Description of the scene where the mystery is finally revealed."),
                ft.IconButton(icon=ft.icons.STARS, on_click=lambda e: control.generate_with_ai(control.case_data.caseMeta, 'ultimateRevealSceneDescription')),
            ]),
            ft.Row([
                ft.TextField(label="Successful Denouement", multiline=True, min_lines=3, value=control.case_data.caseMeta.successfulDenouement if control.case_data.caseMeta else "", on_change=lambda e: control.update_case_meta('successfulDenouement', e.control.value), expand=True, tooltip="Description of the successful resolution of the story."),
                ft.IconButton(icon=ft.icons.STARS, on_click=lambda e: control.generate_with_ai(control.case_data.caseMeta, 'successfulDenouement')),
            ]),
            ft.Row([
                ft.TextField(label="Failed Denouement", multiline=True, min_lines=3, value=control.case_data.caseMeta.failedDenouement if control.case_data.caseMeta else "", on_change=lambda e: control.update_case_meta('failedDenouement', e.control.value), expand=True, tooltip="Description of a potential failed resolution of the story."),
                ft.IconButton(icon=ft.icons.STARS, on_click=lambda e: control.generate_with_ai(control.case_data.caseMeta, 'failedDenouement')),
            ]),
        ]
    )

    suspects_tab = ft.Column(
        [
            ft.Text("Manage Suspects", style=ft.TextThemeStyle.HEADLINE_MEDIUM),
            suspects_section,
        ]
    )

    clues_tab = ft.Column(
        [
            ft.Text("Manage Clues", style=ft.TextThemeStyle.HEADLINE_MEDIUM),
            clues_section,
        ]
    )

    case_locations_tab = ft.Column(
        [
            ft.Text("Manage Case Locations", style=ft.TextThemeStyle.HEADLINE_MEDIUM),
            case_locations_section,
        ]
    )

    update_case_locations_view()

    if asset_to_select_id:
        # Try to select the asset if an ID is provided
        selected_asset_obj = None
        # Check in suspects
        for suspect in control.case_data.keySuspects:
            if suspect.characterId == asset_to_select_id:
                selected_asset_obj = suspect
                break
            for iq in suspect.interview:
                if iq.questionId == asset_to_select_id:
                    selected_asset_obj = iq
                    break
            if selected_asset_obj: break
        
        # Check in clues
        if not selected_asset_obj:
            for clue in control.case_data.clues:
                if clue.clueId == asset_to_select_id:
                    selected_asset_obj = clue
                    break
        
        # Check in case locations
        if not selected_asset_obj:
            for case_loc in control.case_data.caseLocations:
                if case_loc.locationId == asset_to_select_id:
                    selected_asset_obj = case_loc
                    break
                for witness in case_loc.witnesses:
                    if witness.characterId == asset_to_select_id:
                        selected_asset_obj = witness
                        break
                if selected_asset_obj: break

        if selected_asset_obj:
            control.select_asset(selected_asset_obj)
        elif control.case_data.caseMeta and asset_to_select_id == "caseMeta":
            control.select_asset(control.case_data.caseMeta)

    return_tabs = ft.Tabs(
        selected_index=0,
        animation_duration=300,
        tabs=[
            ft.Tab(text="Case Meta", content=case_meta_tab),
            ft.Tab(text="Suspects", content=suspects_tab),
            ft.Tab(text="Clues", content=clues_tab),
            ft.Tab(text="Case Locations", content=case_locations_tab),
            ft.Tab(text="Plot Graph", content=plot_graph.build_plot_graph_view(control)),
            ft.Tab(text="Timeline Editor", content=timeline_editor.build_timeline_editor_view(control)),
        ],
        expand=1,
    )
    control.case_builder_tabs = return_tabs
    return return_tabs
