### **The Agency: Project Vision & End Goal**

The ultimate goal of this project is to create a suite of tools and a gameplay experience centered around an all-in-one authoring application, The Agency, for creating intricate and logically sound detective stories.

The project is divided into two primary components:

1. The Case Builder: A powerful, developer-facing web application used to generate, edit, and verify a large library of pre-built mystery cases. This tool uses a robust logic engine for structure and offers optional AI assistance for creative flavor text.  
2. The Game: The public-facing desktop application (built in Godot) that players will experience. It loads the pre-built case files and provides the UI and tools for the player to solve them.

At its core, the software is designed to solve a key problem for writers: managing the complex web of information that makes up a compelling mystery. The application will provide a structured, user-friendly environment that separates the creative process into distinct, manageable phases.

### 1\. Build a Living World

* What It Is: The foundational database for the narrative. This is where the creator builds a rich, interconnected repository of every person, place, and object that could be relevant to a story. It's about defining the building blocks of the universe before the crime even happens.  
* Why It Matters: A mystery is only as compelling as its setting and cast. By creating these assets first, the author establishes a "ground truth" for the world, ensuring consistency and depth. A character's pre-defined motivations can organically create plausible motives for a crime. A location's established layout can dictate opportunity. This front-loading of creative work makes the subsequent case construction more intuitive and logical.  
* Specific Details:  
  * Characters: Will have detailed profiles including biography, personality, secrets, relationships, and a personality object that defines their baseReliability and biasVector to support a dynamic unreliability system.  
  * Locations: Will be vivid settings with a defined atmosphere, a list of keyCharacters often found there, and potential associatedItems that belong in that space.  
  * Items: Will be significant objects with a clear description, significance to the plot, and properties that might make them a possibleMeans, possibleMotive, or possibleOpportunity.

### 2\. Construct a Case

* What It Is: The storytelling phase where the author uses a visual, node-based interface to weave world assets into a dynamic plot. This involves defining the central crime, crafting the narrative path, and structuring the flow of information.  
* Why It Matters: This structured, visual approach forces the author to think like a detective. Instead of a linear form, a graph editor allows the author to see the web of causality, manage branching narratives, and identify structural issues intuitively. This ensures the plot is driven by evidence and deduction, leading to a more satisfying mystery.  
* Specific Details:  
  * Visual Plot Graph: The primary authoring tool will be a node-based graph editor (similar to Twine or Articy:Draft). Characters, clues, and locations will be nodes, and their relationships will be visible, editable connections. This is a mission-critical component for enabling the creation of high-quality, complex mysteries.  
  * Systemic Red Herrings: Red herrings will be architected as complete, internally consistent, but ultimately incorrect narrative paths (redHerringPaths). Each path will have a plausible false culprit, a false motive, supporting clues, and a specific underminingClueId that allows the player to definitively disprove it.  
  * Dynamic Interviews: Interviews will be a core mechanic for plot progression. Answers can be flagged as isLie, which then requires linking to a debunkingClue. A character's truthfulness will be calculated dynamically based on their personality and the player's faction reputation.  
  * Subplots as Mechanical Unlocks: Subplots will be designed as self-contained narrative arcs that intersect with the main plot. Completing a subplot will provide tangible rewards, such as unlocking a new location, revealing a critical clue for the main case, or altering faction reputation.

### 3\. Ensure a Solvable and Satisfying Mystery

* What It Is: An automated "story editor" that acts as a logic and narrative checker. It will provide real-time feedback on the structural integrity and the *quality* of the player's deductive experience.  
* Why It Matters: The validator's role is not just to prevent game-breaking errors but to actively help the author engineer a compelling and satisfying "Aha\!" moment for the player. It frees the author from the immense mental load of tracking every connection, allowing them to focus on creativity while the software analyzes the logical and cognitive framework.  
* Specific Details & Validation Rules:  
  * Logical Integrity Checks:  
    * Orphaned Clues: Identifies critical evidence with no discovery path.  
    * Undebunkable Lies: Verifies that every lie is connected to evidence that can prove it false.  
    * Core Mystery Logic: Ensures the culprit has a plausible path to the murder weapon and crime scene, and that clues exist for Means, Motive, and Opportunity.  
  * Narrative & Gameplay Quality Checks:  
    * Narrative Dead Ends: Flags locations or interviews that offer no path forward, preventing the investigation from stalling.  
    * Cognitive Load Warning: Analyzes the start of a case to warn the author if too many new characters, locations, or concepts are introduced at once, which could overwhelm the player.  
    * "Aha\!" Moment Potential: Analyzes the clue graph to find "linchpin" clues—clues whose value comes from synthesizing multiple, separate lines of investigation—and encourages the author to make their discovery a rewarding challenge.  
    * Red Herring Coherence: Checks that red herring subplots are plausible, internally consistent, and have a clear resolution that explains the suspicious evidence.

### 4\. The Authoring & Generation Engine

* What It Is: The technical backbone of content creation, combining human authorship, AI assistance, and procedural principles into a powerful, flexible workflow.  
* Why It Matters: This hybrid approach provides the author with ultimate control over the core puzzle and thematic direction of a case while leveraging automation to handle laborious tasks and enhance creativity.  
* Workflow & Features:  
  * Hybrid Authoring: The primary workflow will involve a human author using a visual plotting tool (e.g., Plottr) to design the narrative "scaffold" of a case. This scaffold is then exported and transformed by a script into a partial case\_file.json.  
  * AI as Creative Co-Pilot: The scaffold file is fed to a Large Language Model (LLM). The AI's role is not to invent logic, but to act as a creative partner:  
    * Fleshing Out Text: It populates empty fields with compelling, atmospheric prose for clue descriptions, location details, and character dialogue.  
    * Brainstorming: The author can prompt the AI to suggest alternative discovery paths, plausible red herrings for innocent characters, or potential plot twists based on the existing structure.  
  * Advanced LLM Prompting: To ensure high-quality output, the system will use a "Tree-of-Thoughts" (ToT) prompt structure. This forces the LLM to simulate a writer's room, where it brainstorms multiple scenarios, critiques them, and selects the most compelling option before generating the final output.

### 5\. Technical Architecture & Deployment

* What It Is: The high-level technical plan for building, connecting, and deploying the project's components.  
* Why It Matters: A clear architecture ensures that the different parts of the project can be developed independently and integrated smoothly, leading to a robust and performant final product.  
* Specifics:  
  * Case Builder (Web App):  
    * Framework: A modern web framework like React (using Vite for scaffolding).  
    * UI/Visualization: React Flow for the node-based plot graph editor, with UI components from a library like Lucide-react.  
    * State Management: Zustand for managing the application's state.  
  * The Game (Desktop App):  
    * Engine: Godot, chosen for its strength in 2D UI-driven games.  
  * Data Strategy:  
    * Interchange Format: The Case Builder will export cases as .json files. This is a universal, human-readable format.  
    * Game Data Format: The project will include a Godot import plugin. This plugin will run inside the Godot editor, read the .json case file, and convert it into native Godot Custom Resource files (.tres). This provides significantly better performance and engine integration for the final game.  
  * Deployment:  
    * The Case Builder web application can be deployed to a static hosting service like Vercel or Netlify.  
    * The final game will be built and packaged for distribution on platforms like itch.io or Steam.  
    * 