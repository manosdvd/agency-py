Project Blueprint: The Agency Case Builder
Official Repository: https://github.com/manosdvd/agency-py/
Objective: Develop a standalone desktop application, "The Agency," for authoring intricate and logically sound detective stories. This document serves as the master plan and single source of truth for its development in a Python environment.
1. Core Vision & Strategic Phases
 * Product: "The Agency" is an integrated authoring tool for narrative designers. It provides a comprehensive, intuitive environment for creating, managing, and rigorously validating all game data, from individual CaseFile mysteries to the global lore and assets of the game world.
 * Primary Function: To empower a writer to build a complete, self-contained mystery as a structured data file, which contains every element needed for a separate game application to run the story.
 * Secondary Function: To serve as an active writing reference tool, allowing the author to quickly search and cross-reference the entire world's data.
 * Core Philosophy: The creative process is divided into three phases: Build a World, Construct a Case, and Ensure a Solvable Mystery.
 * Note that this software is intended to, and is only logically capable of, assisting with the creation of a mystery plot, not narrative or story/character arcs. 
 * Strategic Phases:
   * Phase I (V1 - The Comprehensive Editor & Validator): Build a robust manual editor for creating all world and case data, coupled with integrated real-time and pre-export logical validation. (Partially Complete)
   * Phase II (V2 - The World-Builder & Plot Graph): Expand the tool to manage global game world data more dynamically and introduce advanced creative assistance tools, including the fully interactive plot graph.
   * Phase III (V3 - The Generator): Introduce procedural generation capabilities to assist in the rapid creation of case skeletons and characters.
2. UI/UX Design & Authoring Experience
The user experience must be intuitive, powerful, and visually engaging, blending a classic noir aesthetic with modern usability. The goal is to minimize the author's cognitive load so they can focus on creativity.
 * Aesthetic & Design System:
   * Theme: Noir. A dark, navy-blue background with high-contrast text and UI elements in shades of blue and white.
   * Feel: Tactile and analog-inspired within a clean digital interface. Elements should evoke the feeling of managing physical file folders, bulletin boards, and case files.
   * Design Language (Material Design Adaptation): We will adopt Google Material Design's structural and behavioral principles (elevation, component states, ripple effects) but override its color palette with our Noir theme.
 * Global UI Layout:
   * Main Navigation: The application shell will have two primary top-level tabs: "World Builder" and "Case Builder".
   * Secondary Navigation: A persistent left-side navigation panel will display icons for the different asset categories within the selected main tab.
   * Tertiary Navigation: To the left of the content area is a list of the assets in the category selected (including an Add and search/filter function). Selecting an asset will show that asset in the content area.
   * Content Area: The main content area will use horizontal sub-tabs to manage information density and avoid overwhelming the user. Individual panes must scroll internally. Assets will have save and delete buttons.
   * Global Search: A prominent, persistent search bar must be present at all times.
   * Import and Export: Cases, asset categories, and individual assets can be exported and imported in an easily portable data package.
3. The World Builder: Specialized Authoring Tools
The "World Builder" is a suite of specialized visual tools designed to help authors intuitively create and manage the complex relationships that bring a world to life.
 * Character Relationship Graph (Social Graph): A visual, node-based editor focused exclusively on character connections (e.g., "Family," "Rival," "Owes Money To").
 * Geographical Layout Tool (Map Tool): An interactive map interface where authors can place location assets to manage spatial relationships, travel routes, and adjacencies.
 * Faction Dynamics Map: A visual diagram for modeling the relationships and power structures between factions (e.g., "Allied," "At War").
 * Lore & World History Timeline: A dedicated, interactive timeline for plotting significant historical events and character backstories, distinct from the case-specific eventChain.
4. The Case Builder: Core Authoring Components
 * Core UI Component: The Interactive Bulletin Board (Plot Graph):
   * Concept: The author's primary workspace for structuring the case. It is a clean, powerful, and technical visual diagramming tool.
   * Functionality: All case assets can be dragged onto a pannable, zoomable canvas as nodes. The author can graphically link nodes to define the logical flow of the investigation, and the board provides direct visual feedback for validation errors.
 * Core UI Component: The Gamified Timeline Editor (eventChain)
   * Objective: To transform the creation of the case's ground-truth timeline from a tedious data-entry task into an engaging, puzzle-like experience.
   * Guided, Backward-Flowing Design: The authoring process is guided to work backward from "The Crime" event, with the UI prompting the user with causal questions to build the timeline step-by-step.
   * Interactive Validation: The Validator provides real-time feedback directly on the timeline, immediately flagging chronological or logical impossibilities.
5. Data & Performance Architecture
This section outlines the architectural decisions for data management, focusing on ensuring the application is fast, responsive, and scalable, even with large and complex case files.
 * Data Storage Model: File-Based JSON
   * Decision: The application will continue to use a directory of human-readable .json files as its primary storage method. This approach is chosen over a formal database (like SQL/SQLite) for several key reasons:
     * Portability: A case is a self-contained folder that can be easily shared, version-controlled, and used by other tools.
     * Simplicity: It avoids the complexity of database setup, management, and the need for import/export routines.
     * Direct Output: The storage format is the final output format, eliminating a conversion step.
 * Performance Strategy: In-Memory Indexing
   * Concept: The primary performance bottleneck is not loading files, but searching and cross-referencing data within the application. To solve this, upon loading a case, the application will create in-memory "indexes" of the data.
   * Implementation: Instead of repeatedly searching through lists of assets (an O(n) operation), the application will generate dictionaries (hash maps) that map asset IDs to the asset objects themselves. This makes lookups instantaneous (an O(1) operation). This strategy will be the backbone of the fast global search and the responsive cross-referencing dropdowns.
 * Efficient Rendering Techniques:
   * List Virtualization: For long lists of assets (e.g., hundreds of characters in the World Builder), the UI will only render the items currently visible on the screen. As the user scrolls, items that move out of view will be de-rendered and new ones will be rendered, keeping the application's memory usage low and scrolling smooth.
   * Optimized Graph Rendering: The Interactive Bulletin Board will be built for performance. It will use optimized rendering techniques (e.g., layered canvases, selective re-drawing) to ensure that panning, zooming, and manipulating hundreds of nodes remains fluid and does not cause UI lag.
 * File Management & Error Handling:
   * Graceful Error Handling: The application must never crash due to a file error.
     * User-Friendly Messages: Display clear, specific error dialogs for issues like "File Not Found" or "Invalid File Format."
     * Logging: Write detailed technical error messages to a local error.log file for debugging.
     * Data Loss Prevention: If a save operation fails, the application must keep the current data safely in memory and prompt the user to try saving again to a different location.
6. The Validator Powertool
The Validator is the software's most critical feature. It is an intelligent "story editor" that provides real-time, actionable feedback.
 * UI Integration: The Validator's feedback must be persistently visible in the UI and update in real-time.
 * Actionable Suggestions: Each validation issue will be generated from a template populated with dynamic data, providing a clear description, a concrete suggestion, and a "Go to Issue" button that navigates the user to the source of the problem.
 * Validation Tiers to Implement:
   * Tier 1: Foundational Integrity (Errors): Checks for the existence and uniqueness of core assets and valid ID references.
   * Tier 2: Logical Consistency (Errors): Checks for solvability ("Orphan Clues"), causality ("Circular Logic"), lie integrity ("Undebunkable Lies"), chronology, and unique solutions.
   * Tier 3: Playability & Narrative Craft (Warnings): Checks for plausible suspects, red herring sufficiency, and pacing issues.
   * Tier 4: Player Experience & Cognition (Warnings): Checks for cognitive overload and the potential for "Aha!" moments.
7. The Authoring & Generation Engine
 * AI as Creative Co-Pilot: The AI's role is to augment, not replace, the author.
   * Dual-Voice Model: The AI must operate in two distinct modes: a clinical, fact-based Tool Assistant for analysis and a character-driven Content Generator that adopts the voiceModel and dialogueStyle from the character schema.
   * Specific Use Cases:
     * "What If" Scenarios: Prompt the AI with a change (e.g., "What if Character X was secretly the killer?") and have it suggest plot implications.
     * Automated Clue Suggestion: AI suggests plausible clues based on context.
     * Dialogue Polishing: Offer alternative phrasing for character dialogue.
     * Validator Explanations: AI provides more in-depth explanations for validation errors.
     * Pacing Analysis: Leverage AI to analyze the eventChain and suggest adjustments.
8. Future Considerations: Collaboration & Version Control
 * Cloud Sync/Storage: Options to save/load cases from cloud services.
 * Basic Versioning: The ability to save different iterations of a case file and revert to previous versions.
 * Comment/Annotation System: Allowing authors to leave notes directly within the case data.
9. Accessibility & Inclusivity
 * Keyboard Navigation: All UI elements must be fully navigable and operable via keyboard.
 * Screen Reader Compatibility: Elements will be designed with proper semantic markup.
 * Customizable UI: Users will be able to adjust font sizes and select an alternative high-contrast theme.
10. Testing & Quality Assurance
 * Unit Testing: Core logic, especially data schemas and validation rules, will be covered by unit tests.
 * Integration Testing: The interaction between different components will be tested.
 * User Acceptance Testing (UAT): The application will be beta-tested by actual writers.
 * Performance Testing: The Bulletin Board and other data-intensive views will be tested with hundreds of nodes to ensure responsiveness, verifying the effectiveness of the in-memory indexing and rendering strategies.
11. Definition of Done: Master Checklist
The project is considered "done" when all of the following criteria are met and verified.
[ ] 1. Core Application & Data Management
 * [ ] The application launches into a stable main window.
 * [ ] User can perform all file operations: New, Open, Save, Save As, Import, Export.
 * [ ] All data operations are robust and feature graceful error handling.
[ ] 2. Performance & Architecture
 * [ ] Data is loaded into indexed in-memory structures for fast lookups.
 * [ ] The global search and cross-reference dropdowns are instantaneous, even with large datasets.
 * [ ] Long asset lists use virtualization to ensure smooth scrolling.
 * [ ] The Interactive Bulletin Board remains fluid and responsive with hundreds of nodes.
[ ] 3. UI/UX & Authoring Experience
 * [ ] The full three-pane (navigation/list/detail) UI is implemented and functional.
 * [ ] The Noir/Material Design aesthetic is applied consistently.
 * [ ] Every field from every schema is represented by a corresponding UI input with a tooltip.
 * [ ] All cross-reference fields are implemented as searchable selectors with "Go to Asset" functionality.
 * [ ] Image uploading and viewing is functional for all relevant assets.
 * [ ] The World Builder's specialized tools (Social Graph, Map Tool, etc.) are implemented.
 * [ ] The Interactive Bulletin Board is fully implemented as a technical diagramming tool.
 * [ ] The Gamified Timeline Editor for the eventChain is fully implemented.
[ ] 4. Asset Implementation (All Schemas)
 * [ ] World Builder: Full CRUD functionality is complete for all world asset types.
 * [ ] Case Builder: All case-specific editors are fully functional.
[ ] 5. Validator Implementation
 * [ ] The Validator panel is always visible and updates in real-time.
 * [ ] All Tier 1, 2, 3, and 4 validation rules are implemented and functional.
 * [ ] Each validation message includes a working "Go to Issue" button.
[ ] 6. AI Integration Placeholder
 * [ ] A UI button for "Generate with AI" exists next to designated text fields.
 * [ ] The application architecture is ready for AI integration, including API key management and the dual-voice model.
[ ] 7. Accessibility & Testing
 * [ ] The application meets the defined accessibility standards.
 * [ ] The core logic, validation rules, and performance architecture are covered by a suite of tests.


