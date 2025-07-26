import pytest
from schemas import Character, Location, Item, Faction, District, Sleuth, CaseData, Clue, CaseMeta, InterviewQuestion, CaseSuspect, CaseLocation, CaseWitness

def test_character_creation():
    char = Character(
        id="char1",
        fullName="John Doe",
        biography="A simple man.",
        personality="Quiet",
        alignment="True Neutral",
        honesty=5,
        victimLikelihood=5,
        killerLikelihood=5
    )
    assert char.id == "char1"
    assert char.fullName == "John Doe"

def test_location_creation():
    loc = Location(
        id="loc1",
        name="Old House",
        description="A spooky old house."
    )
    assert loc.id == "loc1"
    assert loc.name == "Old House"

def test_item_creation():
    item = Item(
        id="item1",
        name="Rusty Key",
        description="A key.",
        possibleMeans=False,
        possibleMotive=False,
        possibleOpportunity=True,
        cluePotential="Low",
        value="10",
        condition="Used"
    )
    assert item.id == "item1"
    assert item.name == "Rusty Key"

def test_faction_creation():
    faction = Faction(
        id="fact1",
        name="The Shadows",
        description="A mysterious group."
    )
    assert faction.id == "fact1"
    assert faction.name == "The Shadows"

def test_district_creation():
    district = District(
        id="dist1",
        name="Downtown",
        description="Busy city center."
    )
    assert district.id == "dist1"
    assert district.name == "Downtown"

def test_sleuth_creation():
    sleuth = Sleuth(
        id="sleuth1",
        name="Sherlock Holmes",
        city="London",
        biography="Master detective.",
        wealthClass="Working Stiff",
        archetype="Detective",
        personality="Observant",
        alignment="Lawful Good"
    )
    assert sleuth.id == "sleuth1"
    assert sleuth.name == "Sherlock Holmes"

def test_clue_creation():
    clue = Clue(
        clueId="clue1",
        criticalClue=True,
        redHerring=False,
        isLie=False,
        source="Crime Scene",
        clueSummary="Bloody footprint.",
        knowledgeLevel="Sleuth Only"
    )
    assert clue.clueId == "clue1"
    assert clue.clueSummary == "Bloody footprint."

def test_case_meta_creation():
    meta = CaseMeta(
        victim="char1",
        culprit="char2",
        crimeScene="loc1",
        murderWeapon="item1",
        coreMysterySolutionDetails="It was the butler."
    )
    assert meta.victim == "char1"
    assert meta.culprit == "char2"

def test_interview_question_creation():
    iq = InterviewQuestion(
        questionId="q1",
        question="Where were you?",
        answerId="a1",
        answer="At home.",
        isLie=False,
        isClue=True
    )
    assert iq.questionId == "q1"
    assert iq.question == "Where were you?"

def test_case_suspect_creation():
    suspect = CaseSuspect(
        characterId="char1",
        interview=[]
    )
    assert suspect.characterId == "char1"

def test_case_location_creation():
    cl = CaseLocation(
        locationId="loc1",
        locationClues=[],
        witnesses=[]
    )
    assert cl.locationId == "loc1"

def test_case_witness_creation():
    cw = CaseWitness(
        characterId="char1",
        interview=[]
    )
    assert cw.characterId == "char1"
