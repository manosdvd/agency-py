import flet as ft
from my_control import Control
import schemas
import case_builder

def main(page: ft.Page):
    page.title = "The Agency"
    page.window_width = 1200
    page.window_height = 800

    # Create a single instance of the Control class
    app_control = Control(page)

    def nav_changed(e):
        selected_index = e.control.selected_index
        main_content.controls.clear()

        if selected_index == 0:
            main_content.controls.append(build_world_builder(app_control))
        elif selected_index == 1:
            main_content.controls.append(case_builder.build_case_builder_view(app_control))
        elif selected_index == 2:
            main_content.controls.append(ft.Text("Validator View - Coming Soon!"))
        
        page.update()

    def build_world_builder(control: Control):
        
        character_view = create_asset_editor(control, "Characters", control.world_data.characters)
        location_view = create_asset_editor(control, "Locations", control.world_data.locations)
        item_view = create_asset_editor(control, "Items", control.world_data.items)
        faction_view = create_asset_editor(control, "Factions", control.world_data.factions)
        district_view = create_asset_editor(control, "Districts", control.world_data.districts)
        sleuth_view = create_asset_editor(control, "Sleuth", [control.world_data.sleuth] if control.world_data.sleuth else [])

        asset_tabs = ft.Tabs(
            selected_index=0,
            animation_duration=300,
            tabs=[
                ft.Tab(text="Characters", content=character_view),
                ft.Tab(text="Locations", content=location_view),
                ft.Tab(text="Items", content=item_view),
                ft.Tab(text="Factions", content=faction_view),
                ft.Tab(text="Districts", content=district_view),
                ft.Tab(text="Sleuth", content=sleuth_view),
            ],
            expand=1,
        )

        return ft.Column([asset_tabs], expand=True)

    def create_asset_editor(control: Control, asset_name: str, asset_list: list):
        
        def on_asset_click(e):
            # Find the asset in the asset_list by its display name
            clicked_asset_name = e.control.title.value
            for asset in asset_list:
                display_name = getattr(asset, 'fullName', getattr(asset, 'name', 'Unknown'))
                if display_name == clicked_asset_name:
                    control.select_asset(asset)
                    break
            update_form()

        def build_asset_list():
            asset_list_view.controls.clear()
            if asset_list:
                for asset in asset_list:
                    display_name = getattr(asset, 'fullName', getattr(asset, 'name', 'Unknown'))
                    asset_list_view.controls.append(
                        ft.ListTile(
                            title=ft.Text(display_name),
                            on_click=on_asset_click,
                        )
                    )
        
        asset_list_view = ft.ListView(expand=1, spacing=10, padding=20)
        build_asset_list()

        form_view = ft.Column(
            expand=True,
            scroll=ft.ScrollMode.AUTO,
        )

        def handle_new_asset(e):
            if asset_name == "Characters":
                control.create_new_character()
            elif asset_name == "Locations":
                control.create_new_location()
            elif asset_name == "Items":
                control.create_new_item()
            elif asset_name == "Factions":
                control.create_new_faction()
            elif asset_name == "Districts":
                control.create_new_district()
            build_asset_list()
            update_form()

        def update_form():
            form_view.controls.clear()
            if control.selected_asset:
                if isinstance(control.selected_asset, schemas.Character):
                    char = control.selected_asset
                    form_view.controls.extend([
                        ft.TextField(label="ID", value=char.id, on_change=lambda e: control.update_selected_asset('id', e.control.value)),
                        ft.TextField(label="Full Name", value=char.fullName, on_change=lambda e: control.update_selected_asset('fullName', e.control.value)),
                        ft.TextField(label="Biography", value=char.biography, multiline=True, min_lines=3, on_change=lambda e: control.update_selected_asset('biography', e.control.value)),
                        ft.TextField(label="Personality", value=char.personality, on_change=lambda e: control.update_selected_asset('personality', e.control.value)),
                        ft.Dropdown(
                            label="Alignment",
                            options=[ft.dropdown.Option(a) for a in schemas.Alignment.__args__],
                            value=char.alignment,
                            on_change=lambda e: control.update_selected_asset('alignment', e.control.value)
                        ),
                        ft.TextField(label="Honesty", value=str(char.honesty), keyboard_type=ft.KeyboardType.NUMBER, on_change=lambda e: control.update_selected_asset('honesty', e.control.value)),
                        ft.TextField(label="Victim Likelihood", value=str(char.victimLikelihood), keyboard_type=ft.KeyboardType.NUMBER, on_change=lambda e: control.update_selected_asset('victimLikelihood', e.control.value)),
                        ft.TextField(label="Killer Likelihood", value=str(char.killerLikelihood), keyboard_type=ft.KeyboardType.NUMBER, on_change=lambda e: control.update_selected_asset('killerLikelihood', e.control.value)),
                        ft.TextField(label="Alias", value=char.alias, on_change=lambda e: control.update_selected_asset('alias', e.control.value)),
                        ft.TextField(label="Age", value=str(char.age), keyboard_type=ft.KeyboardType.NUMBER, on_change=lambda e: control.update_selected_asset('age', e.control.value)),
                        ft.Dropdown(
                            label="Gender",
                            options=[ft.dropdown.Option(g) for g in schemas.Gender.__args__],
                            value=char.gender,
                            on_change=lambda e: control.update_selected_asset('gender', e.control.value)
                        ),
                        ft.TextField(label="Employment", value=char.employment, on_change=lambda e: control.update_selected_asset('employment', e.control.value)),
                        ft.TextField(label="Image", value=char.image, on_change=lambda e: control.update_selected_asset('image', e.control.value)),
                        ft.TextField(label="Faction", value=char.faction, on_change=lambda e: control.update_selected_asset('faction', e.control.value)),
                        ft.Dropdown(
                            label="Wealth Class",
                            options=[ft.dropdown.Option(w) for w in schemas.WealthClass.__args__],
                            value=char.wealthClass,
                            on_change=lambda e: control.update_selected_asset('wealthClass', e.control.value)
                        ),
                        ft.TextField(label="District", value=char.district, on_change=lambda e: control.update_selected_asset('district', e.control.value)),
                        ft.TextField(label="Motivations", value=", ".join(char.motivations), on_change=lambda e: control.update_selected_asset('motivations', [s.strip() for s in e.control.value.split(',')])),
                        ft.TextField(label="Secrets", value=", ".join(char.secrets), on_change=lambda e: control.update_selected_asset('secrets', [s.strip() for s in e.control.value.split(',')])),
                        ft.TextField(label="Allies", value=", ".join(char.allies), on_change=lambda e: control.update_selected_asset('allies', [s.strip() for s in e.control.value.split(',')])),
                        ft.TextField(label="Enemies", value=", ".join(char.enemies), on_change=lambda e: control.update_selected_asset('enemies', [s.strip() for s in e.control.value.split(',')])),
                        ft.TextField(label="Items", value=", ".join(char.items), on_change=lambda e: control.update_selected_asset('items', [s.strip() for s in e.control.value.split(',')])),
                        ft.TextField(label="Archetype", value=char.archetype, on_change=lambda e: control.update_selected_asset('archetype', e.control.value)),
                        ft.TextField(label="Values", value=", ".join(char.values), on_change=lambda e: control.update_selected_asset('values', [s.strip() for s in e.control.value.split(',')])),
                        ft.TextField(label="Flaws/Handicaps/Limitations", value=", ".join(char.flawsHandicapsLimitations), on_change=lambda e: control.update_selected_asset('flawsHandicapsLimitations', [s.strip() for s in e.control.value.split(',')])),
                        ft.TextField(label="Quirks", value=", ".join(char.quirks), on_change=lambda e: control.update_selected_asset('quirks', [s.strip() for s in e.control.value.split(',')])),
                        ft.TextField(label="Characteristics", value=", ".join(char.characteristics), on_change=lambda e: control.update_selected_asset('characteristics', [s.strip() for s in e.control.value.split(',')])),
                        ft.TextField(label="Vulnerabilities", value=", ".join(char.vulnerabilities), on_change=lambda e: control.update_selected_asset('vulnerabilities', [s.strip() for s in e.control.value.split(',')])),
                        ft.TextField(label="Voice Model", value=char.voiceModel, on_change=lambda e: control.update_selected_asset('voiceModel', e.control.value)),
                        ft.TextField(label="Dialogue Style", value=char.dialogueStyle, on_change=lambda e: control.update_selected_asset('dialogueStyle', e.control.value)),
                        ft.TextField(label="Expertise", value=", ".join(char.expertise), on_change=lambda e: control.update_selected_asset('expertise', [s.strip() for s in e.control.value.split(',')])),
                        ft.TextField(label="Portrayal Notes", value=char.portrayalNotes, on_change=lambda e: control.update_selected_asset('portrayalNotes', e.control.value)),
                    ])
                elif isinstance(control.selected_asset, schemas.Location):
                    loc = control.selected_asset
                    form_view.controls.extend([
                        ft.TextField(label="ID", value=loc.id, on_change=lambda e: control.update_selected_asset('id', e.control.value)),
                        ft.TextField(label="Name", value=loc.name, on_change=lambda e: control.update_selected_asset('name', e.control.value)),
                        ft.TextField(label="Description", value=loc.description, multiline=True, min_lines=3, on_change=lambda e: control.update_selected_asset('description', e.control.value)),
                        ft.TextField(label="Type", value=loc.type, on_change=lambda e: control.update_selected_asset('type', e.control.value)),
                        ft.TextField(label="District", value=loc.district, on_change=lambda e: control.update_selected_asset('district', e.control.value)),
                        ft.TextField(label="Owning Faction", value=loc.owningFaction, on_change=lambda e: control.update_selected_asset('owningFaction', e.control.value)),
                        ft.TextField(label="Danger Level", value=str(loc.dangerLevel), keyboard_type=ft.KeyboardType.NUMBER, on_change=lambda e: control.update_selected_asset('dangerLevel', e.control.value)),
                        ft.TextField(label="Population", value=str(loc.population), keyboard_type=ft.KeyboardType.NUMBER, on_change=lambda e: control.update_selected_asset('population', e.control.value)),
                        ft.TextField(label="Image", value=loc.image, on_change=lambda e: control.update_selected_asset('image', e.control.value)),
                        ft.TextField(label="Key Characters", value=", ".join(loc.keyCharacters), on_change=lambda e: control.update_selected_asset('keyCharacters', [s.strip() for s in e.control.value.split(',')])),
                        ft.TextField(label="Associated Items", value=", ".join(loc.associatedItems), on_change=lambda e: control.update_selected_asset('associatedItems', [s.strip() for s in e.control.value.split(',')])),
                        ft.Dropdown(
                            label="Accessibility",
                            options=[ft.dropdown.Option(a) for a in ["Public", "Semi-Private", "Private", "Restricted"]],
                            value=loc.accessibility,
                            on_change=lambda e: control.update_selected_asset('accessibility', e.control.value)
                        ),
                        ft.Checkbox(label="Hidden", value=loc.hidden, on_change=lambda e: control.update_selected_asset('hidden', e.control.value)),
                        ft.TextField(label="Internal Logic Notes", value=loc.internalLogicNotes, multiline=True, min_lines=2, on_change=lambda e: control.update_selected_asset('internalLogicNotes', e.control.value)),
                        elif isinstance(control.selected_asset, schemas.Sleuth):
                    sleuth = control.selected_asset
                    form_view.controls.extend([
                        ft.TextField(label="ID", value=sleuth.id, on_change=lambda e: control.update_selected_asset('id', e.control.value)),
                        ft.TextField(label="Name", value=sleuth.name, on_change=lambda e: control.update_selected_asset('name', e.control.value)),
                        ft.TextField(label="City", value=sleuth.city, on_change=lambda e: control.update_selected_asset('city', e.control.value)),
                        ft.TextField(label="Biography", value=sleuth.biography, multiline=True, min_lines=3, on_change=lambda e: control.update_selected_asset('biography', e.control.value)),
                        ft.Dropdown(
                            label="Wealth Class",
                            options=[ft.dropdown.Option(w) for w in schemas.WealthClass.__args__],
                            value=sleuth.wealthClass,
                            on_change=lambda e: control.update_selected_asset('wealthClass', e.control.value)
                        ),
                        ft.TextField(label="Archetype", value=sleuth.archetype, on_change=lambda e: control.update_selected_asset('archetype', e.control.value)),
                        ft.TextField(label="Personality", value=sleuth.personality, on_change=lambda e: control.update_selected_asset('personality', e.control.value)),
                        ft.Dropdown(
                            label="Alignment",
                            options=[ft.dropdown.Option(a) for a in schemas.Alignment.__args__],
                            value=sleuth.alignment,
                            on_change=lambda e: control.update_selected_asset('alignment', e.control.value)
                        ),
                        ft.TextField(label="Age", value=str(sleuth.age), keyboard_type=ft.KeyboardType.NUMBER, on_change=lambda e: control.update_selected_asset('age', e.control.value)),
                        ft.Dropdown(
                            label="Gender",
                            options=[ft.dropdown.Option(g) for g in schemas.Gender.__args__],
                            value=sleuth.gender,
                            on_change=lambda e: control.update_selected_asset('gender', e.control.value)
                        ),
                        ft.TextField(label="Employment", value=sleuth.employment, on_change=lambda e: control.update_selected_asset('employment', e.control.value)),
                        ft.TextField(label="Image", value=sleuth.image, on_change=lambda e: control.update_selected_asset('image', e.control.value)),
                        ft.TextField(label="District", value=sleuth.district, on_change=lambda e: control.update_selected_asset('district', e.control.value)),
                        ft.TextField(label="Relationships", value=", ".join(sleuth.relationships), on_change=lambda e: control.update_selected_asset('relationships', [s.strip() for s in e.control.value.split(',')])),
                        ft.TextField(label="Nemesis", value=sleuth.nemesis, on_change=lambda e: control.update_selected_asset('nemesis', e.control.value)),
                        ft.TextField(label="Values", value=", ".join(sleuth.values), on_change=lambda e: control.update_selected_asset('values', [s.strip() for s in e.control.value.split(',')])),
                        ft.TextField(label="Flaws/Handicaps/Limitations", value=", ".join(sleuth.flawsHandicapsLimitations), on_change=lambda e: control.update_selected_asset('flawsHandicapsLimitations', [s.strip() for s in e.control.value.split(',')])),
                        ft.TextField(label="Quirks", value=", ".join(sleuth.quirks), on_change=lambda e: control.update_selected_asset('quirks', [s.strip() for s in e.control.value.split(',')])),
                        ft.TextField(label="Primary Arc", value=sleuth.primaryArc, on_change=lambda e: control.update_selected_asset('primaryArc', e.control.value)),
                        ft.TextField(label="Characteristics", value=", ".join(sleuth.characteristics), on_change=lambda e: control.update_selected_asset('characteristics', [s.strip() for s in e.control.value.split(',')])),
                        ft.TextField(label="Motivations", value=", ".join(sleuth.motivations), on_change=lambda e: control.update_selected_asset('motivations', [s.strip() for s in e.control.value.split(',')])),
                        ft.TextField(label="Secrets", value=", ".join(sleuth.secrets), on_change=lambda e: control.update_selected_asset('secrets', [s.strip() for s in e.control.value.split(',')])),
                        ft.TextField(label="Vulnerabilities", value=", ".join(sleuth.vulnerabilities), on_change=lambda e: control.update_selected_asset('vulnerabilities', [s.strip() for s in e.control.value.split(',')])),
                        ft.TextField(label="Voice Model", value=sleuth.voiceModel, on_change=lambda e: control.update_selected_asset('voiceModel', e.control.value)),
                        ft.TextField(label="Dialogue Style", value=sleuth.dialogueStyle, on_change=lambda e: control.update_selected_asset('dialogueStyle', e.control.value)),
                        ft.TextField(label="Expertise", value=", ".join(sleuth.expertise), on_change=lambda e: control.update_selected_asset('expertise', [s.strip() for s in e.control.value.split(',')])),
                        ft.TextField(label="Portrayal Notes", value=sleuth.portrayalNotes, on_change=lambda e: control.update_selected_asset('portrayalNotes', e.control.value)),
                    ])

                form_view.controls.append(
                    ft.Row([
                        ft.ElevatedButton(text="New", on_click=handle_new_asset) if asset_name != "Sleuth" else ft.Container(),
                        ft.ElevatedButton(text="Save", on_click=lambda e: control.save_data()),
                    ])
                )
            page.update()

        # Initial form state
        if asset_list:
            control.select_asset(asset_list[0])
        update_form()


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
    
    # Initial view
    main_content.controls.append(build_world_builder(app_control))


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
