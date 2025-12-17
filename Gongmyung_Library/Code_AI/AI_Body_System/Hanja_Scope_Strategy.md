# Hanja Code Scope Strategy: The "Ideographic Venn Diagram"

## 1. Concept: Hanja as a Semantic Assembler
Western characters (Alphabet) are phonetic and linear. They form meaning only when strung together (s-t-r-i-n-g).
Eastern characters (Hanja) are **ideographic and modular**. A single character is often a compressed system of meanings, built like a Venn diagram.

*   **Radical (부수)**: The root domain or context (e.g., 氵 for Water/Network, 木 for Tree/Structure).
*   **Body (몸)**: The specific function or phonetic value.

## 2. Application to Code: "The Scattered Code Hunter"
The user pointed out that "scattered code" (code that is here and there, merged) is hard to define with linear paths.
Using the Hanja structure, we can define code scopes not by folder path, but by **Semantic Composition**.

### Example: "Bright" (明) Scope
If we want to find code that handles "Displaying (Sun/日)" AND "Data Reflection (Moon/月)", we look for the "明" scope.
*   **日 (Sun)**: UI Rendering code, CSS, Frontend.
*   **月 (Moon)**: Backend Logic, Database, Shadow DOM.
*   **明 (Bright)**: The intersection where Backend data is rendered to Frontend.

### Example: "Forest" (林) Scope
*   **木 (Tree)**: A single module or class.
*   **林 (Forest)**: A cluster of similar modules (e.g., a plugin system).
*   **森 (Deep Forest)**: The core engine where modules are densely packed.

## 3. Technical Implementation: "Semantic Tagging"
We can tag code blocks with "Radicals".

```python
# @radical: 氵 (Flow/Network)
def fetch_data():
    ...

# @radical: 目 (Eye/Vision/UI)
def render_view():
    ...

# @compound: 淚 (Tears = Water + Eye) -> Error Logging / Debug View
def log_error_to_screen():
    ...
```

## 4. Strategy for "Gongmyung"
1.  **Define Radicals**: Map system domains to Hanja radicals.
    *   CPU/Process = 火 (Fire)
    *   Memory/Storage = 土 (Earth)
    *   Network/Stream = 氵 (Water)
    *   User Interface = 目 (Eye) or 口 (Mouth)
    *   Kernel/Core = 心 (Heart)
2.  **Scan & Compose**: The `Narrative_Indexer` can be upgraded to a `Semantic_Composer`.
    *   It scans for keywords.
    *   If a file has both "Network" and "UI" keywords, it is tagged as "Communication" (e.g., 言 or 淸).
3.  **Venn Diagram Search**:
    *   "Find me all code that is 'Water' but NOT 'Fire'."
    *   "Find the 'Heart' of the system."

## 5. Next Step
Create a prototype `Hanja_Scope_Mapper.py` that defines these radicals and scans a file to assign it a "Hanja Character" based on its content.
