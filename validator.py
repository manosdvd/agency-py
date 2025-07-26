import flet as ft
from my_control import Control
import schemas

def build_validator_view(control: Control):
    """
    Builds the UI for the Validator view.
    """

    results_column = ft.Column()

    def run_validation(e):
        results_column.controls.clear()
        errors, warnings = control.validate_case()

        def create_result_tile(result: schemas.ValidationResult):
            return ft.ListTile(
                title=ft.Text(result.message, color="red" if result.type == "error" else "orange"),
                trailing=ft.IconButton(
                    icon=ft.icons.ARROW_FORWARD,
                    on_click=lambda e: control.go_to_issue(result),
                    tooltip="Go to Issue",
                ) if result.asset_id else None,
            )

        # Display results
        if errors:
            results_column.controls.append(ft.Text("Errors:", style=ft.TextThemeStyle.HEADLINE_SMALL, color="red"))
            for error in errors:
                results_column.controls.append(create_result_tile(error))
        
        if warnings:
            results_column.controls.append(ft.Text("Warnings:", style=ft.TextThemeStyle.HEADLINE_SMALL, color="orange"))
            for warning in warnings:
                results_column.controls.append(create_result_tile(warning))

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
