import flet as ft
from my_control import Control

def build_validator_view(control: Control):
    """
    Builds the UI for the Validator view.
    """

    results_column = ft.Column()

    def run_validation(e):
        results_column.controls.clear()
        errors = []
        warnings = []

        # 1. Orphaned Clues Check
        for clue in control.case_data.clues:
            if not clue.discoveryPath and not any(clue.clueId in interview.debunkingClue for suspect in control.case_data.keySuspects for interview in suspect.interview if interview.debunkingClue):
                # Check if it's revealed by another clue
                is_unlocked = any(unlock.get("id") == clue.clueId for c in control.case_data.clues for unlock in c.revealsUnlocks)
                if not is_unlocked:
                    errors.append(f"Orphaned Clue: '{clue.clueSummary}' has no discovery path and is not used to debunk a lie or unlocked by another clue.")

        # 2. Undebunkable Lies Check
        for suspect in control.case_data.keySuspects:
            for interview in suspect.interview:
                if interview.isLie and not interview.debunkingClue:
                    errors.append(f"Undebunkable Lie: '{interview.question}' by {suspect.characterId} is a lie but has no debunking clue.")

        # 3. Narrative Dead-End Detection
        for location in control.case_data.caseLocations:
            if not location.locationClues and not location.witnesses:
                warnings.append(f"Potential Dead End: Location '{location.locationId}' has no clues or witnesses associated with it.")
        
        for suspect in control.case_data.keySuspects:
            if not suspect.interview:
                warnings.append(f"Potential Dead End: Suspect '{suspect.characterId}' has no interview questions.")
            elif not any(iq.isClue or iq.isLie for iq in suspect.interview):
                warnings.append(f"Potential Dead End: Interview with '{suspect.characterId}' yields no clues or lies.")

        # 4. Core Mystery Logic Check
        meta = control.case_data.caseMeta
        if not meta:
            errors.append("Core Mystery Not Defined: CaseMeta is missing.")
        else:
            if not meta.meansClue: warnings.append("Core Mystery: The 'Means' clue is not defined.")
            if not meta.motiveClue: warnings.append("Core Mystery: The 'Motive' clue is not defined.")
            if not meta.opportunityClue: warnings.append("Core Mystery: The 'Opportunity' clue is not defined.")
            
            # Weapon Accessibility
            culprit = next((c for c in control.world_data.characters if c.id == meta.culprit), None)
            weapon = next((i for i in control.world_data.items if i.id == meta.murderWeapon), None)
            if culprit and weapon:
                weapon_loc = next((l for l in control.world_data.locations if l.id == weapon.defaultLocation), None)
                if weapon_loc and culprit.id not in weapon_loc.keyCharacters:
                     warnings.append(f"Weapon Accessibility: Culprit '{culprit.fullName}' may not have access to the weapon '{weapon.name}' at its default location.")

            # Crime Scene Accessibility
            if culprit:
                scene = next((l for l in control.world_data.locations if l.id == meta.crimeScene), None)
                if scene and culprit.id not in scene.keyCharacters:
                    warnings.append(f"Crime Scene Accessibility: Culprit '{culprit.fullName}' may not have access to the crime scene '{scene.name}'.")


        # 5. Red Herring Validation
        for clue in control.case_data.clues:
            if clue.redHerring and not clue.debunkingClue:
                errors.append(f"Unsolvable Red Herring: The red herring clue '{clue.clueSummary}' has no debunking clue.")


        # Display results
        if errors:
            results_column.controls.append(ft.Text("Errors:", style=ft.TextThemeStyle.HEADLINE_SMALL, color="red"))
            for error in errors:
                results_column.controls.append(ft.Text(f"- {error}"))
        
        if warnings:
            results_column.controls.append(ft.Text("Warnings:", style=ft.TextThemeStyle.HEADLINE_SMALL, color="orange"))
            for warning in warnings:
                results_column.controls.append(ft.Text(f"- {warning}"))

        if not errors and not warnings:
            results_column.controls.append(ft.Text("No validation issues found!", color="green"))

        results_column.update()


    return ft.Column(
        [
            ft.Text("Validator", style=ft.TextThemeStyle.HEADLINE_MEDIUM),
            ft.ElevatedButton(text="Run Validation", on_click=run_validation),
            results_column,
        ]
    )
