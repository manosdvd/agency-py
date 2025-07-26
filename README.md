# The Agency

**A tool for authoring intricate and logically sound detective stories.**

## Overview

The Agency is a standalone desktop application designed to be an all-in-one authoring tool for writers and game designers to create complex and logically sound detective stories. It provides a structured environment to manage the web of information that makes up a compelling mystery, separating the creative process into three distinct phases.

## Core Features

### 1. Build a Living World

*   **Create a Rich Database:** Build a repository of every person, place, and object relevant to your story.
*   **Define Ground Truth:** Establish a consistent world with detailed characters, locations, and items to ensure depth and logical consistency.
*   **Interconnected Assets:** Develop characters with detailed profiles, vivid locations, and significant items that can serve as clues or motives.

### 2. Construct a Case

*   **Weave a Dynamic Plot:** Take your world assets and craft a dynamic plot by defining the central crime and narrative path.
*   **Design the Investigation:** Structure the flow of information, ensuring the plot is driven by evidence and deduction.
*   **Detailed Narrative Crafting:** Create interview questions, define lies, and link them to debunking clues.

### 3. Ensure a Solvable Mystery

*   **Automated Logic Checker:** Get real-time feedback on the structural integrity of your mystery.
*   **Prevent Plot Holes:** The validator identifies orphaned clues, undebunkable lies, and narrative dead ends.
*   **Focus on Creativity:** The software handles the logical bookkeeping, allowing you to focus on storytelling.

## Getting Started

To get started with The Agency, follow these steps:

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/your-username/agency-py.git
    ```
2.  **Navigate to the project directory:**
    ```bash
    cd agency-py
    ```
3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
4.  **Run the application:**
    ```bash
    python3 main.py
    ```

## Project Structure

```
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
```

## Contributing

Contributions are welcome! If you have any ideas, suggestions, or bug reports, please open an issue or submit a pull request.