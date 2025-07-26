The Agency
A tool for authoring intricate and logically sound detective stories.
Overview
The Agency is a standalone desktop application designed to be an all-in-one authoring tool for writers and game designers. Its mission is to solve a core problem in mystery writing: managing the immense complexity of a compelling narrative while ensuring the final story is both logically sound and deeply satisfying for the audience.
It provides a structured, visually-driven environment that separates the creative process into three distinct phases, empowering creators to focus on the art of storytelling by providing a robust framework to manage the science of a perfectly constructed mystery.
Core Features
The Agency is built around a powerful workflow that guides the author from world-building to final validation.
1. Build a Living World
Create a rich, interconnected database of every person, place, and object that forms the foundation of your narrative. This is about defining the "ground truth" of your universe before the crime even happens.
 * Create a Rich Database: Build a repository of every person, place, and object relevant to your story.
 * Specialized Visual Tools: Go beyond simple forms with dedicated editors for:
   * Social Graphs: Visually map character relationships (allies, rivals, family).
   * Geographical Maps: Define the spatial relationships between key locations.
   * Faction Dynamics: Model the power structures and conflicts between different groups.
 * Interconnected Assets: Develop characters with detailed profiles, vivid locations, and significant items that can organically serve as clues, motives, or alibis.
2. Construct a Case
Weave your world assets into a dynamic plot by defining the central crime and crafting the narrative path using intuitive, visual tools.
 * The Interactive Bulletin Board: The centerpiece of the Case Builder. A visual, node-based "murder board" where you can drag and drop assets, draw connections, and see the entire web of causality at a glance.
 * The Gamified Timeline Editor: Construct the case's ground-truth eventChain with a guided, interactive timeline. Work backward from the crime as the software prompts you with causal questions, turning a complex logical task into an engaging puzzle.
 * Detailed Narrative Crafting: Create interview questions, define lies, and explicitly link them to the clues that can debunk them, ensuring every piece of dialogue serves a purpose.
3. Ensure a Solvable Mystery
The Validator is the software's "secret sauce"—an intelligent story editor that acts as an impartial judge of your case's logic and quality, providing real-time feedback as you write.
 * Automated Logic Checker: The Validator runs constantly in the background, providing live feedback on the structural integrity of your mystery.
 * Prevent Plot Holes: The multi-tiered system identifies critical errors and provides actionable suggestions to fix them:
   * Logical Errors: Catches "orphan" clues that can't be discovered, "undebunkable" lies, and circular logic.
   * Narrative Warnings: Flags potential playability issues like a lack of plausible suspects, weak red herrings, or poor pacing.
   * Cognitive Analysis: Warns you if the beginning of your case might overwhelm the player with too much information.
 * Focus on Creativity: Let the software handle the logical bookkeeping so you can focus on telling a great story.
Getting Started
To get started with The Agency, follow these steps:
 * Clone the repository:
   git clone https://github.com/manosdvd/agency-py.git

 * Navigate to the project directory:
   cd agency-py

 * Install dependencies:
   pip install -r requirements.txt

 * Run the application:
   python3 main.py

Project Structure
agency-py/
├── .gitignore
├── blueprint.md        # Project vision and design documentation
├── case_builder.py     # UI components for the Case Builder view
├── data_manager.py     # Handles loading and saving of case/world data
├── main.py             # Main application entry point (Flet UI)
├── my_control.py       # Contains the core application logic and state
├── README.md           # This file
├── requirements.txt    # Project dependencies
├── schemas.py          # Defines the data structures for the application
├── validator.py        # UI components for the Validator view
└── cases/              # Contains all case data
    └── the_crimson_stain/
        ├── case_data.json
        └── world_data/
            ├── characters.json
            ├── districts.json
            ├── factions.json
            ├── items.json
            ├── locations.json
            └── sleuth.json

Contributing
Contributions are welcome! If you have any ideas, suggestions, or bug reports, please open an issue or submit a pull request.
