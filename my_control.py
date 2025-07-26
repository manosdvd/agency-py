import flet as ft
from typing import Optional, Any, Callable
import data_manager
from schemas import WorldData, CaseData
import schemas
import os
from transformers import pipeline, set_seed

class Control:
    def __init__(self, page: ft.Page, nav_rail: ft.NavigationRail, main_content: ft.Column, build_world_builder_func: Callable, build_case_builder_view_func: Callable, asset_tabs: Optional[ft.Tabs] = None, case_builder_tabs: Optional[ft.Tabs] = None):
        self.page = page
        self.nav_rail = nav_rail
        self.main_content = main_content
        self.build_world_builder_func = build_world_builder_func
        self.build_case_builder_view_func = build_case_builder_view_func
        self.asset_tabs = asset_tabs
        self.case_builder_tabs = case_builder_tabs
        self.selected_asset: Optional[Any] = None
        self.search_term: str = ""
        self.load_initial_data()

        self.file_picker = ft.FilePicker(on_result=self.on_file_picker_result)
        self.page.overlay.append(self.file_picker)
        self.page.update()

        self.current_image_asset = None
        self.current_image_field = None

        # Initialize AI text generation pipeline
        self.generator = pipeline('text-generation', model='gpt2')
        set_seed(42)

    def on_file_picker_result(self, e: ft.FilePickerResultEvent):
        if e.files:
            selected_file = e.files[0]
            # Copy the file to a local assets directory
            # For simplicity, let's assume a fixed assets directory for now
            assets_dir = "assets"
            os.makedirs(assets_dir, exist_ok=True)
            
            file_name = os.path.basename(selected_file.path)
            destination_path = os.path.join(assets_dir, file_name)
            
            import shutil
            shutil.copy(selected_file.path, destination_path)

            if self.current_image_asset and self.current_image_field:
                setattr(self.current_image_asset, self.current_image_field, destination_path)
                self.page.update()
                # Rebuild the view to reflect the image change
                if isinstance(self.current_image_asset, schemas.Character):
                    self.main_content.controls.clear()
                    self.main_content.controls.append(self.build_world_builder_func(self, self.current_image_asset.id))
                # Add similar logic for other asset types if needed
                self.page.update()

    def pick_image_file(self, asset: Any, field_name: str):
        self.current_image_asset = asset
        self.current_image_field = field_name
        self.file_picker.pick_files(allow_multiple=False, allowed_extensions=["png", "jpg", "jpeg", "gif", "webp"])

    def generate_with_ai(self, asset: Any, field_name: str):
        # Placeholder for AI generation logic
        print(f"AI generation requested for {type(asset).__name__}.{field_name}")
        
        prompt = f"Generate a {field_name} for a {type(asset).__name__} named {getattr(asset, 'fullName', getattr(asset, 'name', ''))}:\n"
        generated_text = self.generator(prompt, max_length=100, num_return_sequences=1)[0]['generated_text']
        
        # Extract only the generated part, removing the prompt
        generated_content = generated_text[len(prompt):].strip()

        setattr(asset, field_name, generated_content)
        self.page.update()
        self.world_data: Optional[WorldData] = None
        self.case_data: Optional[CaseData] = None
        self.selected_asset: Optional[Any] = None
        self.search_term: str = ""
        self.load_initial_data()

    def filter_assets(self, search_term: str):
        self.search_term = search_term.lower()
        self.page.update()

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

    def delete_case_suspect(self, suspect: schemas.CaseSuspect):
        """
        Deletes a case suspect.
        """
        if suspect in self.case_data.keySuspects:
            self.case_data.keySuspects.remove(suspect)
            self.selected_asset = None
            self.page.update()

    def delete_case_location(self, case_location: schemas.CaseLocation):
        """
        Deletes a case location.
        """
        if case_location in self.case_data.caseLocations:
            self.case_data.caseLocations.remove(case_location)
            self.selected_asset = None
            self.page.update()

    def delete_clue(self, clue: schemas.Clue):
        """
        Deletes a clue.
        """
        if clue in self.case_data.clues:
            self.case_data.clues.remove(clue)
            self.selected_asset = None
            self.page.update()

    def go_to_issue(self, result: schemas.ValidationResult):
        print(f"Navigating to: {result}")
        # Navigate to the correct main tab
        if result.asset_type in ["Character", "Location", "Item", "Faction", "District", "Sleuth"]:
            self.nav_rail.selected_index = 0  # World Builder
            self.main_content.controls.clear()
            self.main_content.controls.append(self.build_world_builder_func(self, result.asset_id))
            self.page.update()
            # Select the correct sub-tab and asset
            if self.asset_tabs:
                asset_type_to_tab_index = {
                    "Character": 0,
                    "Location": 1,
                    "Item": 2,
                    "Faction": 3,
                    "District": 4,
                    "Sleuth": 5,
                }
                tab_index = asset_type_to_tab_index.get(result.asset_type)
                if tab_index is not None:
                    self.asset_tabs.selected_index = tab_index
                    self.page.update()
                    # The asset selection within the list is handled by create_asset_editor now
        elif result.asset_type in ["CaseMeta", "CaseSuspect", "Clue", "CaseLocation", "InterviewQuestion", "CaseWitness"]:
            self.nav_rail.selected_index = 1  # Case Builder
            self.main_content.controls.clear()
            self.main_content.controls.append(self.build_case_builder_view_func(self, result.asset_id))
            self.page.update()
            # Select the correct sub-tab and asset
            if self.case_builder_tabs:
                asset_type_to_tab_index = {
                    "CaseMeta": 0,
                    "CaseSuspect": 1,
                    "Clue": 2,
                    "CaseLocation": 3,
                    "InterviewQuestion": 1, # Interview questions are part of suspects tab
                    "CaseWitness": 3, # Witnesses are part of case locations tab
                }
                tab_index = asset_type_to_tab_index.get(result.asset_type)
                if tab_index is not None:
                    self.case_builder_tabs.selected_index = tab_index
                    self.page.update()
                    # The asset selection within the list is handled by build_case_builder_view now
        self.page.update()

    def validate_case(self):
        errors: List[schemas.ValidationResult] = []
        warnings: List[schemas.ValidationResult] = []

        # Tier 1: Foundational Integrity (Errors)
        # 1.1 Unique IDs
        all_ids = set()
        for asset_list in [self.world_data.characters, self.world_data.locations, self.world_data.items, self.world_data.factions, self.world_data.districts, self.case_data.clues]:
            for asset in asset_list:
                if hasattr(asset, 'id') and asset.id:
                    if asset.id in all_ids:
                        errors.append(schemas.ValidationResult(
                            message=f"Duplicate ID: {asset.id} found in {type(asset).__name__}.",
                            type="error",
                            asset_id=asset.id,
                            asset_type=type(asset).__name__
                        ))
                    all_ids.add(asset.id)
                elif hasattr(asset, 'clueId') and asset.clueId:
                    if asset.clueId in all_ids:
                        errors.append(schemas.ValidationResult(
                            message=f"Duplicate ID: {asset.clueId} found in {type(asset).__name__}.",
                            type="error",
                            asset_id=asset.clueId,
                            asset_type=type(asset).__name__
                        ))
                    all_ids.add(asset.clueId)

        # 1.2 Valid ID References
        # Character references
        valid_char_ids = {c.id for c in self.world_data.characters}
        for loc in self.world_data.locations:
            for char_id in loc.keyCharacters:
                if char_id not in valid_char_ids:
                    errors.append(schemas.ValidationResult(
                        message=f"Invalid Reference: Location '{loc.name}' references non-existent character ID '{char_id}'.",
                        type="error",
                        asset_id=loc.id,
                        asset_type="Location",
                        field_name="keyCharacters"
                    ))
        for faction in self.world_data.factions:
            for member_id in faction.members:
                if member_id not in valid_char_ids:
                    errors.append(schemas.ValidationResult(
                        message=f"Invalid Reference: Faction '{faction.name}' references non-existent member ID '{member_id}'.",
                        type="error",
                        asset_id=faction.id,
                        asset_type="Faction",
                        field_name="members"
                    ))
        for char in self.world_data.characters:
            for ally_id in char.allies:
                if ally_id not in valid_char_ids:
                    errors.append(schemas.ValidationResult(
                        message=f"Invalid Reference: Character '{char.fullName}' references non-existent ally ID '{ally_id}'.",
                        type="error",
                        asset_id=char.id,
                        asset_type="Character",
                        field_name="allies"
                    ))
            for enemy_id in char.enemies:
                if enemy_id not in valid_char_ids:
                    errors.append(schemas.ValidationResult(
                        message=f"Invalid Reference: Character '{char.fullName}' references non-existent enemy ID '{enemy_id}'.",
                        type="error",
                        asset_id=char.id,
                        asset_type="Character",
                        field_name="enemies"
                    ))
            for item_id in char.items:
                if item_id not in {i.id for i in self.world_data.items}:
                    errors.append(schemas.ValidationResult(
                        message=f"Invalid Reference: Character '{char.fullName}' references non-existent item ID '{item_id}'.",
                        type="error",
                        asset_id=char.id,
                        asset_type="Character",
                        field_name="items"
                    ))
            if char.faction and char.faction not in {f.id for f in self.world_data.factions}:
                errors.append(schemas.ValidationResult(
                    message=f"Invalid Reference: Character '{char.fullName}' references non-existent faction ID '{char.faction}'.",
                    type="error",
                    asset_id=char.id,
                    asset_type="Character",
                    field_name="faction"
                ))
            if char.district and char.district not in {d.id for d in self.world_data.districts}:
                errors.append(schemas.ValidationResult(
                    message=f"Invalid Reference: Character '{char.fullName}' references non-existent district ID '{char.district}'.",
                    type="error",
                    asset_id=char.id,
                    asset_type="Character",
                    field_name="district"
                ))

        if self.world_data.sleuth:
            if self.world_data.sleuth.nemesis and self.world_data.sleuth.nemesis not in valid_char_ids:
                errors.append(schemas.ValidationResult(
                    message=f"Invalid Reference: Sleuth references non-existent nemesis ID '{self.world_data.sleuth.nemesis}'.",
                    type="error",
                    asset_id=self.world_data.sleuth.id,
                    asset_type="Sleuth",
                    field_name="nemesis"
                ))
            if self.world_data.sleuth.district and self.world_data.sleuth.district not in {d.id for d in self.world_data.districts}:
                errors.append(schemas.ValidationResult(
                    message=f"Invalid Reference: Sleuth references non-existent district ID '{self.world_data.sleuth.district}'.",
                    type="error",
                    asset_id=self.world_data.sleuth.id,
                    asset_type="Sleuth",
                    field_name="district"
                ))

        # Location references
        valid_loc_ids = {loc.id for loc in self.world_data.locations}
        for item in self.world_data.items:
            if item.defaultLocation and item.defaultLocation not in valid_loc_ids:
                errors.append(schemas.ValidationResult(
                    message=f"Invalid Reference: Item '{item.name}' references non-existent default location ID '{item.defaultLocation}'.",
                    type="error",
                    asset_id=item.id,
                    asset_type="Item",
                    field_name="defaultLocation"
                ))
        for faction in self.world_data.factions:
            if faction.headquarters and faction.headquarters not in valid_loc_ids:
                errors.append(schemas.ValidationResult(
                    message=f"Invalid Reference: Faction '{faction.name}' references non-existent headquarters ID '{faction.headquarters}'.",
                    type="error",
                    asset_id=faction.id,
                    asset_type="Faction",
                    field_name="headquarters"
                ))
        for district in self.world_data.districts:
            for loc_id in district.keyLocations:
                if loc_id not in valid_loc_ids:
                    errors.append(schemas.ValidationResult(
                        message=f"Invalid Reference: District '{district.name}' references non-existent key location ID '{loc_id}'.",
                        type="error",
                        asset_id=district.id,
                        asset_type="District",
                        field_name="keyLocations"
                    ))

        # Item references
        valid_item_ids = {item.id for item in self.world_data.items}
        for char in self.world_data.characters:
            for item_id in char.items:
                if item_id not in valid_item_ids:
                    errors.append(schemas.ValidationResult(
                        message=f"Invalid Reference: Character '{char.fullName}' references non-existent item ID '{item_id}'.",
                        type="error",
                        asset_id=char.id,
                        asset_type="Character",
                        field_name="items"
                    ))

        # Faction references
        valid_faction_ids = {f.id for f in self.world_data.factions}
        for loc in self.world_data.locations:
            if loc.owningFaction and loc.owningFaction not in valid_faction_ids:
                errors.append(schemas.ValidationResult(
                    message=f"Invalid Reference: Location '{loc.name}' references non-existent owning faction ID '{loc.owningFaction}'.",
                    type="error",
                    asset_id=loc.id,
                    asset_type="Location",
                    field_name="owningFaction"
                ))
        for char in self.world_data.characters:
            if char.faction and char.faction not in valid_faction_ids:
                errors.append(schemas.ValidationResult(
                    message=f"Invalid Reference: Character '{char.fullName}' references non-existent faction ID '{char.faction}'.",
                    type="error",
                    asset_id=char.id,
                    asset_type="Character",
                    field_name="faction"
                ))
        for district in self.world_data.districts:
            if district.dominantFaction and district.dominantFaction not in valid_faction_ids:
                errors.append(schemas.ValidationResult(
                    message=f"Invalid Reference: District '{district.name}' references non-existent dominant faction ID '{district.dominantFaction}'.",
                    type="error",
                    asset_id=district.id,
                    asset_type="District",
                    field_name="dominantFaction"
                ))
        for faction in self.world_data.factions:
            for ally_id in faction.allyFactions:
                if ally_id not in valid_faction_ids:
                    errors.append(schemas.ValidationResult(
                        message=f"Invalid Reference: Faction '{faction.name}' references non-existent ally faction ID '{ally_id}'.",
                        type="error",
                        asset_id=faction.id,
                        asset_type="Faction",
                        field_name="allyFactions"
                    ))
            for enemy_id in faction.enemyFactions:
                if enemy_id not in valid_faction_ids:
                    errors.append(schemas.ValidationResult(
                        message=f"Invalid Reference: Faction '{faction.name}' references non-existent enemy faction ID '{enemy_id}'.",
                        type="error",
                        asset_id=faction.id,
                        asset_type="Faction",
                        field_name="enemyFactions"
                    ))

        # District references
        valid_district_ids = {d.id for d in self.world_data.districts}
        for loc in self.world_data.locations:
            if loc.district and loc.district not in valid_district_ids:
                errors.append(schemas.ValidationResult(
                    message=f"Invalid Reference: Location '{loc.name}' references non-existent district ID '{loc.district}'.",
                    type="error",
                    asset_id=loc.id,
                    asset_type="Location",
                    field_name="district"
                ))
        for char in self.world_data.characters:
            if char.district and char.district not in valid_district_ids:
                errors.append(schemas.ValidationResult(
                    message=f"Invalid Reference: Character '{char.fullName}' references non-existent district ID '{char.district}'.",
                    type="error",
                    asset_id=char.id,
                    asset_type="Character",
                    field_name="district"
                ))
        if self.world_data.sleuth and self.world_data.sleuth.district and self.world_data.sleuth.district not in valid_district_ids:
            errors.append(schemas.ValidationResult(
                message=f"Invalid Reference: Sleuth references non-existent district ID '{self.world_data.sleuth.district}'.",
                type="error",
                asset_id=self.world_data.sleuth.id,
                asset_type="Sleuth",
                field_name="district"
            ))

        # Clue references
        valid_clue_ids = {c.clueId for c in self.case_data.clues}
        for clue in self.case_data.clues:
            for dep_id in clue.dependencies:
                if dep_id not in valid_clue_ids:
                    errors.append(schemas.ValidationResult(
                        message=f"Invalid Reference: Clue '{clue.clueSummary}' references non-existent dependency clue ID '{dep_id}'.",
                        type="error",
                        asset_id=clue.clueId,
                        asset_type="Clue",
                        field_name="dependencies"
                    ))
            if clue.debunkingClue and clue.debunkingClue not in valid_clue_ids:
                errors.append(schemas.ValidationResult(
                    message=f"Invalid Reference: Clue '{clue.clueSummary}' references non-existent debunking clue ID '{clue.debunkingClue}'.",
                    type="error",
                    asset_id=clue.clueId,
                    asset_type="Clue",
                    field_name="debunkingClue"
                ))
            if clue.associatedItem and clue.associatedItem not in valid_item_ids:
                errors.append(schemas.ValidationResult(
                    message=f"Invalid Reference: Clue '{clue.clueSummary}' references non-existent associated item ID '{clue.associatedItem}'.",
                    type="error",
                    asset_id=clue.clueId,
                    asset_type="Clue",
                    field_name="associatedItem"
                ))
            if clue.associatedLocation and clue.associatedLocation not in valid_loc_ids:
                errors.append(schemas.ValidationResult(
                    message=f"Invalid Reference: Clue '{clue.clueSummary}' references non-existent associated location ID '{clue.associatedLocation}'.",
                    type="error",
                    asset_id=clue.clueId,
                    asset_type="Clue",
                    field_name="associatedLocation"
                ))
            if clue.associatedCharacter and clue.associatedCharacter not in valid_char_ids:
                errors.append(schemas.ValidationResult(
                    message=f"Invalid Reference: Clue '{clue.clueSummary}' references non-existent associated character ID '{clue.associatedCharacter}'.",
                    type="error",
                    asset_id=clue.clueId,
                    asset_type="Clue",
                    field_name="associatedCharacter"
                ))
            for unlock in clue.revealsUnlocks:
                if unlock['type'] == 'location' and unlock['id'] not in valid_loc_ids:
                    errors.append(schemas.ValidationResult(
                        message=f"Invalid Reference: Clue '{clue.clueSummary}' unlocks non-existent location ID '{unlock['id']}'.",
                        type="error",
                        asset_id=clue.clueId,
                        asset_type="Clue",
                        field_name="revealsUnlocks"
                    ))
                # Interview question unlocks are harder to validate here without a flat list of all questions

        for suspect in self.case_data.keySuspects:
            if suspect.characterId not in valid_char_ids:
                errors.append(schemas.ValidationResult(
                    message=f"Invalid Reference: Case Suspect references non-existent character ID '{suspect.characterId}'.",
                    type="error",
                    asset_id=suspect.characterId,
                    asset_type="CaseSuspect",
                    field_name="characterId"
                ))
            for iq in suspect.interview:
                if iq.debunkingClue and iq.debunkingClue not in valid_clue_ids:
                    errors.append(schemas.ValidationResult(
                        message=f"Invalid Reference: Interview question '{iq.question}' references non-existent debunking clue ID '{iq.debunkingClue}'.",
                        type="error",
                        asset_id=suspect.characterId,
                        asset_type="InterviewQuestion",
                        field_name="debunkingClue"
                    ))
                if iq.hasItem and iq.hasItem not in valid_item_ids:
                    errors.append(schemas.ValidationResult(
                        message=f"Invalid Reference: Interview question '{iq.question}' references non-existent item ID '{iq.hasItem}'.",
                        type="error",
                        asset_id=suspect.characterId,
                        asset_type="InterviewQuestion",
                        field_name="hasItem"
                    ))

        for case_loc in self.case_data.caseLocations:
            if case_loc.locationId not in valid_loc_ids:
                errors.append(schemas.ValidationResult(
                    message=f"Invalid Reference: Case Location references non-existent location ID '{case_loc.locationId}'.",
                    type="error",
                    asset_id=case_loc.locationId,
                    asset_type="CaseLocation",
                    field_name="locationId"
                ))
            for clue_id in case_loc.locationClues:
                if clue_id not in valid_clue_ids:
                    errors.append(schemas.ValidationResult(
                        message=f"Invalid Reference: Case Location '{case_loc.locationId}' references non-existent clue ID '{clue_id}'.",
                        type="error",
                        asset_id=case_loc.locationId,
                        asset_type="CaseLocation",
                        field_name="locationClues"
                    ))
            for witness in case_loc.witnesses:
                if witness.characterId not in valid_char_ids:
                    errors.append(schemas.ValidationResult(
                        message=f"Invalid Reference: Case Location '{case_loc.locationId}' references non-existent witness character ID '{witness.characterId}'.",
                        type="error",
                        asset_id=case_loc.locationId,
                        asset_type="CaseWitness",
                        field_name="characterId"
                    ))
                for iq in witness.interview:
                    if iq.debunkingClue and iq.debunkingClue not in valid_clue_ids:
                        errors.append(schemas.ValidationResult(
                            message=f"Invalid Reference: Witness interview question '{iq.question}' references non-existent debunking clue ID '{iq.debunkingClue}'.",
                            type="error",
                            asset_id=witness.characterId,
                            asset_type="InterviewQuestion",
                            field_name="debunkingClue"
                        ))
                    if iq.hasItem and iq.hasItem not in valid_item_ids:
                        errors.append(schemas.ValidationResult(
                            message=f"Invalid Reference: Witness interview question '{iq.question}' references non-existent item ID '{iq.hasItem}'.",
                            type="error",
                            asset_id=witness.characterId,
                            asset_type="InterviewQuestion",
                            field_name="hasItem"
                        ))

        if self.case_data.caseMeta:
            meta = self.case_data.caseMeta
            if meta.victim and meta.victim not in valid_char_ids:
                errors.append(schemas.ValidationResult(
                    message=f"Invalid Reference: Case Meta victim references non-existent character ID '{meta.victim}'.",
                    type="error",
                    asset_id="caseMeta",
                    asset_type="CaseMeta",
                    field_name="victim"
                ))
            if meta.culprit and meta.culprit not in valid_char_ids:
                errors.append(schemas.ValidationResult(
                    message=f"Invalid Reference: Case Meta culprit references non-existent character ID '{meta.culprit}'.",
                    type="error",
                    asset_id="caseMeta",
                    asset_type="CaseMeta",
                    field_name="culprit"
                ))
            if meta.crimeScene and meta.crimeScene not in valid_loc_ids:
                errors.append(schemas.ValidationResult(
                    message=f"Invalid Reference: Case Meta crime scene references non-existent location ID '{meta.crimeScene}'.",
                    type="error",
                    asset_id="caseMeta",
                    asset_type="CaseMeta",
                    field_name="crimeScene"
                ))
            if meta.murderWeapon and meta.murderWeapon not in valid_item_ids:
                errors.append(schemas.ValidationResult(
                    message=f"Invalid Reference: Case Meta murder weapon references non-existent item ID '{meta.murderWeapon}'.",
                    type="error",
                    asset_id="caseMeta",
                    asset_type="CaseMeta",
                    field_name="murderWeapon"
                ))
            if meta.meansClue and meta.meansClue not in valid_clue_ids:
                errors.append(schemas.ValidationResult(
                    message=f"Invalid Reference: Case Meta means clue references non-existent clue ID '{meta.meansClue}'.",
                    type="error",
                    asset_id="caseMeta",
                    asset_type="CaseMeta",
                    field_name="meansClue"
                ))
            if meta.motiveClue and meta.motiveClue not in valid_clue_ids:
                errors.append(schemas.ValidationResult(
                    message=f"Invalid Reference: Case Meta motive clue references non-existent clue ID '{meta.motiveClue}'.",
                    type="error",
                    asset_id="caseMeta",
                    asset_type="CaseMeta",
                    field_name="motiveClue"
                ))
            if meta.opportunityClue and meta.opportunityClue not in valid_clue_ids:
                errors.append(schemas.ValidationResult(
                    message=f"Invalid Reference: Case Meta opportunity clue references non-existent clue ID '{meta.opportunityClue}'.",
                    type="error",
                    asset_id="caseMeta",
                    asset_type="CaseMeta",
                    field_name="opportunityClue"
                ))
            for rh_clue_id in meta.redHerringClues:
                if rh_clue_id not in valid_clue_ids:
                    errors.append(schemas.ValidationResult(
                        message=f"Invalid Reference: Case Meta red herring clue references non-existent clue ID '{rh_clue_id}'.",
                        type="error",
                        asset_id="caseMeta",
                        asset_type="CaseMeta",
                        field_name="redHerringClues"
                    ))

        # Tier 2: Logical Consistency (Errors)
        # 2.1 Orphaned Clues Check (existing)
        for clue in self.case_data.clues:
            if not clue.discoveryPath and not any(clue.clueId == interview.debunkingClue for suspect in self.case_data.keySuspects for interview in suspect.interview if interview.debunkingClue):
                is_unlocked = any(unlock.get("id") == clue.clueId for c in self.case_data.clues for unlock in c.revealsUnlocks)
                if not is_unlocked:
                    errors.append(schemas.ValidationResult(
                        message=f"Orphaned Clue: '{clue.clueSummary}' has no discovery path, is not used to debunk a lie, and is not unlocked by another clue.",
                        type="error",
                        asset_id=clue.clueId,
                        asset_type="Clue",
                        field_name="discoveryPath"
                    ))

        # 2.2 Undebunkable Lies Check (existing)
        for suspect in self.case_data.keySuspects:
            for interview in suspect.interview:
                if interview.isLie and not interview.debunkingClue:
                    errors.append(schemas.ValidationResult(
                        message=f"Undebunkable Lie: '{interview.question}' by {suspect.characterId} is a lie but has no debunking clue.",
                        type="error",
                        asset_id=suspect.characterId,
                        asset_type="InterviewQuestion",
                        field_name="debunkingClue"
                    ))

        # 2.3 Circular Logic in Clue Dependencies
        for clue in self.case_data.clues:
            path = set()
            stack = [clue.clueId]
            while stack:
                current_clue_id = stack.pop()
                if current_clue_id in path:
                    errors.append(schemas.ValidationResult(
                        message=f"Circular Dependency: Clue '{clue.clueSummary}' has a circular dependency involving '{current_clue_id}'.",
                        type="error",
                        asset_id=clue.clueId,
                        asset_type="Clue",
                        field_name="dependencies"
                    ))
                    break
                path.add(current_clue_id)
                current_clue = next((c for c in self.case_data.clues if c.clueId == current_clue_id), None)
                if current_clue:
                    for dep_id in current_clue.dependencies:
                        stack.append(dep_id)

        # Tier 3: Playability & Narrative Craft (Warnings)
        # 3.1 Narrative Dead-End Detection (existing)
        for location in self.case_data.caseLocations:
            if not location.locationClues and not location.witnesses:
                warnings.append(schemas.ValidationResult(
                    message=f"Potential Dead End: Location '{location.locationId}' has no clues or witnesses associated with it.",
                    type="warning",
                    asset_id=location.locationId,
                    asset_type="CaseLocation"
                ))
        
        for suspect in self.case_data.keySuspects:
            if not suspect.interview:
                warnings.append(schemas.ValidationResult(
                    message=f"Potential Dead End: Suspect '{suspect.characterId}' has no interview questions.",
                    type="warning",
                    asset_id=suspect.characterId,
                    asset_type="CaseSuspect"
                ))
            elif not any(iq.isClue or iq.isLie for iq in suspect.interview):
                warnings.append(schemas.ValidationResult(
                    message=f"Potential Dead End: Interview with '{suspect.characterId}' yields no clues or lies.",
                    type="warning",
                    asset_id=suspect.characterId,
                    asset_type="CaseSuspect"
                ))

        # 3.2 Core Mystery Logic Check (existing)
        meta = self.case_data.caseMeta
        if not meta:
            errors.append(schemas.ValidationResult(
                message="Core Mystery Not Defined: CaseMeta is missing.",
                type="error",
                asset_type="CaseMeta"
            ))
        else:
            if not meta.meansClue: warnings.append(schemas.ValidationResult(
                message="Core Mystery: The 'Means' clue is not defined.",
                type="warning",
                asset_type="CaseMeta",
                field_name="meansClue"
            ))
            if not meta.motiveClue: warnings.append(schemas.ValidationResult(
                message="Core Mystery: The 'Motive' clue is not defined.",
                type="warning",
                asset_type="CaseMeta",
                field_name="motiveClue"
            ))
            if not meta.opportunityClue: warnings.append(schemas.ValidationResult(
                message="Core Mystery: The 'Opportunity' clue is not defined.",
                type="warning",
                asset_type="CaseMeta",
                field_name="opportunityClue"
            ))
            
            # Weapon Accessibility
            culprit = next((c for c in self.world_data.characters if c.id == meta.culprit), None)
            weapon = next((i for i in self.world_data.items if i.id == meta.murderWeapon), None)
            if culprit and weapon:
                weapon_loc = next((l for l in self.world_data.locations if l.id == weapon.defaultLocation), None)
                if weapon_loc and culprit.id not in weapon_loc.keyCharacters:
                     warnings.append(schemas.ValidationResult(
                        message=f"Weapon Accessibility: Culprit '{culprit.fullName}' may not have access to the weapon '{weapon.name}' at its default location.",
                        type="warning",
                        asset_id=culprit.id,
                        asset_type="Character",
                        field_name="items"
                     ))

            # Crime Scene Accessibility
            if culprit:
                scene = next((l for l in self.world_data.locations if l.id == meta.crimeScene), None)
                if scene and culprit.id not in scene.keyCharacters:
                    warnings.append(schemas.ValidationResult(
                        message=f"Crime Scene Accessibility: Culprit '{culprit.fullName}' may not have access to the crime scene '{scene.name}'.",
                        type="warning",
                        asset_id=culprit.id,
                        asset_type="Character",
                        field_name="district"
                    ))


        # 3.3 Red Herring Validation (existing)
        for clue in self.case_data.clues:
            if clue.redHerring and not clue.debunkingClue:
                errors.append(schemas.ValidationResult(
                    message=f"Unsolvable Red Herring: The red herring clue '{clue.clueSummary}' has no debunking clue.",
                    type="error",
                    asset_id=clue.clueId,
                    asset_type="Clue",
                    field_name="debunkingClue"
                ))

        # 3.4 Plausible Suspects
        if self.case_data.caseMeta and self.case_data.caseMeta.victim:
            victim_id = self.case_data.caseMeta.victim
            for suspect in self.case_data.keySuspects:
                suspect_char = next((c for c in self.world_data.characters if c.id == suspect.characterId), None)
                if suspect_char:
                    # Check if suspect has any direct relationship with victim or crime scene
                    has_connection = False
                    if victim_id in suspect_char.allies or victim_id in suspect_char.enemies:
                        has_connection = True
                    # Check if suspect is at crime scene or has item related to crime
                    if self.case_data.caseMeta.crimeScene and suspect_char.district == next((loc.district for loc in self.world_data.locations if loc.id == self.case_data.caseMeta.crimeScene), None):
                        has_connection = True
                    if self.case_data.caseMeta.murderWeapon and self.case_data.caseMeta.murderWeapon in suspect_char.items:
                        has_connection = True

                    if not has_connection:
                        warnings.append(schemas.ValidationResult(
                            message=f"Plausibility Warning: Suspect '{suspect_char.fullName}' has no clear connection to the victim or crime scene.",
                            type="warning",
                            asset_id=suspect_char.id,
                            asset_type="Character"
                        ))

        # 3.5 Red Herring Sufficiency
        red_herrings = [clue for clue in self.case_data.clues if clue.redHerring]
        if len(red_herrings) < 2:
            warnings.append(schemas.ValidationResult(
                message="Red Herring Sufficiency: Consider adding more red herrings to increase complexity.",
                type="warning",
                asset_type="Clue"
            ))
        
        # Check if all red herrings have a debunking clue
        for rh in red_herrings:
            if not rh.debunkingClue:
                errors.append(schemas.ValidationResult(
                    message=f"Red Herring Sufficiency: Red herring '{rh.clueSummary}' does not have a debunking clue.",
                    type="error",
                    asset_id=rh.clueId,
                    asset_type="Clue",
                    field_name="debunkingClue"
                ))

        # Tier 4: Player Experience & Cognition (Warnings)
        # 4.1 Cognitive Overload
        num_clues = len(self.case_data.clues)
        num_suspects = len(self.case_data.keySuspects)

        if num_clues > 15: # Arbitrary threshold
            warnings.append(schemas.ValidationResult(
                message=f"Cognitive Overload: Consider reducing the number of clues ({num_clues}) for better player experience.",
                type="warning",
                asset_type="CaseData",
                field_name="clues"
            ))
        if num_suspects > 5: # Arbitrary threshold
            warnings.append(schemas.ValidationResult(
                message=f"Cognitive Overload: Consider reducing the number of suspects ({num_suspects}) for better player experience.",
                type="warning",
                asset_type="CaseData",
                field_name="keySuspects"
            ))

        # 4.2 Potential for "Aha!" Moments (Placeholder)
        # This is a complex check that would require analyzing clue dependencies and logical flow.
        # For now, it's a placeholder.
        if num_clues > 0 and num_suspects > 0 and not errors:
            warnings.append(schemas.ValidationResult(
                message="Aha! Moments: Ensure there are clear paths for players to connect clues and reach 'Aha!' moments.",
                type="warning",
                asset_type="CaseData"
            ))

        return errors, warnings

