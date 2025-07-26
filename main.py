import flet as ft
from my_control import Control
import schemas
import case_builder
import validator
import social_graph
import map_tool
import faction_dynamics
import timeline
import plot_graph
import timeline_editor

def main(page: ft.Page):
    page.title = "The Agency"
    page.window_width = 1200
    page.window_height = 800
    page.theme = ft.Theme(color_scheme_seed="blue")
    page.dark_theme = ft.Theme(color_scheme_seed="blue")
    page.theme_mode = ft.ThemeMode.DARK

    def change_theme(e):
        page.theme_mode = "light" if page.theme_mode == "dark" else "dark"
        page.update()

    page.appbar = ft.AppBar(
        title=ft.Text("The Agency"),
        actions=[
            ft.IconButton(
                ft.icons.LIGHT_MODE,
                on_click=change_theme,
                tooltip="Toggle theme",
            ),
        ],
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

    search_bar = ft.TextField(
        label="Global Search",
        hint_text="Search characters, locations, items...",
        prefix_icon=ft.icons.SEARCH,
        on_change=lambda e: app_control.filter_assets(e.control.value),
        width=400,
    )

    # Create a single instance of the Control class
    app_control = Control(page, nav_rail, main_content, build_world_builder, case_builder.build_case_builder_view)

    def nav_changed(e):
        selected_index = e.control.selected_index
        main_content.controls.clear()

        if selected_index == 0:
            main_content.controls.append(build_world_builder(app_control))
        elif selected_index == 1:
            main_content.controls.append(case_builder.build_case_builder_view(app_control))
        elif selected_index == 2:
            main_content.controls.append(validator.build_validator_view(app_control))
        
        page.update()

    def build_world_builder(control: Control, asset_to_select_id: Optional[str] = None):
        
        character_view = create_asset_editor(control, "Characters", control.world_data.characters, asset_to_select_id)
        location_view = create_asset_editor(control, "Locations", control.world_data.locations, asset_to_select_id)
        item_view = create_asset_editor(control, "Items", control.world_data.items, asset_to_select_id)
        faction_view = create_asset_editor(control, "Factions", control.world_data.factions, asset_to_select_id)
        district_view = create_asset_editor(control, "Districts", control.world_data.districts, asset_to_select_id)
        sleuth_view = create_asset_editor(control, "Sleuth", [control.world_data.sleuth] if control.world_data.sleuth else [], asset_to_select_id)

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
                ft.Tab(text="Social Graph", content=social_graph.build_social_graph_view(control)),
                ft.Tab(text="Map Tool", content=map_tool.build_map_tool_view(control)),
                ft.Tab(text="Faction Dynamics", content=faction_dynamics.build_faction_dynamics_view(control)),
                ft.Tab(text="Timeline", content=timeline.build_timeline_view(control)),
            ],
            expand=1,
        )
        control.asset_tabs = asset_tabs

        return ft.Column([asset_tabs], expand=True)

    def _build_character_form(control: Control, char: schemas.Character):
        return [
        ft.Card(
            content=ft.Container(
                padding=10,
                content=ft.Column([
                    ft.Text("Basic Info", style=ft.TextThemeStyle.HEADLINE_SMALL),
                    ft.TextField(label="ID", value=char.id, on_change=lambda e: control.update_selected_asset('id', e.control.value), tooltip="Unique identifier for the character."),
                    ft.TextField(label="Full Name", value=char.fullName, on_change=lambda e: control.update_selected_asset('fullName', e.control.value), tooltip="The character's full name."),
                    ft.TextField(label="Alias", value=char.alias, on_change=lambda e: control.update_selected_asset('alias', e.control.value), tooltip="Any known aliases or nicknames."),
                    ft.TextField(label="Employment", value=char.employment, on_change=lambda e: control.update_selected_asset('employment', e.control.value), tooltip="The character's occupation or profession."),
                ])
            )
        ),
        ft.Card(
            content=ft.Container(
                padding=10,
                content=ft.Column([
                    ft.Text("Appearance", style=ft.TextThemeStyle.HEADLINE_SMALL),
                    ft.TextField(label="Age", value=str(char.age), keyboard_type=ft.KeyboardType.NUMBER, on_change=lambda e: control.update_selected_asset('age', e.control.value), tooltip="The character's age."),
                    ft.Dropdown(
                        label="Gender",
                        options=[ft.dropdown.Option(g) for g in schemas.Gender.__args__],
                        value=char.gender,
                        on_change=lambda e: control.update_selected_asset('gender', e.control.value), tooltip="The character's gender."),
                    ft.Row([
                        ft.TextField(label="Image", value=char.image, on_change=lambda e: control.update_selected_asset('image', e.control.value), expand=True, tooltip="URL or path to an image representing the character."),
                        ft.IconButton(icon=ft.icons.UPLOAD_FILE, on_click=lambda e: control.pick_image_file(char, "image")),
                    ]),
                    ft.Image(src=char.image, width=100, height=100) if char.image else ft.Container(),
                    ft.TextField(label="Characteristics", value=", ".join(char.characteristics), on_change=lambda e: control.update_selected_asset('characteristics', [s.strip() for s in e.control.value.split(',')]), tooltip="Comma-separated list of physical or behavioral characteristics."),
                ])
            )
        ),
        ft.Card(
            content=ft.Container(
                padding=10,
                content=ft.Column([
                    ft.Text("Personality", style=ft.TextThemeStyle.HEADLINE_SMALL),
                    ft.Row([
                        ft.TextField(label="Biography", value=char.biography, multiline=True, min_lines=3, on_change=lambda e: control.update_selected_asset('biography', e.control.value), expand=True, tooltip="A brief biography of the character."),
                        ft.IconButton(icon=ft.icons.STARS, on_click=lambda e: control.generate_with_ai(char, 'biography')),
                    ]),
                    ft.Row([
                        ft.TextField(label="Personality", value=char.personality, on_change=lambda e: control.update_selected_asset('personality', e.control.value), expand=True, tooltip="A description of the character's personality."),
                        ft.IconButton(icon=ft.icons.STARS, on_click=lambda e: control.generate_with_ai(char, 'personality')),
                    ]),
                    ft.Dropdown(
                        label="Alignment",
                        options=[ft.dropdown.Option(a) for a in schemas.Alignment.__args__],
                        value=char.alignment,
                        on_change=lambda e: control.update_selected_asset('alignment', e.control.value), tooltip="The character's moral and ethical alignment."),
                    ft.TextField(label="Archetype", value=char.archetype, on_change=lambda e: control.update_selected_asset('archetype', e.control.value), tooltip="The character's archetype (e.g., 'Hero', 'Villain', 'Sidekick')."),
                    ft.TextField(label="Values", value=", ".join(char.values), on_change=lambda e: control.update_selected_asset('values', [s.strip() for s in e.control.value.split(',')]), tooltip="Comma-separated list of the character's core values."),
                    ft.TextField(label="Quirks", value=", ".join(char.quirks), on_change=lambda e: control.update_selected_asset('quirks', [s.strip() for s in e.control.value.split(',')]), tooltip="Comma-separated list of the character's unique quirks or habits."),
                ])
            )
        ),
        ft.Card(
            content=ft.Container(
                padding=10,
                content=ft.Column([
                    ft.Text("Social", style=ft.TextThemeStyle.HEADLINE_SMALL),
                    ft.Row([
                        ft.TextField(label="Faction", value=char.faction, on_change=lambda e: control.update_selected_asset('faction', e.control.value), expand=True, tooltip="The faction the character belongs to."),
                        ft.IconButton(icon=ft.icons.LINK, on_click=lambda e: control.go_to_issue(schemas.ValidationResult(message="", type="", asset_id=char.faction, asset_type="Faction"))) if char.faction else ft.Container(),
                    ]),
                    ft.Dropdown(
                        label="Wealth Class",
                        options=[ft.dropdown.Option(w) for w in schemas.WealthClass.__args__],
                        value=char.wealthClass,
                        on_change=lambda e: control.update_selected_asset('wealthClass', e.control.value), tooltip="The character's wealth class."),
                    ft.Row([
                        ft.TextField(label="District", value=char.district, on_change=lambda e: control.update_selected_asset('district', e.control.value), expand=True, tooltip="The district the character primarily resides in."),
                        ft.IconButton(icon=ft.icons.LINK, on_click=lambda e: control.go_to_issue(schemas.ValidationResult(message="", type="", asset_id=char.district, asset_type="District"))) if char.district else ft.Container(),
                    ]),
                    ft.Row([
                        ft.TextField(label="Allies", value=", ".join(char.allies), on_change=lambda e: control.update_selected_asset('allies', [s.strip() for s in e.control.value.split(',')]), expand=True, tooltip="Comma-separated list of character IDs who are allies."),
                        ft.IconButton(icon=ft.icons.LINK, on_click=lambda e: control.go_to_issue(schemas.ValidationResult(message="", type="", asset_id=char.allies[0] if char.allies else None, asset_type="Character"))) if char.allies else ft.Container(),
                    ]),
                    ft.Row([
                        ft.TextField(label="Enemies", value=", ".join(char.enemies), on_change=lambda e: control.update_selected_asset('enemies', [s.strip() for s in e.control.value.split(',')]), expand=True, tooltip="Comma-separated list of character IDs who are enemies."),
                        ft.IconButton(icon=ft.icons.LINK, on_click=lambda e: control.go_to_issue(schemas.ValidationResult(message="", type="", asset_id=char.enemies[0] if char.enemies else None, asset_type="Character"))) if char.enemies else ft.Container(),
                    ]),
                ])
            )
        ),
        ft.Card(
            content=ft.Container(
                padding=10,
                content=ft.Column([
                    ft.Text("Author's Notes", style=ft.TextThemeStyle.HEADLINE_SMALL),
                    ft.TextField(label="Honesty", value=str(char.honesty), keyboard_type=ft.KeyboardType.NUMBER, on_change=lambda e: control.update_selected_asset('honesty', e.control.value), tooltip="Character's honesty level (1-10)."),
                    ft.TextField(label="Victim Likelihood", value=str(char.victimLikelihood), keyboard_type=ft.KeyboardType.NUMBER, on_change=lambda e: control.update_selected_asset('victimLikelihood', e.control.value), tooltip="Likelihood of the character being a victim (1-10)."),
                    ft.TextField(label="Killer Likelihood", value=str(char.killerLikelihood), keyboard_type=ft.KeyboardType.NUMBER, on_change=lambda e: control.update_selected_asset('killerLikelihood', e.control.value), tooltip="Likelihood of the character being the killer (1-10)."),
                    ft.TextField(label="Motivations", value=", ".join(char.motivations), on_change=lambda e: control.update_selected_asset('motivations', [s.strip() for s in e.control.value.split(',')]), tooltip="Comma-separated list of the character's motivations."),
                    ft.TextField(label="Secrets", value=", ".join(char.secrets), on_change=lambda e: control.update_selected_asset('secrets', [s.strip() for s in e.control.value.split(',')]), tooltip="Comma-separated list of the character's secrets."),
                    ft.Row([
                        ft.TextField(label="Items", value=", ".join(char.items), on_change=lambda e: control.update_selected_asset('items', [s.strip() for s in e.control.value.split(',')]), expand=True, tooltip="Comma-separated list of item IDs owned by the character."),
                        ft.IconButton(icon=ft.icons.LINK, on_click=lambda e: control.go_to_issue(schemas.ValidationResult(message="", type="", asset_id=char.items[0] if char.items else None, asset_type="Item"))) if char.items else ft.Container(),
                    ]),
                    ft.TextField(label="Flaws/Handicaps/Limitations", value=", ".join(char.flawsHandicapsLimitations), on_change=lambda e: control.update_selected_asset('flawsHandicapsLimitations', [s.strip() for s in e.control.value.split(',')]), tooltip="Comma-separated list of flaws, handicaps, or limitations."),
                    ft.TextField(label="Vulnerabilities", value=", ".join(char.vulnerabilities), on_change=lambda e: control.update_selected_asset('vulnerabilities', [s.strip() for s in e.control.value.split(',')]), tooltip="Comma-separated list of vulnerabilities."),
                    ft.TextField(label="Voice Model", value=char.voiceModel, on_change=lambda e: control.update_selected_asset('voiceModel', e.control.value), tooltip="Description of the character's voice."),
                    ft.TextField(label="Dialogue Style", value=char.dialogueStyle, on_change=lambda e: control.update_selected_asset('dialogueStyle', e.control.value), tooltip="Description of the character's dialogue style."),
                    ft.TextField(label="Expertise", value=", ".join(char.expertise), on_change=lambda e: control.update_selected_asset('expertise', [s.strip() for s in e.control.value.split(',')]), tooltip="Comma-separated list of areas of expertise."),
                    ft.TextField(label="Portrayal Notes", value=char.portrayalNotes, on_change=lambda e: control.update_selected_asset('portrayalNotes', e.control.value), tooltip="Notes for portraying the character."),
                ])
            )
        ),
    ]

def _build_location_form(control: Control, loc: schemas.Location):
    return [
        ft.Card(
            content=ft.Container(
                padding=10,
                content=ft.Column([
                    ft.Text("Basic Info", style=ft.TextThemeStyle.HEADLINE_SMALL),
                    ft.TextField(label="ID", value=loc.id, on_change=lambda e: control.update_selected_asset('id', e.control.value), tooltip="Unique identifier for the location."),
                    ft.TextField(label="Name", value=loc.name, on_change=lambda e: control.update_selected_asset('name', e.control.value), tooltip="The name of the location."),
                    ft.Row([
                        ft.TextField(label="Description", value=loc.description, multiline=True, min_lines=3, on_change=lambda e: control.update_selected_asset('description', e.control.value), expand=True, tooltip="A detailed description of the location."),
                        ft.IconButton(icon=ft.icons.STARS, on_click=lambda e: control.generate_with_ai(loc, 'description')),
                    ]),
                    ft.TextField(label="Type", value=loc.type, on_change=lambda e: control.update_selected_asset('type', e.control.value), tooltip="The type of location (e.g., 'Residence', 'Business', 'Public Space')."),
                    ft.Row([
                        ft.TextField(label="Image", value=loc.image, on_change=lambda e: control.update_selected_asset('image', e.control.value), expand=True, tooltip="URL or path to an image representing the location."),
                        ft.IconButton(icon=ft.icons.UPLOAD_FILE, on_click=lambda e: control.pick_image_file(loc, "image")),
                    ]),
                    ft.Image(src=loc.image, width=100, height=100) if loc.image else ft.Container(),
                ])
            )
        ),
        ft.Card(
            content=ft.Container(
                padding=10,
                content=ft.Column([
                    ft.Text("Social", style=ft.TextThemeStyle.HEADLINE_SMALL),
                    ft.Row([
                        ft.TextField(label="District", value=loc.district, on_change=lambda e: control.update_selected_asset('district', e.control.value), expand=True, tooltip="The district this location belongs to."),
                        ft.IconButton(icon=ft.icons.LINK, on_click=lambda e: control.go_to_issue(schemas.ValidationResult(message="", type="", asset_id=loc.district, asset_type="District"))) if loc.district else ft.Container(),
                    ]),
                    ft.Row([
                        ft.TextField(label="Owning Faction", value=loc.owningFaction, on_change=lambda e: control.update_selected_asset('owningFaction', e.control.value), expand=True, tooltip="The faction that owns or controls this location."),
                        ft.IconButton(icon=ft.icons.LINK, on_click=lambda e: control.go_to_issue(schemas.ValidationResult(message="", type="", asset_id=loc.owningFaction, asset_type="Faction"))) if loc.owningFaction else ft.Container(),
                    ]),
                    ft.Row([
                        ft.TextField(label="Key Characters", value=", ".join(loc.keyCharacters), on_change=lambda e: control.update_selected_asset('keyCharacters', [s.strip() for s in e.control.value.split(',')]), expand=True, tooltip="Comma-separated list of character IDs frequently found here."),
                        ft.IconButton(icon=ft.icons.LINK, on_click=lambda e: control.go_to_issue(schemas.ValidationResult(message="", type="", asset_id=loc.keyCharacters[0] if loc.keyCharacters else None, asset_type="Character"))) if loc.keyCharacters else ft.Container(),
                    ]),
                ])
            )
        ),
        ft.Card(
            content=ft.Container(
                padding=10,
                content=ft.Column([
                    ft.Text("Details", style=ft.TextThemeStyle.HEADLINE_SMALL),
                    ft.TextField(label="Danger Level", value=str(loc.dangerLevel), keyboard_type=ft.KeyboardType.NUMBER, on_change=lambda e: control.update_selected_asset('dangerLevel', e.control.value), tooltip="Level of danger associated with this location (1-5)."),
                    ft.TextField(label="Population", value=str(loc.population), keyboard_type=ft.KeyboardType.NUMBER, on_change=lambda e: control.update_selected_asset('population', e.control.value), tooltip="Approximate population or number of regular occupants."),
                    ft.Dropdown(
                        label="Accessibility",
                        options=[ft.dropdown.Option(a) for a in ["Public", "Semi-Private", "Private", "Restricted"]],
                        value=loc.accessibility,
                        on_change=lambda e: control.update_selected_asset('accessibility', e.control.value), tooltip="How accessible is this location to the public?"),
                    ft.Checkbox(label="Hidden", value=loc.hidden, on_change=lambda e: control.update_selected_asset('hidden', e.control.value), tooltip="Is this location hidden or secret?"),
                    ft.Row([
                        ft.TextField(label="Associated Items", value=", ".join(loc.associatedItems), on_change=lambda e: control.update_selected_asset('associatedItems', [s.strip() for s in e.control.value.split(',')]), expand=True, tooltip="Comma-separated list of item IDs typically found here."),
                        ft.IconButton(icon=ft.icons.LINK, on_click=lambda e: control.go_to_issue(schemas.ValidationResult(message="", type="", asset_id=loc.associatedItems[0] if loc.associatedItems else None, asset_type="Item"))) if loc.associatedItems else ft.Container(),
                    ]),
                    ft.Row([
                        ft.TextField(label="Clues", value=", ".join(loc.clues), on_change=lambda e: control.update_selected_asset('clues', [s.strip() for s in e.control.value.split(',')]), expand=True, tooltip="Comma-separated list of clue IDs found at this location."),
                        ft.IconButton(icon=ft.icons.LINK, on_click=lambda e: control.go_to_issue(schemas.ValidationResult(message="", type="", asset_id=loc.clues[0] if loc.clues else None, asset_type="Clue"))) if loc.clues else ft.Container(),
                    ]),
                    ft.Row([
                        ft.TextField(label="Internal Logic Notes", value=loc.internalLogicNotes, multiline=True, min_lines=2, on_change=lambda e: control.update_selected_asset('internalLogicNotes', e.control.value), expand=True, tooltip="Notes on the internal logic or mechanics related to this location."),
                        ft.IconButton(icon=ft.icons.STARS, on_click=lambda e: control.generate_with_ai(loc, 'internalLogicNotes')),
                    ]),
                ])
            )
        ),
    ]

def _build_item_form(control: Control, item: schemas.Item):
    return [
        ft.Card(
            content=ft.Container(
                padding=10,
                content=ft.Column([
                    ft.Text("Basic Info", style=ft.TextThemeStyle.HEADLINE_SMALL),
                    ft.TextField(label="ID", value=item.id, on_change=lambda e: control.update_selected_asset('id', e.control.value), tooltip="Unique identifier for the item."),
                    ft.TextField(label="Name", value=item.name, on_change=lambda e: control.update_selected_asset('name', e.control.value), tooltip="The name of the item."),
                    ft.Row([
                        ft.TextField(label="Description", value=item.description, multiline=True, min_lines=3, on_change=lambda e: control.update_selected_asset('description', e.control.value), expand=True, tooltip="A detailed description of the item."),
                        ft.IconButton(icon=ft.icons.STARS, on_click=lambda e: control.generate_with_ai(item, 'description')),
                    ]),
                    ft.TextField(label="Type", value=item.type, on_change=lambda e: control.update_selected_asset('type', e.control.value), tooltip="The type of item (e.g., 'Weapon', 'Tool', 'Document')."),
                    ft.Row([
                        ft.TextField(label="Image", value=item.image, on_change=lambda e: control.update_selected_asset('image', e.control.value), expand=True, tooltip="URL or path to an image representing the item."),
                        ft.IconButton(icon=ft.icons.UPLOAD_FILE, on_click=lambda e: control.pick_image_file(item, "image")),
                    ]),
                    ft.Image(src=item.image, width=100, height=100) if item.image else ft.Container(),
                ])
            )
        ),
        ft.Card(
            content=ft.Container(
                padding=10,
                content=ft.Column([
                    ft.Text("Clue Info", style=ft.TextThemeStyle.HEADLINE_SMALL),
                    ft.Checkbox(label="Possible Means", value=item.possibleMeans, on_change=lambda e: control.update_selected_asset('possibleMeans', e.control.value), tooltip="Can this item be used as a means to commit a crime?"),
                    ft.Checkbox(label="Possible Motive", value=item.possibleMotive, on_change=lambda e: control.update_selected_asset('possibleMotive', e.control.value), tooltip="Does this item suggest a motive for a crime?"),
                    ft.Checkbox(label="Possible Opportunity", value=item.possibleOpportunity, on_change=lambda e: control.update_selected_asset('possibleOpportunity', e.control.value), tooltip="Does this item provide an opportunity for a crime?"),
                    ft.Dropdown(
                        label="Clue Potential",
                        options=[ft.dropdown.Option(c) for c in ["None", "Low", "Medium", "High", "Critical"]],
                        value=item.cluePotential,
                        on_change=lambda e: control.update_selected_asset('cluePotential', e.control.value), tooltip="The significance of this item as a clue."),
                    ft.TextField(label="Significance", value=item.significance, multiline=True, min_lines=2, on_change=lambda e: control.update_selected_asset('significance', e.control.value), tooltip="Detailed explanation of the item's significance as a clue."),
                ])
            )
        ),
        ft.Card(
            content=ft.Container(
                padding=10,
                content=ft.Column([
                    ft.Text("Details", style=ft.TextThemeStyle.HEADLINE_SMALL),
                    ft.TextField(label="Value", value=item.value, on_change=lambda e: control.update_selected_asset('value', e.control.value), tooltip="The monetary or intrinsic value of the item."),
                    ft.Dropdown(
                        label="Condition",
                        options=[ft.dropdown.Option(c) for c in ["New", "Good", "Used", "Worn", "Damaged", "Broken"]],
                        value=item.condition,
                        on_change=lambda e: control.update_selected_asset('condition', e.control.value), tooltip="The physical condition of the item."),
                    ft.Row([
                        ft.TextField(label="Default Location", value=item.defaultLocation, on_change=lambda e: control.update_selected_asset('defaultLocation', e.control.value), expand=True, tooltip="The typical location where this item can be found."),
                        ft.IconButton(icon=ft.icons.LINK, on_click=lambda e: control.go_to_issue(schemas.ValidationResult(message="", type="", asset_id=item.defaultLocation, asset_type="Location"))) if item.defaultLocation else ft.Container(),
                    ]),
                    ft.Row([
                        ft.TextField(label="Default Owner", value=item.defaultOwner, on_change=lambda e: control.update_selected_asset('defaultOwner', e.control.value), expand=True, tooltip="The typical owner of this item."),
                        ft.IconButton(icon=ft.icons.LINK, on_click=lambda e: control.go_to_issue(schemas.ValidationResult(message="", type="", asset_id=item.defaultOwner, asset_type="Character"))) if item.defaultOwner else ft.Container(),
                    ]),
                    ft.TextField(label="Use", value=", ".join(item.use), on_change=lambda e: control.update_selected_asset('use', [s.strip() for s in e.control.value.split(',')]), tooltip="Comma-separated list of common uses for this item."),
                    ft.TextField(label="Unique Properties", value=", ".join(item.uniqueProperties), on_change=lambda e: control.update_selected_asset('uniqueProperties', [s.strip() for s in e.control.value.split(',')]), tooltip="Comma-separated list of unique characteristics or properties."),
                ])
            )
        ),
    ]

def _build_faction_form(control: Control, faction: schemas.Faction):
    return [
        ft.Card(
            content=ft.Container(
                padding=10,
                content=ft.Column([
                    ft.Text("Basic Info", style=ft.TextThemeStyle.HEADLINE_SMALL),
                    ft.TextField(label="ID", value=faction.id, on_change=lambda e: control.update_selected_asset('id', e.control.value), tooltip="Unique identifier for the faction."),
                    ft.TextField(label="Name", value=faction.name, on_change=lambda e: control.update_selected_asset('name', e.control.value), tooltip="The name of the faction."),
                    ft.Row([
                        ft.TextField(label="Description", value=faction.description, multiline=True, min_lines=3, on_change=lambda e: control.update_selected_asset('description', e.control.value), expand=True, tooltip="A detailed description of the faction."),
                        ft.IconButton(icon=ft.icons.STARS, on_click=lambda e: control.generate_with_ai(faction, 'description')),
                    ]),
                    ft.TextField(label="Archetype", value=faction.archetype, on_change=lambda e: control.update_selected_asset('archetype', e.control.value), tooltip="The archetype of the faction (e.g., 'Criminal Syndicate', 'Law Enforcement')."),
                    ft.Row([
                        ft.TextField(label="Image", value=faction.image, on_change=lambda e: control.update_selected_asset('image', e.control.value), expand=True, tooltip="URL or path to an image representing the faction."),
                        ft.IconButton(icon=ft.icons.UPLOAD_FILE, on_click=lambda e: control.pick_image_file(faction, "image")),
                    ]),
                    ft.Image(src=faction.image, width=100, height=100) if faction.image else ft.Container(),
                ])
            )
        ),
        ft.Card(
            content=ft.Container(
                padding=10,
                content=ft.Column([
                    ft.Text("Ideology & Influence", style=ft.TextThemeStyle.HEADLINE_SMALL),
                    ft.TextField(label="Ideology", value=faction.ideology, on_change=lambda e: control.update_selected_asset('ideology', e.control.value), tooltip="The core beliefs or principles of the faction."),
                    ft.Dropdown(
                        label="Influence",
                        options=[ft.dropdown.Option(i) for i in ["Local", "District-wide", "City-wide", "Regional", "Global"]],
                        value=faction.influence,
                        on_change=lambda e: control.update_selected_asset('influence', e.control.value), tooltip="The geographical reach of the faction's influence."),
                    ft.TextField(label="Public Perception", value=faction.publicPerception, on_change=lambda e: control.update_selected_asset('publicPerception', e.control.value), tooltip="How the public generally perceives this faction."),
                ])
            )
        ),
        ft.Card(
            content=ft.Container(
                padding=10,
                content=ft.Column([
                    ft.Text("Assets & Relationships", style=ft.TextThemeStyle.HEADLINE_SMALL),
                    ft.Row([
                        ft.TextField(label="Headquarters", value=faction.headquarters, on_change=lambda e: control.update_selected_asset('headquarters', e.control.value), expand=True, tooltip="The primary base of operations for the faction."),
                        ft.IconButton(icon=ft.icons.LINK, on_click=lambda e: control.go_to_issue(schemas.ValidationResult(message="", type="", asset_id=faction.headquarters, asset_type="Location"))) if faction.headquarters else ft.Container(),
                    ]),
                    ft.TextField(label="Resources", value=", ".join(faction.resources), on_change=lambda e: control.update_selected_asset('resources', [s.strip() for s in e.control.value.split(',')]), tooltip="Comma-separated list of resources controlled by the faction."),
                    ft.Row([
                        ft.TextField(label="Members", value=", ".join(faction.members), on_change=lambda e: control.update_selected_asset('members', [s.strip() for s in e.control.value.split(',')]), expand=True, tooltip="Comma-separated list of character IDs who are members of this faction."),
                        ft.IconButton(icon=ft.icons.LINK, on_click=lambda e: control.go_to_issue(schemas.ValidationResult(message="", type="", asset_id=faction.members[0] if faction.members else None, asset_type="Character"))) if faction.members else ft.Container(),
                    ]),
                    ft.Row([
                        ft.TextField(label="Ally Factions", value=", ".join(faction.allyFactions), on_change=lambda e: control.update_selected_asset('allyFactions', [s.strip() for s in e.control.value.split(',')]), expand=True, tooltip="Comma-separated list of faction IDs that are allies."),
                        ft.IconButton(icon=ft.icons.LINK, on_click=lambda e: control.go_to_issue(schemas.ValidationResult(message="", type="", asset_id=faction.allyFactions[0] if faction.allyFactions else None, asset_type="Faction"))) if faction.allyFactions else ft.Container(),
                    ]),
                    ft.Row([
                        ft.TextField(label="Enemy Factions", value=", ".join(faction.enemyFactions), on_change=lambda e: control.update_selected_asset('enemyFactions', [s.strip() for s in e.control.value.split(',')]), expand=True),
                        ft.IconButton(icon=ft.icons.LINK, on_click=lambda e: control.go_to_issue(schemas.ValidationResult(message="", type="", asset_id=faction.enemyFactions[0] if faction.enemyFactions else None, asset_type="Faction"))) if faction.enemyFactions else ft.Container(),
                    ]),
                ])
            )
        ),
    ]
    ]

def _build_district_form(control: Control, district: schemas.District):
    return [
        ft.Card(
            content=ft.Container(
                padding=10,
                content=ft.Column([
                    ft.Text("Basic Info", style=ft.TextThemeStyle.HEADLINE_SMALL),
                    ft.TextField(label="ID", value=district.id, on_change=lambda e: control.update_selected_asset('id', e.control.value), tooltip="Unique identifier for the district."),
                    ft.TextField(label="Name", value=district.name, on_change=lambda e: control.update_selected_asset('name', e.control.value), tooltip="The name of the district."),
                    ft.Row([
                        ft.TextField(label="Description", value=district.description, multiline=True, min_lines=3, on_change=lambda e: control.update_selected_asset('description', e.control.value), expand=True, tooltip="A detailed description of the district."),
                        ft.IconButton(icon=ft.icons.STARS, on_click=lambda e: control.generate_with_ai(district, 'description')),
                    ]),
                    ft.Row([
                        ft.TextField(label="Image", value=district.image, on_change=lambda e: control.update_selected_asset('image', e.control.value), expand=True, tooltip="URL or path to an image representing the district."),
                        ft.IconButton(icon=ft.icons.UPLOAD_FILE, on_click=lambda e: control.pick_image_file(district, "image")),
                    ]),
                    ft.Image(src=district.image, width=100, height=100) if district.image else ft.Container(),
                ])
            )
        ),
        ft.Card(
            content=ft.Container(
                padding=10,
                content=ft.Column([
                    ft.Text("Social & Demographics", style=ft.TextThemeStyle.HEADLINE_SMALL),
                    ft.Dropdown(
                        label="Wealth Class",
                        options=[ft.dropdown.Option(w) for w in schemas.WealthClass.__args__],
                        value=district.wealthClass,
                        on_change=lambda e: control.update_selected_asset('wealthClass', e.control.value), tooltip="The predominant wealth class in this district."),
                    ft.Dropdown(
                        label="Population Density",
                        options=[ft.dropdown.Option(p) for p in ["Sparse", "Moderate", "Dense", "Crowded"]],
                        value=district.populationDensity,
                        on_change=lambda e: control.update_selected_asset('populationDensity', e.control.value), tooltip="The population density of the district."),
                    ft.Row([
                        ft.TextField(label="Dominant Faction", value=district.dominantFaction, on_change=lambda e: control.update_selected_asset('dominantFaction', e.control.value), expand=True, tooltip="The faction with the most influence in this district."),
                        ft.IconButton(icon=ft.icons.LINK, on_click=lambda e: control.go_to_issue(schemas.ValidationResult(message="", type="", asset_id=district.dominantFaction, asset_type="Faction"))) if district.dominantFaction else ft.Container(),
                    ]),
                ])
            )
        ),
        ft.Card(
            content=ft.Container(
                padding=10,
                content=ft.Column([
                    ft.Text("Details", style=ft.TextThemeStyle.HEADLINE_SMALL),
                    ft.TextField(label="Atmosphere", value=district.atmosphere, on_change=lambda e: control.update_selected_asset('atmosphere', e.control.value), tooltip="The general mood or atmosphere of the district."),
                    ft.Row([
                        ft.TextField(label="Notable Features", value=", ".join(district.notableFeatures), on_change=lambda e: control.update_selected_asset('notableFeatures', [s.strip() for s in e.control.value.split(',')]), expand=True, tooltip="Comma-separated list of notable landmarks or features."),
                        ft.IconButton(icon=ft.icons.LINK, on_click=lambda e: control.go_to_issue(schemas.ValidationResult(message="", type="", asset_id=district.notableFeatures[0] if district.notableFeatures else None, asset_type="Location"))) if district.notableFeatures else ft.Container(),
                    ]),
                    ft.Row([
                        ft.TextField(label="Key Locations", value=", ".join(district.keyLocations), on_change=lambda e: control.update_selected_asset('keyLocations', [s.strip() for s in e.control.value.split(',')]), expand=True, tooltip="Comma-separated list of key location IDs within this district."),
                        ft.IconButton(icon=ft.icons.LINK, on_click=lambda e: control.go_to_issue(schemas.ValidationResult(message="", type="", asset_id=district.keyLocations[0] if district.keyLocations else None, asset_type="Location"))) if district.keyLocations else ft.Container(),
                    ]),
                ])
            )
        ),
    ]

def _build_sleuth_form(control: Control, sleuth: schemas.Sleuth):
    return [
        ft.Card(
            content=ft.Container(
                padding=10,
                content=ft.Column([
                    ft.Text("Basic Info", style=ft.TextThemeStyle.HEADLINE_SMALL),
                    ft.TextField(label="ID", value=sleuth.id, on_change=lambda e: control.update_selected_asset('id', e.control.value), tooltip="Unique identifier for the sleuth."),
                    ft.TextField(label="Name", value=sleuth.name, on_change=lambda e: control.update_selected_asset('name', e.control.value), tooltip="The sleuth's name."),
                    ft.TextField(label="City", value=sleuth.city, on_change=lambda e: control.update_selected_asset('city', e.control.value), tooltip="The city where the sleuth operates."),
                    ft.TextField(label="Employment", value=sleuth.employment, on_change=lambda e: control.update_selected_asset('employment', e.control.value), tooltip="The sleuth's occupation or agency."),
                ])
            )
        ),
        ft.Card(
            content=ft.Container(
                padding=10,
                content=ft.Column([
                    ft.Text("Appearance", style=ft.TextThemeStyle.HEADLINE_SMALL),
                    ft.TextField(label="Age", value=str(sleuth.age), keyboard_type=ft.KeyboardType.NUMBER, on_change=lambda e: control.update_selected_asset('age', e.control.value), tooltip="The sleuth's age."),
                    ft.Dropdown(
                        label="Gender",
                        options=[ft.dropdown.Option(g) for g in schemas.Gender.__args__],
                        value=sleuth.gender,
                        on_change=lambda e: control.update_selected_asset('gender', e.control.value), tooltip="The sleuth's gender."),
                    ft.Row([
                        ft.Row([
                        ft.TextField(label="Image", value=sleuth.image, on_change=lambda e: control.update_selected_asset('image', e.control.value), expand=True, tooltip="URL or path to an image representing the sleuth."),
                        ft.IconButton(icon=ft.icons.UPLOAD_FILE, on_click=lambda e: control.pick_image_file(sleuth, "image")),
                    ]),
                    ft.Image(src=sleuth.image, width=100, height=100) if sleuth.image else ft.Container(),
                        ft.IconButton(icon=ft.icons.UPLOAD_FILE, on_click=lambda e: control.pick_image_file(sleuth, "image")),
                    ]),
                    ft.Image(src=sleuth.image, width=100, height=100) if sleuth.image else ft.Container(),
                    ft.TextField(label="Characteristics", value=", ".join(sleuth.characteristics), on_change=lambda e: control.update_selected_asset('characteristics', [s.strip() for s in e.control.value.split(',')]), tooltip="Comma-separated list of physical or behavioral characteristics."),
                ])
            )
        ),
        ft.Card(
            content=ft.Container(
                padding=10,
                content=ft.Column([
                    ft.Text("Personality", style=ft.TextThemeStyle.HEADLINE_SMALL),
                    ft.Row([
                        ft.TextField(label="Biography", value=sleuth.biography, multiline=True, min_lines=3, on_change=lambda e: control.update_selected_asset('biography', e.control.value), expand=True, tooltip="A brief biography of the sleuth."),
                        ft.IconButton(icon=ft.icons.STARS, on_click=lambda e: control.generate_with_ai(sleuth, 'biography')),
                    ]),
                    ft.Row([
                        ft.TextField(label="Personality", value=sleuth.personality, on_change=lambda e: control.update_selected_asset('personality', e.control.value), expand=True, tooltip="A description of the sleuth's personality."),
                        ft.IconButton(icon=ft.icons.STARS, on_click=lambda e: control.generate_with_ai(sleuth, 'personality')),
                    ]),
                    ft.Dropdown(
                        label="Alignment",
                        options=[ft.dropdown.Option(a) for a in schemas.Alignment.__args__],
                        value=sleuth.alignment,
                        on_change=lambda e: control.update_selected_asset('alignment', e.control.value), tooltip="The sleuth's moral and ethical alignment."),
                    ft.TextField(label="Archetype", value=sleuth.archetype, on_change=lambda e: control.update_selected_asset('archetype', e.control.value), tooltip="The sleuth's archetype (e.g., 'Hardboiled', 'Amateur')."),
                    ft.TextField(label="Values", value=", ".join(sleuth.values), on_change=lambda e: control.update_selected_asset('values', [s.strip() for s in e.control.value.split(',')]), tooltip="Comma-separated list of the sleuth's core values."),
                    ft.TextField(label="Quirks", value=", ".join(sleuth.quirks), on_change=lambda e: control.update_selected_asset('quirks', [s.strip() for s in e.control.value.split(',')]), tooltip="Comma-separated list of the sleuth's unique quirks or habits."),
                ])
            )
        ),
        ft.Card(
            content=ft.Container(
                padding=10,
                content=ft.Column([
                    ft.Text("Social", style=ft.TextThemeStyle.HEADLINE_SMALL),
                    ft.Dropdown(
                        label="Wealth Class",
                        options=[ft.dropdown.Option(w) for w in schemas.WealthClass.__args__],
                        value=sleuth.wealthClass,
                        on_change=lambda e: control.update_selected_asset('wealthClass', e.control.value), tooltip="The sleuth's wealth class."),
                    ft.Row([
                        ft.TextField(label="District", value=sleuth.district, on_change=lambda e: control.update_selected_asset('district', e.control.value), expand=True, tooltip="The district the sleuth primarily operates in."),
                        ft.IconButton(icon=ft.icons.LINK, on_click=lambda e: control.go_to_issue(schemas.ValidationResult(message="", type="", asset_id=sleuth.district, asset_type="District"))) if sleuth.district else ft.Container(),
                    ]),
                    ft.TextField(label="Relationships", value=", ".join(sleuth.relationships), on_change=lambda e: control.update_selected_asset('relationships', [s.strip() for s in e.control.value.split(',')]), tooltip="Comma-separated list of key relationships."),
                    ft.Row([
                        ft.TextField(label="Nemesis", value=sleuth.nemesis, on_change=lambda e: control.update_selected_asset('nemesis', e.control.value), expand=True, tooltip="The sleuth's primary adversary."),
                        ft.IconButton(icon=ft.icons.LINK, on_click=lambda e: control.go_to_issue(schemas.ValidationResult(message="", type="", asset_id=sleuth.nemesis, asset_type="Character"))) if sleuth.nemesis else ft.Container(),
                    ]),
                ])
            )
        ),
        ft.Card(
            content=ft.Container(
                padding=10,
                content=ft.Column([
                    ft.Text("Author's Notes", style=ft.TextThemeStyle.HEADLINE_SMALL),
                    ft.TextField(label="Primary Arc", value=sleuth.primaryArc, on_change=lambda e: control.update_selected_asset('primaryArc', e.control.value), tooltip="The sleuth's main character arc."),
                    ft.TextField(label="Motivations", value=", ".join(sleuth.motivations), on_change=lambda e: control.update_selected_asset('motivations', [s.strip() for s in e.control.value.split(',')]), tooltip="Comma-separated list of the sleuth's motivations."),
                    ft.TextField(label="Secrets", value=", ".join(sleuth.secrets), on_change=lambda e: control.update_selected_asset('secrets', [s.strip() for s in e.control.value.split(',')]), tooltip="Comma-separated list of the sleuth's secrets."),
                    ft.TextField(label="Flaws/Handicaps/Limitations", value=", ".join(sleuth.flawsHandicapsLimitations), on_change=lambda e: control.update_selected_asset('flawsHandicapsLimitations', [s.strip() for s in e.control.value.split(',')]), tooltip="Comma-separated list of flaws, handicaps, or limitations."),
                    ft.TextField(label="Vulnerabilities", value=", ".join(sleuth.vulnerabilities), on_change=lambda e: control.update_selected_asset('vulnerabilities', [s.strip() for s in e.control.value.split(',')]), tooltip="Comma-separated list of vulnerabilities."),
                    ft.TextField(label="Voice Model", value=sleuth.voiceModel, on_change=lambda e: control.update_selected_asset('voiceModel', e.control.value), tooltip="Description of the sleuth's voice."),
                    ft.TextField(label="Dialogue Style", value=sleuth.dialogueStyle, on_change=lambda e: control.update_selected_asset('dialogueStyle', e.control.value), tooltip="Description of the sleuth's dialogue style."),
                    ft.TextField(label="Expertise", value=", ".join(sleuth.expertise), on_change=lambda e: control.update_selected_asset('expertise', [s.strip() for s in e.control.value.split(',')]), tooltip="Comma-separated list of areas of expertise."),
                    ft.TextField(label="Portrayal Notes", value=sleuth.portrayalNotes, on_change=lambda e: control.update_selected_asset('portrayalNotes', e.control.value), tooltip="Notes for portraying the sleuth."),
                ])
            )
        ),
    ]

def create_asset_editor(control: Control, asset_name: str, asset_list: list, asset_to_select_id: Optional[str] = None):
        
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
                filtered_assets = [
                    asset for asset in asset_list
                    if control.search_term in getattr(asset, 'fullName', getattr(asset, 'name', '')).lower()
                ]
                for asset in filtered_assets:
                    display_name = getattr(asset, 'fullName', getattr(asset, 'name', 'Unknown'))
                    
                    icon = ft.icons.PERSON
                    if isinstance(asset, schemas.Location):
                        icon = ft.icons.LOCATION_CITY
                    elif isinstance(asset, schemas.Item):
                        icon = ft.icons.TOY
                    elif isinstance(asset, schemas.Faction):
                        icon = ft.icons.GROUP
                    elif isinstance(asset, schemas.District):
                        icon = ft.icons.MAP
                    elif isinstance(asset, schemas.Sleuth):
                        icon = ft.icons.PERSON_SEARCH

                    asset_list_view.controls.append(
                        ft.ListTile(
                            title=ft.Text(display_name),
                            leading=ft.Icon(icon),
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

        def handle_delete_asset(e):
            def on_confirm(e):
                control.delete_asset()
                build_asset_list()
                update_form()
                dlg.open = False
                page.update()

            dlg = ft.AlertDialog(
                modal=True,
                title=ft.Text("Please confirm"),
                content=ft.Text("Do you really want to delete this asset?"),
                actions=[
                    ft.TextButton("Yes", on_click=on_confirm),
                    ft.TextButton("No", on_click=lambda e: setattr(dlg, 'open', False) or page.update()),
                ],
                actions_alignment=ft.MainAxisAlignment.END,
            )
            page.dialog = dlg
            dlg.open = True
            page.update()

        def update_form():
            form_view.controls.clear()
            if control.selected_asset:
                if isinstance(control.selected_asset, schemas.Character):
                    form_view.controls.extend(_build_character_form(control, control.selected_asset))
                elif isinstance(control.selected_asset, schemas.Location):
                    form_view.controls.extend(_build_location_form(control, control.selected_asset))
                elif isinstance(control.selected_asset, schemas.Item):
                    form_view.controls.extend(_build_item_form(control, control.selected_asset))
                elif isinstance(control.selected_asset, schemas.Faction):
                    form_view.controls.extend(_build_faction_form(control, control.selected_asset))
                elif isinstance(control.selected_asset, schemas.District):
                    form_view.controls.extend(_build_district_form(control, control.selected_asset))
                elif isinstance(control.selected_asset, schemas.Sleuth):
                    form_view.controls.extend(_build_sleuth_form(control, control.selected_asset))

                form_view.controls.append(
                    ft.Row([
                        ft.ElevatedButton(text="New", on_click=handle_new_asset) if asset_name != "Sleuth" else ft.Container(),
                        ft.ElevatedButton(text="Save", on_click=lambda e: control.save_data()),
                        ft.ElevatedButton(text="Delete", on_click=handle_delete_asset, color="white", bgcolor="red") if asset_name != "Sleuth" else ft.Container(),
                    ])
                )
            page.update()

        # Initial form state
        if asset_to_select_id:
            selected_asset_obj = next((asset for asset in asset_list if getattr(asset, 'id', getattr(asset, 'clueId', None)) == asset_to_select_id), None)
            if selected_asset_obj:
                control.select_asset(selected_asset_obj)
            else:
                control.select_asset(asset_list[0]) if asset_list else None
        elif asset_list:
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

    search_bar = ft.TextField(
        label="Global Search",
        hint_text="Search characters, locations, items...",
        prefix_icon=ft.icons.SEARCH,
        on_change=lambda e: app_control.filter_assets(e.control.value),
        width=400,
    )
    
    # Initial view
    main_content.controls.append(search_bar)
    main_content.controls.append(build_world_builder(app_control))


    page.add(
        ft.ResponsiveRow(
            [
                ft.Column([nav_rail], col={"sm": 2, "md": 1}),
                ft.VerticalDivider(width=1),
                ft.Column([main_content], col={"sm": 10, "md": 11}),
            ],
            expand=True,
        )
    )

if __name__ == "__main__":
    ft.app(target=main)

