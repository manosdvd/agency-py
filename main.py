import flet as ft
import data_manager
from schemas import WorldData, CaseData

def main(page: ft.Page):
    page.title = "The Agency"
    page.window_width = 1200
    page.window_height = 800

    world_data: WorldData = None
    case_data: CaseData = None

    def load_initial_data():
        nonlocal world_data, case_data
        try:
            world_data, case_data = data_manager.load_case("The Crimson Stain")
        except FileNotFoundError:
            data_manager.create_new_case("The Crimson Stain")
            world_data, case_data = data_manager.load_case("The Crimson Stain")

    def nav_changed(e):
        selected_index = e.control.selected_index
        main_content.controls.clear()

        if selected_index == 0:
            main_content.controls.append(build_world_builder())
        elif selected_index == 1:
            main_content.controls.append(ft.Text("Case Builder View - Coming Soon!"))
        elif selected_index == 2:
            main_content.controls.append(ft.Text("Validator View - Coming Soon!"))
        
        page.update()

    def build_world_builder():
        asset_tabs = ft.Tabs(
            selected_index=0,
            animation_duration=300,
            tabs=[
                ft.Tab(text="Characters"),
                ft.Tab(text="Locations"),
                ft.Tab(text="Items"),
                ft.Tab(text="Factions"),
                ft.Tab(text="Districts"),
                ft.Tab(text="Sleuth"),
            ],
            expand=1,
        )

        character_view = create_asset_editor("Characters", world_data.characters)
        
        # This is a placeholder for the content of the tabs
        asset_tabs.content = ft.Column([
            character_view
        ])

        return ft.Column([asset_tabs], expand=True)

    def create_asset_editor(asset_name, asset_list):
        asset_list_view = ft.ListView(expand=1, spacing=10, padding=20)
        if asset_list:
            for asset in asset_list:
                # Use fullName for Characters, name for others
                display_name = getattr(asset, 'fullName', getattr(asset, 'name', 'Unknown'))
                asset_list_view.controls.append(ft.Text(display_name))

        form_view = ft.Column(
            [
                ft.TextField(label="ID"),
                ft.TextField(label="Full Name"),
                ft.TextField(label="Biography", multiline=True, min_lines=3),
                ft.TextField(label="Personality"),
                ft.Dropdown(
                    label="Alignment",
                    options=[
                        ft.dropdown.Option("Lawful Good"),
                        ft.dropdown.Option("Neutral Good"),
                        ft.dropdown.Option("Chaotic Good"),
                        ft.dropdown.Option("Lawful Neutral"),
                        ft.dropdown.Option("True Neutral"),
                        ft.dropdown.Option("Chaotic Neutral"),
                        ft.dropdown.Option("Lawful Evil"),
                        ft.dropdown.Option("Neutral Evil"),
                        ft.dropdown.Option("Chaotic Evil"),
                    ],
                ),
                ft.TextField(label="Honesty", keyboard_type=ft.KeyboardType.NUMBER),
                ft.TextField(label="Victim Likelihood", keyboard_type=ft.KeyboardType.NUMBER),
                ft.TextField(label="Killer Likelihood", keyboard_type=ft.KeyboardType.NUMBER),
                ft.TextField(label="Alias"),
                ft.TextField(label="Age", keyboard_type=ft.KeyboardType.NUMBER),
                ft.Dropdown(
                    label="Gender",
                    options=[
                        ft.dropdown.Option("Male"),
                        ft.dropdown.Option("Female"),
                        ft.dropdown.Option("Nonbinary"),
                        ft.dropdown.Option("Trans Man"),
                        ft.dropdown.Option("Trans Woman"),
                        ft.dropdown.Option("Unknown"),
                        ft.dropdown.Option("Unspecified"),
                    ],
                ),
                ft.TextField(label="Employment"),
                ft.TextField(label="Image"),
                ft.TextField(label="Faction"),
                ft.Dropdown(
                    label="Wealth Class",
                    options=[
                        ft.dropdown.Option("Old Money Rich"),
                        ft.dropdown.Option("New Money Rich"),
                        ft.dropdown.Option("Business Person"),
                        ft.dropdown.Option("Working Stiff"),
                        ft.dropdown.Option("Poor"),
                        ft.dropdown.Option("Transient"),
                    ],
                ),
                ft.TextField(label="District"),
                ft.TextField(label="Motivations (comma-separated)"),
                ft.TextField(label="Secrets (comma-separated)"),
                ft.TextField(label="Allies (comma-separated)"),
                ft.TextField(label="Enemies (comma-separated)"),
                ft.TextField(label="Items (comma-separated)"),
                ft.TextField(label="Archetype"),
                ft.TextField(label="Values (comma-separated)"),
                ft.TextField(label="Flaws/Handicaps/Limitations (comma-separated)"),
                ft.TextField(label="Quirks (comma-separated)"),
                ft.TextField(label="Characteristics (comma-separated)"),
                ft.TextField(label="Vulnerabilities (comma-separated)"),
                ft.TextField(label="Voice Model"),
                ft.TextField(label="Dialogue Style"),
                ft.TextField(label="Expertise (comma-separated)"),
                ft.TextField(label="Portrayal Notes"),
            ],
            expand=True,
            scroll=ft.ScrollMode.AUTO,
        )

        return ft.Row(
            [
                ft.Column([ft.Text(f"{asset_name} List", style=ft.TextThemeStyle.HEADLINE_SMALL), asset_list_view], expand=1),
                ft.VerticalDivider(width=1),
                form_view,
            ],
            expand=True,
        )

    nav_rail = ft.NavigationRail(
        selected_index=0,
        label_type=ft.NavigationRailLabelType.ALL,
        group_alignment=-0.9,
        destinations=[
            ft.NavigationRailDestination(
                icon=ft.Icon(ft.Icons.BUILD_CIRCLE_OUTLINED),
                selected_icon=ft.Icon(ft.Icons.BUILD_CIRCLE),
                label="World Builder",
            ),
            ft.NavigationRailDestination(
                icon=ft.Icon(ft.Icons.FOLDER_SPECIAL_OUTLINED),
                selected_icon=ft.Icon(ft.Icons.FOLDER_SPECIAL),
                label="Case Builder",
            ),
            ft.NavigationRailDestination(
                icon=ft.Icon(ft.Icons.CHECK_CIRCLE_OUTLINE),
                selected_icon=ft.Icon(ft.Icons.CHECK_CIRCLE),
                label_content=ft.Text("Validator"),
            ),
        ],
        on_change=nav_changed,
    )

    main_content = ft.Column(expand=True)
    
    # Initial load
    load_initial_data()
    main_content.controls.append(build_world_builder())


    page.add(
        ft.Row(
            [
                nav_rail,
                ft.VerticalDivider(width=1),
                main_content,
            ],
            expand=True,
        )
    )

if __name__ == "__main__":
    ft.app(target=main)
