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
                
                debunking_clue_dropdown = ft.Dropdown(
                    label="Debunking Clue",
                    options=[ft.dropdown.Option(c.clueId, c.clueSummary) for c in control.case_data.clues],
                    value=interview_q.debunkingClue,
                    on_change=lambda e, q=interview_q: control.update_interview_question(q, 'debunkingClue', e.control.value),
                    disabled=not interview_q.isLie
                )

                is_lie_checkbox = ft.Checkbox(
                    label="Is Lie?", 
                    value=interview_q.isLie, 
                    on_change=lambda e, q=interview_q, d=debunking_clue_dropdown: (
                        control.update_interview_question(q, 'isLie', e.control.value),
                        setattr(d, 'disabled', not e.control.value),
                        control.page.update()
                    )
                )

                interview_column.controls.append(
                    ft.Column([
                        ft.TextField(label=f"Question {i+1}", value=interview_q.question, on_change=lambda e, q=interview_q: control.update_interview_question(q, 'question', e.control.value)),
                        ft.TextField(label=f"Answer {i+1}", value=interview_q.answer, on_change=lambda e, q=interview_q: control.update_interview_question(q, 'answer', e.control.value)),
                        is_lie_checkbox,
                        debunking_clue_dropdown,
                        ft.Checkbox(label="Is Clue?", value=interview_q.isClue, on_change=lambda e, q=interview_q: control.toggle_interview_question_is_clue(q, e.control.value)),
                        ft.Divider(),
                    ])
                )
            
            suspects_section.controls.append(interview_column)
            suspects_section.controls.append(ft.ElevatedButton(text="Add Interview Question", on_click=lambda e: control.add_interview_question(suspect)))
    
    update_suspects_view()


    clues_section = ft.Column()

    def open_unlocks_dialog(clue: schemas.Clue):
        
        unlock_type = ft.Dropdown(
            label="Unlock Type",
            options=[
                ft.dropdown.Option("location", "Location"),
                ft.dropdown.Option("interview_question", "Interview Question"),
            ],
            on_change=lambda e: update_unlock_options(e.control.value)
        )
        unlock_target = ft.Dropdown(label="Target")
        
        def update_unlock_options(type: str):
            unlock_target.options.clear()
            if type == "location":
                unlock_target.options.extend([ft.dropdown.Option(loc.id, loc.name) for loc in control.world_data.locations])
            elif type == "interview_question":
                for suspect in control.case_data.keySuspects:
                    for iq in suspect.interview:
                        unlock_target.options.append(ft.dropdown.Option(iq.questionId, f"{suspect.characterId}: {iq.question}"))
            unlock_target.update()

        def add_unlock(e):
            clue.revealsUnlocks.append({"type": unlock_type.value, "id": unlock_target.value})
            dialog.open = False
            control.page.update()

        dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Add Unlock"),
            content=ft.Column([
                unlock_type,
                unlock_target,
            ]),
            actions=[
                ft.TextButton("Add", on_click=add_unlock),
                ft.TextButton("Cancel", on_click=lambda e: setattr(dialog, 'open', False) or control.page.update()),
            ]
        )
        control.page.dialog = dialog
        dialog.open = True
        control.page.update()

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
                ft.Dropdown(
                    label="Dependencies",
                    options=[ft.dropdown.Option(c.clueId, c.clueSummary) for c in control.case_data.clues],
                    value=clue.dependencies,
                    multi_select=True,
                    on_change=lambda e: control.update_clue(clue, 'dependencies', e.control.value)
                ),
                ft.TextField(label="Required Actions for Discovery", value=", ".join(clue.requiredActionsForDiscovery), on_change=lambda e: control.update_clue(clue, 'requiredActionsForDiscovery', [s.strip() for s in e.control.value.split(',')])),
                ft.TextField(label="Associated Item", value=clue.associatedItem, on_change=lambda e: control.update_clue(clue, 'associatedItem', e.control.value)),
                ft.TextField(label="Associated Location", value=clue.associatedLocation, on_change=lambda e: control.update_clue(clue, 'associatedLocation', e.control.value)),
                ft.TextField(label="Associated Character", value=clue.associatedCharacter, on_change=lambda e: control.update_clue(clue, 'associatedCharacter', e.control.value)),
                ft.ElevatedButton(text="Manage Unlocks", on_click=lambda e: open_unlocks_dialog(clue)),
            ])
            clues_section.controls.append(clue_form)

    update_clues_view()

    case_locations_section = ft.Column()

    def update_case_locations_view():
        case_locations_section.controls.clear()

        def on_location_select(e):
            # Find or create the CaseLocation
            case_loc = next((cl for cl in control.case_data.caseLocations if cl.locationId == e.control.value), None)
            if not case_loc:
                case_loc = schemas.CaseLocation(locationId=e.control.value, locationClues=[], witnesses=[])
                control.case_data.caseLocations.append(case_loc)
            control.select_asset(case_loc)
            update_case_locations_view()

        location_dropdown = ft.Dropdown(
            label="Select Location",
            options=[ft.dropdown.Option(loc.id, loc.name) for loc in control.world_data.locations],
            value=control.selected_asset.locationId if isinstance(control.selected_asset, schemas.CaseLocation) else None,
            on_change=on_location_select
        )
        case_locations_section.controls.append(location_dropdown)

        if isinstance(control.selected_asset, schemas.CaseLocation):
            case_loc = control.selected_asset
            
            clues_checklist = ft.Column([ft.Text("Clues at this Location", style=ft.TextThemeStyle.HEADLINE_SMALL)])
            for clue in control.case_data.clues:
                def on_clue_check_change(e, c=clue, cloc=case_loc):
                    if e.control.value:
                        cloc.locationClues.append(c.clueId)
                    else:
                        cloc.locationClues.remove(c.clueId)
                clues_checklist.controls.append(ft.Checkbox(label=clue.clueSummary, value=clue.clueId in case_loc.locationClues, on_change=on_clue_check_change))
            
            witnesses_checklist = ft.Column([ft.Text("Witnesses at this Location", style=ft.TextThemeStyle.HEADLINE_SMALL)])
            non_suspects = [char for char in control.world_data.characters if char.id not in [s.characterId for s in control.case_data.keySuspects]]
            for witness in non_suspects:
                def on_witness_check_change(e, w=witness, cloc=case_loc):
                    if e.control.value:
                        cloc.witnesses.append(schemas.CaseWitness(characterId=w.id, interview=[]))
                    else:
                        cloc.witnesses = [wit for wit in cloc.witnesses if wit.characterId != w.id]
                witnesses_checklist.controls.append(ft.Checkbox(label=witness.fullName, value=any(w.characterId == witness.id for w in case_loc.witnesses), on_change=on_witness_check_change))

            case_locations_section.controls.extend([clues_checklist, witnesses_checklist])

    update_case_locations_view()

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
            ft.Text("Manage Case Locations", style=ft.TextThemeStyle.HEADLINE_MEDIUM),
            case_locations_section,
            ft.Divider(),
            ft.Text("Manage Clues", style=ft.TextThemeStyle.HEADLINE_MEDIUM),
            clues_section,
            ft.ElevatedButton(text="Save Case", on_click=lambda e: control.save_data())
        ]
    )
