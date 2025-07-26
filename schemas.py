# schemas.py
from dataclasses import dataclass, field
from typing import List, Optional, Literal, Union

# --- Type Aliases from schemas.ts ---

WealthClass = Literal[
    "Old Money Rich", "New Money Rich", "Business Person", "Working Stiff", "Poor", "Transient"
]

Alignment = Literal[
    "Lawful Good", "Neutral Good", "Chaotic Good",
    "Lawful Neutral", "True Neutral", "Chaotic Neutral",
    "Lawful Evil", "Neutral Evil", "Chaotic Evil"
]

Gender = Literal[
    "Male", "Female", "Nonbinary", "Trans Man", "Trans Woman", "Unknown", "Unspecified"
]


# --- World Data Schemas ---

@dataclass
class District:
    id: str
    name: str
    description: str
    image: Optional[str] = None
    wealthClass: Optional[WealthClass] = None
    atmosphere: Optional[str] = None
    populationDensity: Optional[Literal["Sparse", "Moderate", "Dense", "Crowded"]] = None
    notableFeatures: List[str] = field(default_factory=list)
    dominantFaction: Optional[str] = None
    keyLocations: List[str] = field(default_factory=list)

@dataclass
class Location:
    id: str
    name: str
    description: str
    type: Optional[str] = None
    district: Optional[str] = None
    owningFaction: Optional[str] = None
    dangerLevel: Optional[Literal[1, 2, 3, 4, 5]] = None
    population: Optional[int] = None
    image: Optional[str] = None
    keyCharacters: List[str] = field(default_factory=list)
    associatedItems: List[str] = field(default_factory=list)
    accessibility: Optional[Literal["Public", "Semi-Private", "Private", "Restricted"]] = None
    hidden: Optional[bool] = False
    internalLogicNotes: Optional[str] = None
    clues: List[str] = field(default_factory=list)

@dataclass
class Faction:
    id: str
    name: str
    description: str
    archetype: Optional[str] = None
    ideology: Optional[str] = None
    headquarters: Optional[str] = None
    resources: List[str] = field(default_factory=list)
    image: Optional[str] = None
    allyFactions: List[str] = field(default_factory=list)
    enemyFactions: List[str] = field(default_factory=list)
    members: List[str] = field(default_factory=list)
    influence: Optional[Literal["Local", "District-wide", "City-wide", "Regional", "Global"]] = None
    publicPerception: Optional[str] = None

@dataclass
class Character:
    id: str
    fullName: str
    biography: str
    personality: str
    alignment: Alignment
    honesty: int
    victimLikelihood: int
    killerLikelihood: int
    alias: Optional[str] = None
    age: Optional[int] = None
    gender: Optional[Gender] = None
    employment: Optional[str] = None
    image: Optional[str] = None
    faction: Optional[str] = None
    wealthClass: Optional[WealthClass] = None
    district: Optional[str] = None
    motivations: List[str] = field(default_factory=list)
    secrets: List[str] = field(default_factory=list)
    allies: List[str] = field(default_factory=list)
    enemies: List[str] = field(default_factory=list)
    items: List[str] = field(default_factory=list)
    archetype: Optional[str] = None
    values: List[str] = field(default_factory=list)
    flawsHandicapsLimitations: List[str] = field(default_factory=list)
    quirks: List[str] = field(default_factory=list)
    characteristics: List[str] = field(default_factory=list)
    vulnerabilities: List[str] = field(default_factory=list)
    voiceModel: Optional[str] = None
    dialogueStyle: Optional[str] = None
    expertise: List[str] = field(default_factory=list)
    portrayalNotes: Optional[str] = None

@dataclass
class Sleuth:
    id: str
    name: str
    city: str
    biography: str
    wealthClass: WealthClass
    archetype: str
    personality: str
    alignment: Alignment
    age: Optional[int] = None
    gender: Optional[Gender] = None
    employment: Optional[str] = None
    image: Optional[str] = None
    district: Optional[str] = None
    relationships: List[str] = field(default_factory=list)
    nemesis: Optional[str] = None
    values: List[str] = field(default_factory=list)
    flawsHandicapsLimitations: List[str] = field(default_factory=list)
    quirks: List[str] = field(default_factory=list)
    primaryArc: Optional[str] = None
    characteristics: List[str] = field(default_factory=list)
    motivations: List[str] = field(default_factory=list)
    secrets: List[str] = field(default_factory=list)
    vulnerabilities: List[str] = field(default_factory=list)
    voiceModel: Optional[str] = None
    dialogueStyle: Optional[str] = None
    expertise: List[str] = field(default_factory=list)
    portrayalNotes: Optional[str] = None

@dataclass
class Item:
    id: str
    name: str
    description: str
    possibleMeans: bool
    possibleMotive: bool
    possibleOpportunity: bool
    cluePotential: Literal["None", "Low", "Medium", "High", "Critical"]
    value: str
    condition: Literal["New", "Good", "Used", "Worn", "Damaged", "Broken"]
    image: Optional[str] = None
    type: Optional[str] = None
    defaultLocation: Optional[str] = None
    defaultOwner: Optional[str] = None
    use: List[str] = field(default_factory=list)
    uniqueProperties: List[str] = field(default_factory=list)
    significance: Optional[str] = None

@dataclass
class WorldData:
    """The root object for all world assets."""
    districts: List[District] = field(default_factory=list)
    locations: List[Location] = field(default_factory=list)
    factions: List[Faction] = field(default_factory=list)
    characters: List[Character] = field(default_factory=list)
    sleuth: Optional[Sleuth] = None
    items: List[Item] = field(default_factory=list)


# --- Case Data Schemas ---

@dataclass
class CaseMeta:
    victim: str
    culprit: str
    crimeScene: str
    murderWeapon: str
    coreMysterySolutionDetails: str
    murderWeaponHidden: Optional[bool] = False
    meansClue: Optional[str] = None
    motiveClue: Optional[str] = None
    opportunityClue: Optional[str] = None
    redHerringClues: List[str] = field(default_factory=list)
    narrativeViewpoint: Optional[Literal[
        "First-Person", "Third-Limited (Sleuth)", "Third-Limited (Multiple)",
        "Omniscient", "Storyteller Omniscient", "Epistolary"
    ]] = None
    narrativeTense: Optional[Literal["Past", "Present"]] = None
    openingMonologue: Optional[str] = None
    ultimateRevealSceneDescription: Optional[str] = None
    successfulDenouement: Optional[str] = None
    failedDenouement: Optional[str] = None

@dataclass
class InterviewQuestion:
    questionId: str
    question: str
    answerId: str
    answer: str
    isLie: bool
    isClue: bool
    debunkingClue: Optional[str] = None
    clueId: Optional[str] = None
    hasItem: Optional[str] = None

@dataclass
class CaseSuspect:
    characterId: str
    interview: List[InterviewQuestion] = field(default_factory=list)

@dataclass
class CaseWitness:
    characterId: str
    interview: List[InterviewQuestion] = field(default_factory=list)

@dataclass
class CaseLocation:
    locationId: str
    locationClues: List[str] = field(default_factory=list)
    witnesses: List[CaseWitness] = field(default_factory=list)

@dataclass
class Clue:
    # Required fields (no default value) must come first.
    clueId: str
    criticalClue: bool
    redHerring: bool
    isLie: bool
    source: str
    clueSummary: str
    knowledgeLevel: Literal["Sleuth Only", "Reader Only", "Both", "Neither (Off-Page)"]
    
    # Optional fields (with default values) must come after required fields.
    discoveryPath: List[str] = field(default_factory=list)
    presentationMethod: List[Literal["Dialogue", "Setting/Description", "Character Action", "Introspection"]] = field(default_factory=list)
    characterImplicated: Optional[str] = None
    redHerringType: Optional[Literal["Decoy Suspect", "Misleading Object", "False Alibi", "Misleading Dialogue"]] = None
    mechanismOfMisdirection: Optional[str] = None
    debunkingClue: Optional[str] = None
    dependencies: List[str] = field(default_factory=list)
    requiredActionsForDiscovery: List[str] = field(default_factory=list)
    revealsUnlocks: List[dict] = field(default_factory=list) # e.g., {"type": "location_id", "id": "loc-01"}
    associatedItem: Optional[str] = None
    associatedLocation: Optional[str] = None
    associatedCharacter: Optional[str] = None

@dataclass
class ValidationResult:
    message: str
    type: Literal["error", "warning"]
    asset_id: Optional[str] = None
    asset_type: Optional[str] = None
    field_name: Optional[str] = None

@dataclass
class CaseData:
    """The root object for a specific mystery case."""
    caseMeta: Optional[CaseMeta] = None
    keySuspects: List[CaseSuspect] = field(default_factory=list)
    caseLocations: List[CaseLocation] = field(default_factory=list)
    clues: List[Clue] = field(default_factory=list)
