import flet as ft
from typing import Optional, Any
import data_manager
from schemas import WorldData, CaseData
import schemas

class Control:
    def __init__(self, page: ft.Page):
        self.page = page
        self.world_data: Optional[WorldData] = None
        self.case_data: Optional[CaseData] = None
        self.selected_asset: Optional[Any] = None
        self.load_initial_data()

    def load_initial_data(self):
        """
        Loads the initial case data. If not found, creates a new case.
        """
        try:
            self.world_data, self.case_data = data_manager.load_case("The Crimson Stain")
        except FileNotFoundError:
            data_manager.create_new_case("The Crimson Stain")
            self.world_data, self.case_data = data_manager.load_case("The Crimson Stain")

    def save_data(self):
        """
        Saves the current world and case data.
        """
        if self.world_data and self.case_data:
            data_manager.save_case("The Crimson Stain", self.world_data, self.case_data)
            self.page.snack_bar = ft.SnackBar(ft.Text("Case data saved successfully!"), open=True)
            self.page.update()

    def select_asset(self, asset: Any):
        """
        Sets the currently selected asset and updates the page.
        """
        self.selected_asset = asset
        self.page.update()

    def create_new_district(self):
        """
        Creates a new district with default values and adds it to the list.
        """
        import uuid
        new_district = schemas.District(
            id=f"district-{uuid.uuid4()}",
            name="New District",
            description="",
        )
        self.world_data.districts.append(new_district)
        self.select_asset(new_district)
        self.page.update()

    def create_new_faction(self):
        """
        Creates a new faction with default values and adds it to the list.
        """
        import uuid
        new_faction = schemas.Faction(
            id=f"faction-{uuid.uuid4()}",
            name="New Faction",
            description="",
        )
        self.world_data.factions.append(new_faction)
        self.select_asset(new_faction)
        self.page.update()

    def create_new_item(self):
        """
        Creates a new item with default values and adds it to the list.
        """
        import uuid
        new_item = schemas.Item(
            id=f"item-{uuid.uuid4()}",
            name="New Item",
            description="",
            possibleMeans=False,
            possibleMotive=False,
            possibleOpportunity=False,
            cluePotential="None",
            value="",
            condition="New",
        )
        self.world_data.items.append(new_item)
        self.select_asset(new_item)
        self.page.update()

    def create_new_location(self):
        """
        Creates a new location with default values and adds it to the list.
        """
        import uuid
        new_loc = schemas.Location(
            id=f"loc-{uuid.uuid4()}",
            name="New Location",
            description="",
        )
        self.world_data.locations.append(new_loc)
        self.select_asset(new_loc)
        self.page.update()

    def create_new_character(self):
        """
        Creates a new character with default values and adds it to the list.
        """
        import uuid
        new_char = schemas.Character(
            id=f"char-{uuid.uuid4()}",
            fullName="New Character",
            biography="",
            personality="",
            alignment="True Neutral",
            honesty=5,
            victimLikelihood=5,
            killerLikelihood=5,
        )
        self.world_data.characters.append(new_char)
        self.select_asset(new_char)
        # We need a way to tell the UI to refresh the list.
        # This will be handled in the next step.
        self.page.update()

    def update_clue(self, clue: schemas.Clue, attribute_name: str, new_value: Any):
        """
        Updates an attribute of a clue.
        """
        setattr(clue, attribute_name, new_value)
        self.page.update()

    def create_new_clue(self):
        """
        Creates a new, empty clue.
        """
        import uuid
        new_clue = schemas.Clue(
            clueId=f"clue-{uuid.uuid4()}",
            criticalClue=False,
            redHerring=False,
            isLie=False,
            source="",
            clueSummary="",
            knowledgeLevel="Sleuth Only",
        )
        self.case_data.clues.append(new_clue)
        self.select_asset(new_clue)
        self.page.update()

    def toggle_interview_question_is_clue(self, question: schemas.InterviewQuestion, is_clue: bool):
        """
        Toggles the isClue flag on an interview question and creates/removes a corresponding clue.
        """
        question.isClue = is_clue
        if is_clue:
            # Create a new clue if one doesn't already exist for this question
            if not any(c.source == question.questionId for c in self.case_data.clues):
                new_clue = schemas.Clue(
                    clueId=f"clue-{question.questionId}",
                    criticalClue=False,
                    redHerring=False,
                    isLie=False,
                    source=question.questionId,
                    clueSummary=f"From interview: {question.question}",
                    knowledgeLevel="Sleuth Only",
                )
                self.case_data.clues.append(new_clue)
        else:
            # Remove the clue if it exists
            self.case_data.clues = [c for c in self.case_data.clues if c.source != question.questionId]
        
        self.page.update()

    def add_interview_question(self, suspect: schemas.CaseSuspect):
        """
        Adds a new, empty interview question to a suspect.
        """
        import uuid
        new_question = schemas.InterviewQuestion(
            questionId=f"q-{uuid.uuid4()}",
            question="",
            answerId=f"a-{uuid.uuid4()}",
            answer="",
            isLie=False,
            isClue=False,
        )
        suspect.interview.append(new_question)
        self.page.update()

    def update_interview_question(self, question: schemas.InterviewQuestion, attribute_name: str, new_value: Any):
        """
        Updates an attribute of an interview question.
        """
        setattr(question, attribute_name, new_value)
        self.page.update()

    def update_case_meta(self, attribute_name: str, new_value: Any):
        """
        Updates an attribute of the caseMeta.
        """
        if not self.case_data.caseMeta:
            self.case_data.caseMeta = schemas.CaseMeta(
                victim="",
                culprit="",
                crimeScene="",
                murderWeapon="",
                coreMysterySolutionDetails=""
            )
        
        setattr(self.case_data.caseMeta, attribute_name, new_value)
        self.page.update()

    def delete_asset(self):
        """
        Deletes the currently selected asset.
        """
        if self.selected_asset:
            asset_type_map = {
                schemas.Character: self.world_data.characters,
                schemas.Location: self.world_data.locations,
                schemas.Item: self.world_data.items,
                schemas.Faction: self.world_data.factions,
                schemas.District: self.world_data.districts,
            }
            for asset_type, asset_list in asset_type_map.items():
                if isinstance(self.selected_asset, asset_type):
                    asset_list.remove(self.selected_asset)
                    self.selected_asset = None
                    self.page.update()
                    return

