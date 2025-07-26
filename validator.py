import flet as ft
from my_control import Control

def build_validator_view(control: Control):
    """
    Builds the UI for the Validator view.
    """

    results_column = ft.Column()

    def run_validation(e):
        results_column.controls.clear()
        
        # Orphaned Clues Check
        orphaned_clues = [clue for clue in control.case_data.clues if not clue.discoveryPath]
        if orphaned_clues:
            results_column.controls.append(ft.Text("Orphaned Clues:", style=ft.TextThemeStyle.HEADLINE_SMALL))
            for clue in orphaned_clues:
                results_column.controls.append(ft.Text(f"- {clue.clueId}: {clue.clueSummary}"))
        
        # Undebunkable Lies Check
        undebunkable_lies = []
        for suspect in control.case_data.keySuspects:
            for interview in suspect.interview:
                if interview.isLie and not interview.debunkingClue:
                    undebunkable_lies.append(interview)
        
        if undebunkable_lies:
            results_column.controls.append(ft.Text("Undebunkable Lies:", style=ft.TextThemeStyle.HEADLINE_SMALL))
            for lie in undebunkable_lies:
                results_column.controls.append(ft.Text(f"- {lie.question}"))

        if not orphaned_clues and not undebunkable_lies:
            results_column.controls.append(ft.Text("No validation errors found!", color="green"))

        results_column.update()


    return ft.Column(
        [
            ft.Text("Validator", style=ft.TextThemeStyle.HEADLINE_MEDIUM),
            ft.ElevatedButton(text="Run Validation", on_click=run_validation),
            results_column,
        ]
    )
