import json
import os
from pathlib import Path
from dataclasses import asdict
from typing import Tuple

# Import the data structures from our schemas file
from schemas import WorldData, CaseData

# Define the base directory where all cases will be stored.
# Using Path from pathlib is a modern and cross-platform way to handle file paths.
CASES_DIR = Path("cases")

def _sanitize_name(name: str) -> str:
    """Converts a human-readable name into a valid directory name."""
    return name.lower().replace(" ", "_").replace("-", "_")

def create_new_case(case_name: str) -> Path:
    """
    Creates the directory structure and initial empty files for a new case.
    This is the Python equivalent of the 'New Case' button functionality.
    
    Args:
        case_name: The human-readable name for the case (e.g., "The Missing Heir").

    Returns:
        The path to the newly created case directory.
    """
    sanitized_name = _sanitize_name(case_name)
    case_path = CASES_DIR / sanitized_name
    world_data_path = case_path / "world_data"

    print(f"Creating new case at: {case_path}")
    
    # Create the necessary directories. `exist_ok=True` prevents errors if the directory already exists.
    world_data_path.mkdir(parents=True, exist_ok=True)

    # Define the files to be created
    files_to_create = {
        case_path: ["case_data.json"],
        world_data_path: [
            "districts.json", "locations.json", "factions.json",
            "characters.json", "sleuth.json", "items.json"
        ]
    }

    # Create empty JSON files, each containing an empty list or object.
    for directory, filenames in files_to_create.items():
        for filename in filenames:
            filepath = directory / filename
            if not filepath.exists():
                with open(filepath, 'w') as f:
                    # sleuth.json and case_data.json should be objects, others are lists
                    if filename in ["sleuth.json", "case_data.json"]:
                        json.dump({}, f)
                    else:
                        json.dump([], f)
                print(f"  - Created {filepath}")
    
    return case_path

def save_case(case_name: str, world_data: WorldData, case_data: CaseData):
    """
    Saves the current world and case data to their respective JSON files.
    This function serializes the dataclass objects into a structured,
    human-readable JSON format.
    
    Args:
        case_name: The name of the case to save.
        world_data: The WorldData object containing all world-building assets.
        case_data: The CaseData object containing the specifics of the mystery.
    """
    sanitized_name = _sanitize_name(case_name)
    case_path = CASES_DIR / sanitized_name
    world_data_path = case_path / "world_data"

    if not case_path.exists():
        print(f"Error: Case '{case_name}' does not exist. Please create it first.")
        return

    print(f"Saving data for case: {case_name}")

    # Use `asdict` to convert dataclasses to dictionaries for JSON serialization.
    # The `lambda d: {k: v for (k, v) in d if v is not None}` part ensures
    # that fields with `None` values are not included in the JSON file, keeping it clean.
    dict_factory = lambda d: {k: v for (k, v) in d if v is not None}

    # Save world data components
    with open(world_data_path / "characters.json", "w") as f:
        json.dump([asdict(c, dict_factory=dict_factory) for c in world_data.characters], f, indent=4)
    
    with open(world_data_path / "locations.json", "w") as f:
        json.dump([asdict(loc, dict_factory=dict_factory) for loc in world_data.locations], f, indent=4)

    with open(world_data_path / "items.json", "w") as f:
        json.dump([asdict(i, dict_factory=dict_factory) for i in world_data.items], f, indent=4)

    if world_data.sleuth:
        with open(world_data_path / "sleuth.json", "w") as f:
            json.dump(asdict(world_data.sleuth, dict_factory=dict_factory), f, indent=4)
    
    # ... you would add similar blocks for factions and districts ...

    # Save the main case data
    with open(case_path / "case_data.json", "w") as f:
        json.dump(asdict(case_data, dict_factory=dict_factory), f, indent=4)
        
    print(f"Successfully saved '{case_name}'.")


def load_case(case_name: str) -> Tuple[WorldData, CaseData]:
    """
    Loads all data for a given case from the file system, reconstructing
    the dataclass objects from the JSON files.

    Args:
        case_name: The name of the case to load.

    Returns:
        A tuple containing the populated WorldData and CaseData objects.
    """
    sanitized_name = _sanitize_name(case_name)
    case_path = CASES_DIR / sanitized_name
    world_data_path = case_path / "world_data"

    if not case_path.exists():
        raise FileNotFoundError(f"Case '{case_name}' not found at {case_path}")

    print(f"Loading data for case: {case_name}")
    
    # Load world data by reading each JSON and reconstructing the dataclasses
    # The ** operator unpacks the dictionary into keyword arguments
    with open(world_data_path / "characters.json", 'r') as f:
        from schemas import Character # Local import to avoid circular dependency issues if schemas grow
        characters_data = json.load(f)
        characters = [Character(**data) for data in characters_data]

    with open(world_data_path / "locations.json", 'r') as f:
        from schemas import Location
        locations_data = json.load(f)
        locations = [Location(**data) for data in locations_data]

    # ... and so on for other world data files ...

    world_data = WorldData(characters=characters, locations=locations)

    # Load case data
    with open(case_path / "case_data.json", 'r') as f:
        from schemas import CaseData, CaseMeta, Clue, CaseSuspect # etc.
        case_data_dict = json.load(f)
        
        # Reconstruct nested dataclasses
        if 'caseMeta' in case_data_dict and case_data_dict['caseMeta']:
            case_data_dict['caseMeta'] = CaseMeta(**case_data_dict['caseMeta'])
        
        if 'clues' in case_data_dict:
            case_data_dict['clues'] = [Clue(**clue_data) for clue_data in case_data_dict['clues']]
            
        # ... and so on for keySuspects, caseLocations ...

        case_data = CaseData(**case_data_dict)

    return world_data, case_data

# --- Example Usage ---
if __name__ == "__main__":
    # 1. Create a new case. This builds the directory structure.
    case_name = "The Crimson Stain"
    create_new_case(case_name)

    # 2. Populate data using the schemas
    #    (In a real app, this would come from user input)
    from schemas import Character, Location, Item, WorldData, CaseData, CaseMeta

    # Create some world assets
    char1 = Character(id="char-01", fullName="Victor Blackwood", biography="A reclusive millionaire.", personality="Cunning", alignment="Lawful Evil", honesty=2, victimLikelihood=3, killerLikelihood=8)
    loc1 = Location(id="loc-01", name="Blackwood Manor", description="A sprawling, gothic estate.")
    item1 = Item(id="item-01", name="Letter Opener", description="A silver letter opener with a ruby pommel.", possibleMeans=True, possibleMotive=False, possibleOpportunity=False, cluePotential="Medium", value="Priceless", condition="Good")

    # Create the main WorldData object
    world_data_instance = WorldData(
        characters=[char1],
        locations=[loc1],
        items=[item1]
    )

    # Create the main CaseData object
    case_meta_instance = CaseMeta(
        victim="char-02", # ID of a character you would create
        culprit="char-01",
        crimeScene="loc-01",
        murderWeapon="item-01",
        coreMysterySolutionDetails="Victor Blackwood used the letter opener in his study."
    )
    case_data_instance = CaseData(caseMeta=case_meta_instance)

    # 3. Save the populated data to the file system
    save_case(case_name, world_data_instance, case_data_instance)

    # 4. Load the data back from the files
    try:
        loaded_world, loaded_case = load_case(case_name)
        print("\n--- Data Loaded Successfully ---")
        print(f"Loaded Character: {loaded_world.characters[0].fullName}")
        print(f"Loaded Crime Scene: {loaded_case.caseMeta.crimeScene}")
        print("------------------------------")
    except FileNotFoundError as e:
        print(e)

