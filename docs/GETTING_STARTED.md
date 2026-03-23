# Getting Started — Your First Ancestors Mod

> From zero to a working mod in 15 minutes.
> No prior modding experience needed.

---

## How Ancestors modding works

Ancestors runs on **Unreal Engine 4.20**. All game data (models, textures, sounds, gameplay data) is packed inside `.pak` files in the `Content/Paks/` folder.

UE4 has a built-in **patch system**: if you place a file named `Something_P.pak` in the same folder, the engine loads it *after* the base game and **overrides** any matching files. Your original game files are never touched.

```
Content/Paks/
├── Ancestors-WindowsNoEditor.pak    ← Base game (3.75 GB, 18,105 files)
├── VL01E01.pak                      ← Game content duplicate
└── YourMod_P.pak                    ← YOUR MOD (overrides matching files)
```

This means modding Ancestors is a 3-step process:
1. **Extract** a file from the base .pak
2. **Modify** the values you want to change
3. **Repack** into a new `_P.pak` and drop it in the folder

---

## Prerequisites

### Required
- **Python 3.10+** — [Download](https://www.python.org/downloads/) (check "Add to PATH")
- **repak** — [Download](https://github.com/trumank/repak/releases) (grab the Windows .zip, extract `repak.exe`)

### Recommended
- **FModel** — [Download](https://fmodel.app) — Visual asset browser
- **UAssetGUI** — [Download](https://github.com/atenfyr/UAssetGUI/releases) — Edit .uasset files with a GUI
- **HxD** — [Download](https://mh-nexus.de/en/hxd/) — Hex editor for inspecting files

### For 3D work
- **UModel** — [Download](https://www.gildor.org/en/projects/umodel) — Extract 3D models
- **Blender** + [PSK/PSA addon](https://github.com/matyalatte/Blender3D-Import-PSK-PSA) — Edit models

---

## Step 1 — Set up your workspace

Create a folder for your modding work:

```
C:\AncestorsModding\
├── repak.exe            ← The pak tool
├── extracted\           ← Where you'll put extracted files
└── my_mod\              ← Where you'll build your mod
```

Find your game installation:
```
C:\Program Files (x86)\Steam\steamapps\common\Ancestors The Humankind Odyssey\
```

You can find it via Steam: right-click the game → Manage → Browse local files.

---

## Step 2 — Explore the game data

### List what's inside the pak

```bash
repak.exe list "C:\...\Ancestors\Content\Paks\Ancestors-WindowsNoEditor.pak"
```

This outputs all 18,105 file paths. Pipe it to a file to browse:

```bash
repak.exe list "...\Ancestors-WindowsNoEditor.pak" > all_files.txt
```

### Understand the folder structure

```
Ancestors/Content/
├── Prod/Data/
│   ├── GameSystems/           ← Gameplay logic (AI, evolution, items)
│   │   ├── Animals_AI/        ← Per-animal AI, health, behavior
│   │   ├── Evolution/         ← Neural evolution tree
│   │   ├── GameItems/         ← Item definitions
│   │   └── FoodDispensers/    ← Food item definitions
│   ├── Art/                   ← Environment art (rocks, trees, etc.)
│   └── UI/                    ← User interface
├── Character/
│   ├── Animal/                ← Animal models, textures, animations
│   └── Humanoid/              ← Hominid models
└── Cinematic/                 ← Cutscenes
```

### Extract a single file

```bash
repak.exe get "...\Ancestors-WindowsNoEditor.pak" "Ancestors/Content/Prod/Data/GameSystems/Animals_AI/Leopard/VL01_CDSHealth_Leopard.uasset" > leopard_health.uasset
```

---

## Step 3 — Your first mod: change an animal's health

The simplest mod: make the leopard weaker (or stronger).

### Find the value

Each animal's health is stored as a **float** (decimal number) in a `.uasset` file. The leopard has `HealthMax = 9.0` stored at byte offset `1140`.

### Modify it

Create a Python script `my_first_mod.py`:

```python
import struct

# Read the original file
with open('leopard_health.uasset', 'rb') as f:
    data = bytearray(f.read())

# Check current value
old = struct.unpack_from('<f', data, 1140)[0]
print(f"Current health: {old}")  # Should print 9.0

# Change to new value
struct.pack_into('<f', data, 1140, 1.0)  # 1 HP = one-hit kill

# Save (keeping the EXACT same file size!)
import os
os.makedirs('my_mod/Ancestors/Content/Prod/Data/GameSystems/Animals_AI/Leopard', exist_ok=True)
with open('my_mod/Ancestors/Content/Prod/Data/GameSystems/Animals_AI/Leopard/VL01_CDSHealth_Leopard.uasset', 'wb') as f:
    f.write(data)

print("Done! File saved.")
```

Run it: `python my_first_mod.py`

### Pack it

```bash
repak.exe pack --version V5 --compression Zlib --mount-point "../../../" my_mod/ MyFirstMod_P.pak
```

### Install it

Copy `MyFirstMod_P.pak` to `[Game]\Ancestors\Content\Paks\`

### Test it

Launch the game, find a leopard, and enjoy your one-hit kill!

### Uninstall it

Delete `MyFirstMod_P.pak` from the Paks folder. That's it.

---

## Step 4 — Understanding .uasset files

A `.uasset` is a binary file with this structure:

```
┌─────────────────────────┐
│  Header                 │  ← Magic number, version, package info
├─────────────────────────┤
│  Name Table             │  ← All string names used in the file
├─────────────────────────┤
│  Import Table           │  ← References to external assets/classes
├─────────────────────────┤
│  Export Table           │  ← Objects defined in this file
├─────────────────────────┤
│  Serialized Data        │  ← The actual values (this is what we modify)
└─────────────────────────┘
```

For simple float/int modifications, you only need to change bytes in the **Serialized Data** section. The header and tables stay untouched.

**Golden rule: NEVER change the file size.** Adding or removing bytes breaks all internal offsets.

---

## Step 5 — What else can you modify?

### Easy (binary patching)
- Animal health, speed, perception
- Player energy regeneration
- Hunger/thirst/sleep timers
- Any float or int property in a BlueprintGeneratedClass

### Medium (requires UAssetAPI)
- DataTable entries (weapons, items)
- Blueprint properties
- Evolution node conditions

### Hard (requires UE4 editor or DLL injection)
- Textures (need proper DXT encoding)
- New assets
- Game logic changes

See [MODDING_PIPELINE.md](MODDING_PIPELINE.md) for the full guide on each method.

---

## Common mistakes

| Mistake | Result | Fix |
|---------|--------|-----|
| Changed file size | Crash on load | Always keep exact same byte count |
| Wrong pak version | Game ignores the mod | Use `--version V5 --compression Zlib` |
| Wrong mount point | Files don't override | Use `--mount-point "../../../"` |
| Missing `_P` suffix | Game ignores the pak | Name must end with `_P.pak` |
| Modified texture bytes blindly | Crash | Use FModel/UAssetAPI for textures |
| Edited during gameplay | No effect | Close game, apply mod, relaunch |

---

## Next steps

- Read [ANIMAL_DATABASE.md](ANIMAL_DATABASE.md) for all animal stats and file locations
- Read [GAME_ARCHITECTURE.md](GAME_ARCHITECTURE.md) for the full technical breakdown
- Read [PDB_ANALYSIS.md](PDB_ANALYSIS.md) for C++ class documentation
- Try the [Difficulty Mod Manager](../tools/AncestorsDifficultyMod.py) for a GUI experience
- Join the modding discussion on Nexus Mods!
