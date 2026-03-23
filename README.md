# Ancestors: The Humankind Odyssey — Modding Toolkit

> **The first open-source modding documentation and tools for Ancestors: The Humankind Odyssey.**

Ancestors is an incredible game that never got modding support. Development stopped in 2020, and the community was left with no tools, no SDK, and no documentation. This project changes that.

Everything you need to start modding Ancestors is here — from understanding the game's internal architecture to building your own mods.

---

## What's inside

### Documentation

| Document | Description | Audience |
|----------|-------------|----------|
| [docs/GETTING_STARTED.md](docs/GETTING_STARTED.md) | **Start here** — First mod in 15 minutes | Beginners |
| [docs/ANIMAL_DATABASE.md](docs/ANIMAL_DATABASE.md) | All 14 species — stats, files, bones, animations | All modders |
| [docs/EVOLUTION_GUIDE.md](docs/EVOLUTION_GUIDE.md) | Neural evolution tree — 17 branches, conditions, structure | All modders |
| [docs/MODDING_PIPELINE.md](docs/MODDING_PIPELINE.md) | Step-by-step guide: extract → modify → repack → test | All modders |
| [docs/TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md) | Common problems and solutions | All modders |
| [docs/ASSET_MAP.md](docs/ASSET_MAP.md) | Full map of all 18,105 game assets | Advanced |
| [docs/GAME_ARCHITECTURE.md](docs/GAME_ARCHITECTURE.md) | Technical architecture — CDS system, module structure | Advanced |
| [docs/PDB_ANALYSIS.md](docs/PDB_ANALYSIS.md) | 508 C++ source classes identified from debug symbols | Advanced |
| [docs/EXTRACTED_ASSETS.md](docs/EXTRACTED_ASSETS.md) | Inventory of all extracted 3D models, textures, animations | 3D artists |
| [docs/FINDINGS_LOG.md](docs/FINDINGS_LOG.md) | Research journal — what works, what doesn't, and why | Contributors |
| [CONTRIBUTING.md](CONTRIBUTING.md) | How to contribute to this project | Contributors |

### Tools

| Tool | Description |
|------|-------------|
| [tools/AncestorsDifficultyMod.py](tools/AncestorsDifficultyMod.py) | GUI difficulty mod manager — customize animal health and player survival |
| [tools/patch_health.py](tools/patch_health.py) | CLI script to patch animal health values |

### Mod Releases

| Mod | Description |
|-----|-------------|
| [releases/](releases/) | Ready-to-distribute mod packages |

---

## Quick start — Make your first mod in 5 minutes

### Prerequisites
- [repak](https://github.com/trumank/repak/releases) — Download `repak.exe` from releases
- Python 3.10+

### 1. Extract an asset
```bash
repak get "path/to/Ancestors-WindowsNoEditor.pak" "Ancestors/Content/Prod/Data/GameSystems/Animals_AI/Leopard/VL01_CDSHealth_Leopard.uasset" > leopard.uasset
```

### 2. Modify a value
```python
import struct
with open('leopard.uasset', 'rb') as f:
    data = bytearray(f.read())

# HealthMax float at offset 1140 (original: 9.0)
struct.pack_into('<f', data, 1140, 1.0)  # One-hit kill!

with open('mod/Ancestors/Content/Prod/Data/GameSystems/Animals_AI/Leopard/VL01_CDSHealth_Leopard.uasset', 'wb') as f:
    f.write(data)
```

### 3. Pack and install
```bash
repak pack --version V5 --compression Zlib --mount-point "../../../" ./mod/ ./MyMod_P.pak
copy MyMod_P.pak "[Game]\Ancestors\Content\Paks\"
```

Launch the game. The leopard now has 1 HP.

---

## Game technical overview

| Property | Value |
|----------|-------|
| Engine | Unreal Engine 4.20 |
| Pak format | Version 5, Zlib compression |
| Encryption | **None** (no AES) |
| Audio | Wwise (Audiokinetic) |
| Physics | PhysX 3 |
| Debug symbols | **Yes** — 625 MB .pdb included with the game |
| Total assets | 18,105 files in main pak |

### Architecture

The game uses a **Component Data Set (CDS)** architecture where each gameplay aspect is a separate component:

```
CDSHealth          — Health points
CDSVitality        — Energy, stamina
CDSRegimen         — Hunger, thirst, sleep
CDSCombat          — Combat system
CDSNavigation      — Movement
CDSEmotional       — Fear, panic, calm
CDSTemperature     — Body temperature
CDSCrafting        — Item crafting
CDSEquipment       — Equipped items
...and 40+ more components
```

Each animal has its own set of CDS files that can be individually modified.

### Animal health values (vanilla)

| Animal | HealthMax | Offset | File |
|--------|-----------|--------|------|
| Elephant | 20.0 | 1144 | VL01_CDSHealth_Elephant.uasset |
| Crocodile | 12.0 | 1148 | VL01_CDSHealth_Crocodile.uasset |
| Buffalo | 10.0 | 1147 | VL01_CDSHealth_Buffalo.uasset |
| Hippo | 10.0 | 1132 | VL01_CDSHealth_Hippo.uasset |
| Rhino | 10.0 | 1152 | VL01_CDSHealth_WhiteRhino.uasset |
| Leopard | 9.0 | 1140 | VL01_CDSHealth_Leopard.uasset |
| Hyena | 6.0 | 1132 | VL01_CDSHealth_Hyena.uasset |
| Jackal | 6.0 | 1136 | VL01_CDSHealth_Jackal.uasset |
| Warthog | 6.0 | 1140 | VL01_CDSHealth_Warthog.uasset |
| Gazelle | 4.0 | 1140 | VL01_CDSHealth_Gazelle.uasset |
| Python | 4.0 | 1166 | VL01_CDSHealth_PythonCrawler.uasset |
| Giant Otter | 3.0 | 1152 | VL01_CDSHealth_GiantOtter.uasset |
| Zebra | 3.0 | 1132 | VL01_CDSHealth_Zebra.uasset |
| Scolopendra | 3.0 | 1165 | VL01_Scolopendra_CDSHealth.uasset |

### Player vitality values

| Parameter | Value | Offset | File |
|-----------|-------|--------|------|
| EnergyRegenPerSecond | 0.03 | 1524 | VL01_HumanAI_Shared_CDSVitality.uasset |
| HoursBeforeStarvation | 30.0 | 1968 | VL01_HumanAI_Shared_CDSRegimen.uasset |
| MinutesBeforeDeath (food) | 20.0 | 2026 | VL01_HumanAI_Shared_CDSRegimen.uasset |
| HoursBeforeSleepDeath | 16.0 | 2170 | VL01_HumanAI_Shared_CDSRegimen.uasset |
| MinutesBeforeDeath (sleep) | 20.0 | 2468 | VL01_HumanAI_Shared_CDSRegimen.uasset |

### Shared quadruped skeleton (77 bones)

All quadruped animals share `Quadruped_Skeleton.uasset` with 77 bones. This means new animals can reuse existing animations if rigged to the same skeleton.

### Evolution system

17 neural branches with 3 types of unlock conditions:
- `GameConditionDiscoverGameItem` — Discover a specific item
- `GameConditionCharacterMetric` — Eat/drink/interact X times
- `GameConditionPlayerCombat` — Fight specific animals

---

## What's possible (and what's not)

| Mod type | Feasibility | Method |
|----------|-------------|--------|
| Change animal stats | **Easy** | Binary float patching |
| Change player survival | **Easy** | Binary float patching |
| Texture reskin | **Medium** | FModel export → edit → UAssetAPI reimport |
| Weapon rebalance | **Medium** | UAssetAPI DataTable editing |
| Evolution tree tweaks | **Medium** | UAssetAPI Blueprint editing |
| New animals | **Hard** | Blender + UE4 editor + CDS creation |
| Map modifications | **Hard** | Complex level streaming system |
| New game mechanics | **Very Hard** | DLL injection + Ghidra RE |

---

## Tools you'll need

| Tool | Role | Link |
|------|------|------|
| **repak** | Pack/unpack .pak files | [GitHub](https://github.com/trumank/repak) |
| **FModel** | Browse assets, export textures | [fmodel.app](https://fmodel.app) |
| **UModel** | Extract 3D models and animations | [gildor.org](https://www.gildor.org/en/projects/umodel) |
| **UAssetAPI/UAssetGUI** | Edit .uasset files properly | [GitHub](https://github.com/atenfyr/UAssetAPI) |
| **Ghidra** | Decompile the game binary (with .pdb) | [GitHub](https://github.com/NationalSecurityAgency/ghidra) |
| **Blender** + PSK addon | Import/edit 3D models | [Addon](https://github.com/matyalatte/Blender3D-Import-PSK-PSA) |

---

## Important notes

- This project is for **personal and educational use**
- **Never redistribute original game assets** — only patches and tools
- The game includes a .pdb debug symbols file (625 MB) which is rare and invaluable for reverse engineering
- The pak files are **not encrypted** — no AES key needed
- The game was built with UE4.20 (confirmed by Ancestors.uproject)
- The studio (Panache Digital Games) used Perforce for version control

---

## Contributing — We need you!

This is a community project. The technical pipeline is ready — now we need talented people to help bring this game back to life.

### What we're looking for

| Role | What you'd do | Skills needed |
|------|--------------|---------------|
| **3D Artists** | Create new prehistoric animals using the shared 77-bone skeleton | Blender, modeling, rigging |
| **Texture Artists** | Create animal skins, environment textures | Texturing, Substance Painter, GIMP |
| **Animators** | New animations for animals and hominids | Blender animation |
| **Researchers** | Document more game systems, find new moddable values | Curiosity, hex editors |
| **Tool Developers** | Build new modding tools, improve existing ones | Python, C#, Rust |
| **Writers** | Improve documentation, write tutorials | Clear writing |

### How to contribute

- Open an issue to discuss your findings or ideas
- Submit a PR with documentation, tools, or assets
- Share your mods with the community
- Just star the repo to show support!

---

## License

MIT License — see [LICENSE](LICENSE)

Tools and documentation only. No game assets are included in this repository.

---

**Created by DaddyOurs**
*Because this game deserved a modding community.*
