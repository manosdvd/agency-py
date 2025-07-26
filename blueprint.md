### Project Blueprint: The Agency (Python Version)

**Document Control**

* **Version:** 1.0  
* **Date:** July 25, 2025  
* **Status:** Active Development

### 1\. Core Philosophy: Build, Test, Repeat

This project will follow an iterative and incremental development strategy. Our goal is to build the application in layers, ensuring each layer is stable and testable before we add more complexity. This approach allows us to manage complexity, find bugs early, and ensure the final product is robust and reliable.

### Phase 0: Project Setup & Foundation

**Objective:** To establish a clean, fully configured Python project with a virtual environment and all core modules in place.

* **Task 0.1: Establish Core Modules**  
  * **Purpose:** To create the foundational Python files for the application's structure.  
  * **Action:** Create the initial schemas.py, case\_manager.py, and gui.py files.  
  * **Status:** Complete.  
* **Task 0.2: Set Up Virtual Environment**  
  * **Purpose:** To create an isolated environment for managing project dependencies, preventing conflicts with system-wide packages.  
  * **Commands:**  
    python3 \-m venv venv  
    source venv/bin/activate

  * **Status:** Complete.  
* **Task 0.3: Install Dependencies**  
  * **Purpose:** To add the necessary libraries for building the graphical user interface.  
  * **Command:**  
    pip install customtkinter

  * **Status:** Complete.  
* **Task 0.4: Initialize Case Directory**  
  * **Purpose:** To create the top-level directory where all case data will be stored.  
  * **Action:** The case\_manager.py script will be responsible for creating the cases/ directory upon first run if it doesn't exist.  
  * **Status:** Complete.  
* **Checkpoint 0: Initial Run**  
  * After completing the setup, run python gui.py. The application window should launch without errors, demonstrating that the core modules and dependencies are correctly configured.

### Phase 1: Data Management & Core Logic

**Objective:** To ensure data can be reliably created, stored, and retrieved from the file system according to the defined schemas.

* **Task 1.1: Finalize Data Schemas**  
  * **Purpose:** To create a complete and accurate Python representation of all data entities using dataclasses.  
  * **Action:** Review schemas.py to ensure all fields from the original schemas.ts are present with correct Python typing (str, int, bool, List, Optional, Literal).  
  * **Status:** Complete.  
* **Task 1.2: Implement and Test File Operations**  
  * **Purpose:** To build and verify the functions that handle all interactions with the file system.  
  * **Action:** Fully implement and unit test the create\_new\_case, save\_case, and load\_case functions in case\_manager.py.  
  * **Status:** Complete.  
* **Checkpoint 1: Data Integrity Test**  
  * Write a simple test script (or use the if \_\_name\_\_ \== "\_\_main\_\_" block in case\_manager.py) to programmatically create a new case, populate WorldData and CaseData objects, save them, and then load them back to verify that the data remains unchanged through the save/load cycle.

### Phase 2: GUI Implementation & Data Binding

**Objective:** To build a fully interactive and data-driven graphical user interface for both the "World Builder" and "Case Builder."

* **Task 2.1: Build World Builder UI**  
  * **Purpose:** To create the complete user interface for creating and editing all world assets.  
  * **Action:** In gui.py, build out the two-pane editor (list and form) for each asset tab (Characters, Locations, Items, etc.). The forms should contain a widget for every field in the corresponding dataclass.  
  * **Status:** In Progress.  
* **Task 2.2: Build Case Builder UI**  
  * **Purpose:** To create the data input forms for the "Case Builder" tab.  
  * **Action:** Build out the forms for the "Case Details," "Key Suspects," "Case Locations," and "Clues" tabs, ensuring all fields from the schemas are represented.  
  * **Status:** In Progress.  
* **Task 2.3: Implement Data Binding**  
  * **Purpose:** To connect the GUI widgets to the underlying data objects, allowing for dynamic display and updates.  
  * **Action:**  
    1. Ensure that when an item is selected from a list, its data is correctly loaded into the corresponding form widgets.  
    2. Implement the "Save" button functionality to read the current values from the form widgets, update the in-memory WorldData/CaseData objects, and call case\_manager.save\_case.  
* **Checkpoint 2: Full UI and I/O Test**  
  * At the end of this phase, the entire application UI will be functionally complete. We will perform end-to-end testing: launch the app, load a case, make changes in various forms in both the World Builder and Case Builder, save the case, close the app, and relaunch to confirm that all changes have been persisted correctly.

### Phase 3: Advanced Logic & Validation

**Objective:** To implement the core validation engine that provides feedback on the logical consistency and solvability of the created mystery.

* **Task 3.1: Create Validation Module**  
  * **Purpose:** To have a dedicated module for all case validation logic.  
  * **Action:** Create a new file, validator.py.  
* **Task 3.2: Implement Validation Rules**  
  * **Purpose:** To translate the validation logic from the original project into Python.  
  * **Action:** In validator.py, create functions that correspond to the rules defined in validator-rules.json. These functions will take the WorldData and CaseData objects as input and return a list of feedback messages.  
* **Task 3.3: Integrate Validator with GUI**  
  * **Purpose:** To display validation feedback to the user in real-time.  
  * **Action:**  
    1. Create a "Validation" tab within the "Case Builder."  
    2. When the "Validation" tab is selected, call the functions from validator.py.  
    3. Display the returned feedback messages in a user-friendly format within the tab, using different colors or icons for errors, warnings, and insights.  
* **Checkpoint 3: Final Review & Test**  
  * This is the final checkpoint for the core application. We will create several test cases with known logical flaws (e.g., an unsolvable case, a dead-end location) to ensure the validation system correctly identifies and reports them.