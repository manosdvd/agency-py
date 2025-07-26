import json
import os
from pathlib import Path
from dataclasses import asdict
from typing import Tuple, Type

from schemas import WorldData, CaseData

CASES_DIR = Path("cases")

def _sanitize_name(name: str) -> str:
    """Converts a human-readable name into a valid directory name."""
    return name.lower().replace(" ", "_").replace("-", "_")

def create_new_case(case_name: str) -> Path:
    """
    Creates the directory structure and initial empty files for a new case.
    """
    sanitized_name = _sanitize_name(case_name)
    case_path = CASES_DIR / sanitized_name
    world_data_path = case_path / "world_data"

    world_data_path.mkdir(parents=True, exist_ok=True)

    files_to_create = {
        case_path: ["case_data.json"],
        world_data_path: [
            "districts.json", "locations.json", "factions.json",
            "characters.json", "sleuth.json", "items.json"
        ]
    }

    for directory, filenames in files_to_create.items():
        for filename in filenames:
            filepath = directory / filename
            if not filepath.exists():
                with open(filepath, 'w') as f:
                    if filename in ["sleuth.json", "case_data.json"]:
                        json.dump({}, f)
                    else:
                        json.dump([], f)
    
    return case_path

def save_case(case_name: str, world_data: WorldData, case_data: CaseData):
    """
    Saves the current world and case data to their respective JSON files.
    """
    sanitized_name = _sanitize_name(case_name)
    case_path = CASES_DIR / sanitized_name
    world_data_path = case_path / "world_data"

    if not case_path.exists():
        print(f"Error: Case '{case_name}' does not exist. Please create it first.")
        return

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
    
    with open(world_data_path / "districts.json", "w") as f:
        json.dump([asdict(d, dict_factory=dict_factory) for d in world_data.districts], f, indent=4)

    with open(world_data_path / "factions.json", "w") as f:
        json.dump([asdict(fac, dict_factory=dict_factory) for fac in world_data.factions], f, indent=4)

    # Save the main case data
    with open(case_path / "case_data.json", "w") as f:
        json.dump(asdict(case_data, dict_factory=dict_factory), f, indent=4)

def load_case(case_name: str) -> Tuple[WorldData, CaseData]:
    """
    Loads all data for a given case from the file system.
    """
    sanitized_name = _sanitize_name(case_name)
    case_path = CASES_DIR / sanitized_name
    world_data_path = case_path / "world_data"

    if not case_path.exists():
        raise FileNotFoundError(f"Case '{case_name}' not found at {case_path}")

    # Dynamically import schemas to avoid circular dependencies if they grow
    from schemas import Character, Location, District, Faction, Sleuth, Item
    from schemas import CaseData, CaseMeta, Clue, CaseSuspect, CaseLocation, InterviewQuestion, CaseWitness

    def _load_from_file(path: Path, data_class: Type):
        if path.exists() and path.stat().st_size > 2:
            with open(path, 'r') as f:
                data = json.load(f)
                if isinstance(data, list):
                    return [data_class(**item) for item in data]
                return data_class(**data)
        return [] if data_class not in [Sleuth, CaseData] else None


    characters = _load_from_file(world_data_path / "characters.json", Character)
    locations = _load_from_file(world_data_path / "locations.json", Location)
    districts = _load_from_file(world_data_path / "districts.json", District)
    factions = _load_from_file(world_data_path / "factions.json", Faction)
    sleuth = _load_from_file(world_data_path / "sleuth.json", Sleuth)
    items = _load_from_file(world_data_path / "items.json", Item)

    world_data = WorldData(
        characters=characters,
        locations=locations,
        districts=districts,
        factions=factions,
        sleuth=sleuth,
        items=items
    )

    # Load case data with nested reconstruction
    case_data_dict = {}
    case_data_path = case_path / "case_data.json"
    if case_data_path.exists() and case_data_path.stat().st_size > 2:
        with open(case_data_path, 'r') as f:
            case_data_dict = json.load(f)

    if 'caseMeta' in case_data_dict and case_data_dict['caseMeta']:
        case_data_dict['caseMeta'] = CaseMeta(**case_data_dict['caseMeta'])
    
    if 'clues' in case_data_dict:
        case_data_dict['clues'] = [Clue(**clue_data) for clue_data in case_data_dict['clues']]
        
    if 'keySuspects' in case_data_dict:
        reconstructed_suspects = []
        for suspect_data in case_data_dict['keySuspects']:
            if 'interview' in suspect_data:
                suspect_data['interview'] = [InterviewQuestion(**iq_data) for iq_data in suspect_data['interview']]
            reconstructed_suspects.append(CaseSuspect(**suspect_data))
        case_data_dict['keySuspects'] = reconstructed_suspects

    if 'caseLocations' in case_data_dict:
        reconstructed_locations = []
        for loc_data in case_data_dict['caseLocations']:
            if 'witnesses' in loc_data:
                loc_data['witnesses'] = [CaseWitness(**w) for w in loc_data['witnesses']]
            reconstructed_locations.append(CaseLocation(**loc_data))
        case_data_dict['caseLocations'] = reconstructed_locations

    case_data = CaseData(**case_data_dict)

    return world_data, case_data
