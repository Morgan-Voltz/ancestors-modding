# Contributing to Ancestors Modding

Thanks for your interest in helping document and mod Ancestors: The Humankind Odyssey!

---

## How you can help

### Share your discoveries
Found a new offset? Identified what a game value does? Figured out a new modding technique? Open an issue or PR with your findings.

### Test and report
Try the existing tools and mods. Report bugs, crashes, or unexpected behavior. Include:
- What you did
- What happened
- What you expected
- Your game version (Steam/Epic/GOG)

### Write documentation
Improve existing docs or write new ones. Areas that need work:
- Map/level system documentation
- Audio (Wwise) modding guide
- Blueprint modification guide
- Texture modding pipeline

### Build tools
Create new tools or improve existing ones:
- CLI tools for specific mod types
- Asset converters
- Blender addons/scripts for Ancestors-specific workflows

### Create mods
Build mods and share them! The more mods exist, the more attention the modding scene gets.

---

## Guidelines

### Documentation
- Write in English for maximum reach (French notes welcome as comments)
- Include file paths, offsets, and concrete values — not just descriptions
- When documenting a discovery, explain how you found it so others can learn
- Update existing docs rather than creating duplicates

### Code
- Python for tools (most accessible language)
- Include comments explaining the "why", not just the "what"
- No original game assets in the repository
- Test your changes before submitting

### Commits
- Clear, descriptive commit messages
- One logical change per commit
- Reference issues when applicable

---

## What NOT to include

- Original game files (.uasset, .pak, .wem, .tga, .psk, etc.)
- Game executables or DLLs
- Copyrighted content from Panache Digital Games
- Piracy tools or circumvention methods

This project is about **tools and documentation**, not redistribution.

---

## Project structure

```
ancestors-modding/
├── README.md                  ← Project overview and quick start
├── CONTRIBUTING.md            ← This file
├── LICENSE                    ← MIT License
├── docs/
│   ├── GETTING_STARTED.md     ← Beginner guide
│   ├── ANIMAL_DATABASE.md     ← All animal stats and files
│   ├── EVOLUTION_GUIDE.md     ← Neural evolution system
│   ├── ASSET_MAP.md           ← Full asset inventory
│   ├── GAME_ARCHITECTURE.md   ← Technical architecture
│   ├── MODDING_PIPELINE.md    ← How to make mods
│   ├── PDB_ANALYSIS.md        ← C++ class documentation
│   ├── EXTRACTED_ASSETS.md    ← Exported 3D models/textures
│   ├── FINDINGS_LOG.md        ← Research journal
│   └── TROUBLESHOOTING.md     ← Common problems and fixes
└── tools/
    ├── AncestorsDifficultyMod.py  ← GUI difficulty manager
    ├── patch_health.py            ← CLI health patcher
    └── Launch_Mod_Manager.bat     ← Windows launcher
```

---

## Setting up for development

1. Clone the repo
2. Install Python 3.10+
3. Download [repak](https://github.com/trumank/repak/releases)
4. Own the game on Steam
5. Read [GETTING_STARTED.md](docs/GETTING_STARTED.md)

No additional dependencies needed — everything uses Python standard library.
