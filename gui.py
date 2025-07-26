import customtkinter
from typing import List, Tuple
from schemas import CaseData, CaseMeta, CaseSuspect, CaseLocation, Clue, WorldData, Character, Location, Item
import case_manager # Import your case manager logic

# Set the appearance mode and default color theme
customtkinter.set_appearance_mode("Dark")
customtkinter.set_default_color_theme("blue")

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # --- Data Loading ---
        self.world_data: WorldData = None
        self.case_data: CaseData = None
        self.load_initial_data()


        # --- Window Setup ---
        self.title("The Agency")
        self.geometry("1200x800")

        # --- Main Layout ---
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # --- Main Tab View (for World Builder vs. Case Builder) ---
        self.tab_view = customtkinter.CTkTabview(self, width=250)
        self.tab_view.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

        self.tab_view.add("World Builder")
        self.tab_view.add("Case Builder")
        
        self.tab_view.set("World Builder")

        # --- Configure World Builder Tab ---
        self.create_world_builder_tab()

        # --- Configure Case Builder Tab ---
        self.create_case_builder_tab()


    def load_initial_data(self):
        """Loads data from the default case file."""
        try:
            self.world_data, self.case_data = case_manager.load_case("The Crimson Stain")
        except FileNotFoundError:
            print("Default case 'The Crimson Stain' not found. Please create it first.")
            self.world_data = WorldData()
            self.case_data = CaseData(caseMeta=CaseMeta(victim="", culprit="", crimeScene="", murderWeapon="", coreMysterySolutionDetails=""))

    def create_world_builder_tab(self):
        """Creates the UI for the World Builder section."""
        world_tab = self.tab_view.tab("World Builder")
        world_tab.grid_columnconfigure(0, weight=1)
        
        wb_tab_view = customtkinter.CTkTabview(world_tab, width=250)
        wb_tab_view.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        # Add tabs for each asset type in WorldData
        wb_tab_view.add("Characters")
        wb_tab_view.add("Locations")
        wb_tab_view.add("Items")
        wb_tab_view.add("Factions")
        wb_tab_view.add("Districts")
        wb_tab_view.add("Sleuth")

        # Populate each world builder tab
        self.create_asset_editor_tab(wb_tab_view.tab("Characters"), "Characters", self.world_data.characters, self.populate_character_form)
        self.create_asset_editor_tab(wb_tab_view.tab("Locations"), "Locations", self.world_data.locations, self.populate_location_form)
        self.create_asset_editor_tab(wb_tab_view.tab("Items"), "Items", self.world_data.items, self.populate_item_form)
        # ... placeholders for other tabs
        label_factions = customtkinter.CTkLabel(wb_tab_view.tab("Factions"), text="Factions editor will go here.")
        label_factions.pack(padx=20, pady=20)
        label_districts = customtkinter.CTkLabel(wb_tab_view.tab("Districts"), text="Districts editor will go here.")
        label_districts.pack(padx=20, pady=20)
        label_sleuth = customtkinter.CTkLabel(wb_tab_view.tab("Sleuth"), text="Sleuth editor will go here.")
        label_sleuth.pack(padx=20, pady=20)


    def create_asset_editor_tab(self, tab, asset_name, asset_list, form_populate_func):
        """Generic function to create a two-pane asset editor (list on left, form on right)."""
        tab.grid_columnconfigure(0, weight=1)
        tab.grid_columnconfigure(1, weight=3)
        tab.grid_rowconfigure(0, weight=1)

        # --- Left Frame for the list ---
        left_frame = customtkinter.CTkFrame(tab, width=250)
        left_frame.grid(row=0, column=0, padx=(10, 5), pady=10, sticky="nsew")
        left_frame.grid_rowconfigure(1, weight=1)

        label = customtkinter.CTkLabel(left_frame, text=f"{asset_name} List", font=customtkinter.CTkFont(size=16, weight="bold"))
        label.grid(row=0, column=0, padx=10, pady=10)
        
        # --- Listbox ---
        listbox = customtkinter.CTkTextbox(left_frame, width=200)
        listbox.grid(row=1, column=0, padx=10, pady=(0, 10), sticky="nsew")
        
        # Populate listbox and create a mapping from name to asset object
        asset_map = {getattr(asset, 'fullName', getattr(asset, 'name', 'Unknown')): asset for asset in asset_list}
        for name in asset_map.keys():
            listbox.insert("end", f"{name}\n")
        
        # --- Right Frame for the form ---
        right_frame = customtkinter.CTkScrollableFrame(tab, label_text=f"Edit {asset_name[:-1]}")
        right_frame.grid(row=0, column=1, padx=(5, 10), pady=10, sticky="nsew")
        right_frame.grid_columnconfigure(1, weight=1)

        # --- Bottom Frame for buttons ---
        bottom_frame = customtkinter.CTkFrame(tab)
        bottom_frame.grid(row=1, column=0, columnspan=2, padx=10, pady=(0, 10), sticky="ew")

        add_button = customtkinter.CTkButton(bottom_frame, text=f"Add New {asset_name[:-1]}")
        add_button.pack(side="left", padx=10, pady=5)
        
        save_button = customtkinter.CTkButton(bottom_frame, text=f"Save {asset_name}")
        save_button.pack(side="right", padx=10, pady=5)

        # --- Bind selection event ---
        def on_select(event):
            # The listbox doesn't have a direct selection method, so we get the current line
            selected_line = listbox.get("insert linestart", "insert lineend")
            selected_asset = asset_map.get(selected_line)
            if selected_asset:
                # Clear previous form and populate with new data
                for widget in right_frame.winfo_children():
                    widget.destroy()
                form_populate_func(right_frame, selected_asset)

        listbox.bind("<ButtonRelease-1>", on_select)

    def populate_character_form(self, parent, character: Character):
        """Populates the form with details of the selected character."""
        self.create_form_row(parent, 0, "Full Name", customtkinter.CTkEntry, {'placeholder_text': character.fullName})
        self.create_form_row(parent, 1, "Biography", customtkinter.CTkTextbox, {'height': 100}).insert("1.0", character.biography)
        self.create_form_row(parent, 2, "Personality", customtkinter.CTkEntry, {'placeholder_text': character.personality})
        # ... and so on for all other character fields.

    def populate_location_form(self, parent, location: Location):
        """Populates the form with details of the selected location."""
        self.create_form_row(parent, 0, "Name", customtkinter.CTkEntry, {'placeholder_text': location.name})
        self.create_form_row(parent, 1, "Description", customtkinter.CTkTextbox, {'height': 100}).insert("1.0", location.description)
        # ... etc.

    def populate_item_form(self, parent, item: Item):
        """Populates the form with details of the selected item."""
        self.create_form_row(parent, 0, "Name", customtkinter.CTkEntry, {'placeholder_text': item.name})
        self.create_form_row(parent, 1, "Description", customtkinter.CTkTextbox, {'height': 100}).insert("1.0", item.description)
        # ... etc.

    def create_case_builder_tab(self):
        """Creates the UI for the Case Builder section."""
        case_builder_frame = self.tab_view.tab("Case Builder")
        case_builder_frame.grid_columnconfigure(0, weight=1)
        
        case_tab_view = customtkinter.CTkTabview(case_builder_frame, width=250)
        case_tab_view.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        case_tab_view.add("Case Details")
        case_tab_view.add("Key Suspects")
        case_tab_view.add("Case Locations")
        case_tab_view.add("Clues")

        self.create_case_details_tab(case_tab_view.tab("Case Details"))
        # ... placeholders for other tabs
        label_suspects = customtkinter.CTkLabel(case_tab_view.tab("Key Suspects"), text="Key Suspects editor will go here.")
        label_suspects.pack(padx=20, pady=20)
        label_locations = customtkinter.CTkLabel(case_tab_view.tab("Case Locations"), text="Case Locations editor will go here.")
        label_locations.pack(padx=20, pady=20)
        label_clues = customtkinter.CTkLabel(case_tab_view.tab("Clues"), text="Clues editor will go here.")
        label_clues.pack(padx=20, pady=20)


    def create_form_row(self, parent, y_pos, label_text, widget_type, widget_options=None):
        """Helper function to create a label and a widget in a grid."""
        if widget_options is None:
            widget_options = {}
            
        label = customtkinter.CTkLabel(parent, text=label_text, anchor="w")
        label.grid(row=y_pos, column=0, padx=20, pady=(10, 0), sticky="w")
        
        widget = widget_type(parent, **widget_options)
        widget.grid(row=y_pos, column=1, padx=20, pady=(10, 0), sticky="ew")
        return widget

    def create_case_details_tab(self, tab):
        """Creates the UI for the CaseMeta schema."""
        tab.grid_columnconfigure(1, weight=1)

        scrollable_frame = customtkinter.CTkScrollableFrame(tab, label_text="Core Case Details")
        scrollable_frame.grid(row=0, column=0, columnspan=2, padx=20, pady=20, sticky="nsew")
        scrollable_frame.grid_columnconfigure(1, weight=1)

        character_names = [char.fullName for char in self.world_data.characters]
        location_names = [loc.name for loc in self.world_data.locations]
        item_names = [item.name for item in self.world_data.items]
        
        current_meta = self.case_data.caseMeta if self.case_data.caseMeta else CaseMeta("", "", "", "", "")

        row = 0
        self.victim_menu = self.create_form_row(scrollable_frame, row, "Victim", customtkinter.CTkOptionMenu, {'values': character_names})
        self.victim_menu.set(next((c.fullName for c in self.world_data.characters if c.id == current_meta.victim), "Select Victim"))
        
        row += 1
        self.culprit_menu = self.create_form_row(scrollable_frame, row, "Culprit", customtkinter.CTkOptionMenu, {'values': character_names})
        self.culprit_menu.set(next((c.fullName for c in self.world_data.characters if c.id == current_meta.culprit), "Select Culprit"))

        row += 1
        self.crimescene_menu = self.create_form_row(scrollable_frame, row, "Crime Scene", customtkinter.CTkOptionMenu, {'values': location_names})
        self.crimescene_menu.set(next((l.name for l in self.world_data.locations if l.id == current_meta.crimeScene), "Select Crime Scene"))

        row += 1
        self.weapon_menu = self.create_form_row(scrollable_frame, row, "Murder Weapon", customtkinter.CTkOptionMenu, {'values': item_names})
        self.weapon_menu.set(next((i.name for i in self.world_data.items if i.id == current_meta.murderWeapon), "Select Weapon"))

        row += 1
        self.weapon_hidden_check = customtkinter.CTkCheckBox(scrollable_frame, text="Murder Weapon Hidden?")
        self.weapon_hidden_check.grid(row=row, column=1, padx=20, pady=(10,0), sticky="w")
        if current_meta.murderWeaponHidden:
            self.weapon_hidden_check.select()

        row += 1
        label = customtkinter.CTkLabel(scrollable_frame, text="Core Mystery Solution Details", anchor="w")
        label.grid(row=row, column=0, padx=20, pady=(10, 0), sticky="nw")
        self.solution_textbox = customtkinter.CTkTextbox(scrollable_frame, height=100)
        self.solution_textbox.grid(row=row, column=1, padx=20, pady=(10, 0), sticky="ew")
        self.solution_textbox.insert("1.0", current_meta.coreMysterySolutionDetails or "")
        
        row += 1
        narrative_viewpoints = ["First-Person", "Third-Limited (Sleuth)", "Third-Limited (Multiple)", "Omniscient", "Storyteller Omniscient", "Epistolary"]
        self.narrative_view_menu = self.create_form_row(scrollable_frame, row, "Narrative Viewpoint", customtkinter.CTkOptionMenu, {'values': narrative_viewpoints})
        self.narrative_view_menu.set(current_meta.narrativeViewpoint or "Select Viewpoint")

        row += 1
        narrative_tenses = ["Past", "Present"]
        self.narrative_tense_menu = self.create_form_row(scrollable_frame, row, "Narrative Tense", customtkinter.CTkOptionMenu, {'values': narrative_tenses})
        self.narrative_tense_menu.set(current_meta.narrativeTense or "Select Tense")

if __name__ == "__main__":
    app = App()
    app.mainloop()
