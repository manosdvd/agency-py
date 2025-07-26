import flet as ft
from my_control import Control
import schemas

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


    suspects_section = ft.Column()

    def update_suspects_view():
        suspects_section.controls.clear()
        
        selected_suspect_id = None
        if control.selected_asset and isinstance(control.selected_asset, schemas.CaseSuspect):
            selected_suspect_id = control.selected_asset.characterId

        def on_suspect_select(e):
            for suspect in control.case_data.keySuspects:
                if suspect.characterId == e.control.value:
                    control.select_asset(suspect)
                    update_suspects_view()
                    return
            # If suspect not found, create a new one
            new_suspect = schemas.CaseSuspect(characterId=e.control.value, interview=[])
            control.case_data.keySuspects.append(new_suspect)
            control.select_asset(new_suspect)
            update_suspects_view()


        suspect_dropdown = ft.Dropdown(
            label="Select Suspect",
            options=[ft.dropdown.Option(char.id, char.fullName) for char in control.world_data.characters],
            value=selected_suspect_id,
            on_change=on_suspect_select
        )
        suspects_section.controls.append(suspect_dropdown)

        if control.selected_asset and isinstance(control.selected_asset, schemas.CaseSuspect):
            suspect = control.selected_asset
            suspects_section.controls.append(ft.Text(f"Editing Suspect: {suspect.characterId}"))
            
            interview_column = ft.Column()
            for i, interview_q in enumerate(suspect.interview):
                interview_column.controls.append(
                    ft.Column([
                        ft.TextField(label=f"Question {i+1}", value=interview_q.question, on_change=lambda e, q=interview_q: control.update_interview_question(q, 'question', e.control.value)),
                        ft.TextField(label=f"Answer {i+1}", value=interview_q.answer, on_change=lambda e, q=interview_q: control.update_interview_question(q, 'answer', e.control.value)),
                        ft.Checkbox(label="Is Lie?", value=interview_q.isLie, on_change=lambda e, q=interview_q: control.update_interview_question(q, 'isLie', e.control.value)),
                        ft.Divider(),
                    ])
                )
            
            suspects_section.controls.append(interview_column)
            suspects_section.controls.append(ft.ElevatedButton(text="Add Interview Question", on_click=lambda e: control.add_interview_question(suspect)))
    
    update_suspects_view()


    clues_section = ft.Column()

    def update_clues_view():
        clues_section.controls.clear()

        def on_clue_click(e):
            clue_id = e.control.data
            for c in control.case_data.clues:
                if c.clueId == clue_id:
                    control.select_asset(c)
                    update_clues_view()
                    break

        clue_list = ft.ListView(expand=1, spacing=5, padding=10)
        for clue in control.case_data.clues:
            clue_list.controls.append(
                ft.ListTile(
                    title=ft.Text(f"{clue.clueId}: {clue.clueSummary}"),
                    data=clue.clueId,
                    on_click=on_clue_click
                )
            )
        
        clues_section.controls.append(clue_list)
        clues_section.controls.append(ft.ElevatedButton(text="New Clue", on_click=lambda e: control.create_new_clue() and update_clues_view()))

        if control.selected_asset and isinstance(control.selected_asset, schemas.Clue):
            clue = control.selected_asset
            clue_form = ft.Column([
                ft.TextField(label="Clue ID", value=clue.clueId, on_change=lambda e: control.update_clue(clue, 'clueId', e.control.value)),
                ft.TextField(label="Summary", value=clue.clueSummary, on_change=lambda e: control.update_clue(clue, 'clueSummary', e.control.value)),
                ft.Checkbox(label="Critical Clue", value=clue.criticalClue, on_change=lambda e: control.update_clue(clue, 'criticalClue', e.control.value)),
                ft.Checkbox(label="Red Herring", value=clue.redHerring, on_change=lambda e: control.update_clue(clue, 'redHerring', e.control.value)),
                ft.Checkbox(label="Is Lie", value=clue.isLie, on_change=lambda e: control.update_clue(clue, 'isLie', e.control.value)),
                ft.TextField(label="Source", value=clue.source, on_change=lambda e: control.update_clue(clue, 'source', e.control.value)),
                ft.Dropdown(
                    label="Knowledge Level",
                    options=[ft.dropdown.Option(k) for k in ["Sleuth Only", "Reader Only", "Both", "Neither (Off-Page)"]],
                    value=clue.knowledgeLevel,
                    on_change=lambda e: control.update_clue(clue, 'knowledgeLevel', e.control.value)
                ),
                ft.TextField(label="Discovery Path", value=", ".join(clue.discoveryPath), on_change=lambda e: control.update_clue(clue, 'discoveryPath', [s.strip() for s in e.control.value.split(',')])),
                ft.TextField(label="Presentation Method", value=", ".join(clue.presentationMethod), on_change=lambda e: control.update_clue(clue, 'presentationMethod', [s.strip() for s in e.control.value.split(',')])),
                ft.TextField(label="Character Implicated", value=clue.characterImplicated, on_change=lambda e: control.update_clue(clue, 'characterImplicated', e.control.value)),
                ft.Dropdown(
                    label="Red Herring Type",
                    options=[ft.dropdown.Option(r) for r in ["Decoy Suspect", "Misleading Object", "False Alibi", "Misleading Dialogue"]],
                    value=clue.redHerringType,
                    on_change=lambda e: control.update_clue(clue, 'redHerringType', e.control.value)
                ),
                ft.TextField(label="Mechanism of Misdirection", value=clue.mechanismOfMisdirection, on_change=lambda e: control.update_clue(clue, 'mechanismOfMisdirection', e.control.value)),
                ft.TextField(label="Debunking Clue", value=clue.debunkingClue, on_change=lambda e: control.update_clue(clue, 'debunkingClue', e.control.value)),
                ft.TextField(label="Dependencies", value=", ".join(clue.dependencies), on_change=lambda e: control.update_clue(clue, 'dependencies', [s.strip() for s in e.control.value.split(',')])),
                ft.TextField(label="Required Actions for Discovery", value=", ".join(clue.requiredActionsForDiscovery), on_change=lambda e: control.update_clue(clue, 'requiredActionsForDiscovery', [s.strip() for s in e.control.value.split(',')])),
                ft.TextField(label="Associated Item", value=clue.associatedItem, on_change=lambda e: control.update_clue(clue, 'associatedItem', e.control.value)),
                ft.TextField(label="Associated Location", value=clue.associatedLocation, on_change=lambda e: control.update_clue(clue, 'associatedLocation', e.control.value)),
                ft.TextField(label="Associated Character", value=clue.associatedCharacter, on_change=lambda e: control.update_clue(clue, 'associatedCharacter', e.control.value)),
            ])
            clues_section.controls.append(clue_form)

    update_clues_view()

    return ft.Column(
        [
            ft.Text("Define the Crime", style=ft.TextThemeStyle.HEADLINE_MEDIUM),
            victim_dropdown,
            culprit_dropdown,
            crime_scene_dropdown,
            murder_weapon_dropdown,
            core_mystery_details,
            ft.Divider(),
            ft.Text("Manage Suspects", style=ft.TextThemeStyle.HEADLINE_MEDIUM),
            suspects_section,
            ft.Divider(),
            ft.Text("Manage Clues", style=ft.TextThemeStyle.HEADLINE_MEDIUM),
            clues_section,
            ft.ElevatedButton(text="Save Case", on_click=lambda e: control.save_data())
        ]
    )
