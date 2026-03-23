# Evolution System — Complete Guide

> How the neural evolution tree works internally, and how to modify it.

---

## Overview

The evolution system is the core progression mechanic. Players unlock "neurons" by performing actions (eating, crafting, fighting, exploring). Each neuron grants a permanent ability or stat boost.

Internally, it's a **hybrid system**:
- A central **DataTable** (`VL01_EvolutionData.uasset`, 89 KB) references all nodes
- Individual **Blueprints** per node group (`EVO_VL01_XX##.uasset`)
- A **tracker** system that monitors player actions

---

## Architecture

```
VL01_EvolutionData.uasset          ← Master data table (all nodes + metadata)
│
├── EVO_VL01_DI01.uasset           ← Node group "Dexterity 01"
│   ├── Node DI01_01               ← Individual neuron
│   ├── Node DI01_02
│   └── ...
├── EVO_VL01_FO01.uasset           ← Node group "Food 01"
│   ├── Node FO01_01
│   └── ...
└── ...

SYS_GIC_EvolutionTracker.uasset    ← Tracks player progress
VL01_FulfillmentData.uasset        ← Completion requirements
```

---

## The 17 neural branches

| Code | Branch (probable) | Nodes | Condition type |
|------|-------------------|-------|---------------|
| **BU** | Build/Construction | 3 | DiscoverGameItem |
| **CR** | Crafting | 4 | DiscoverGameItem |
| **DI** | Dexterity/Intelligence | ~40+ | DiscoverGameItem |
| **DO** | Dodge/Domination | ~18 | PlayerCombat |
| **FE** | Fear | 4 | CharacterMetric |
| **FO** | Food/Foraging | 9 | CharacterMetric |
| **HE** | Health/Healing | 5 | CharacterMetric |
| **IA** | Interpersonal/Awareness | 6 | DiscoverGameItem |
| **IF** | Intelligence/Fabrication | ~50+ | DiscoverGameItem |
| **IN** | Intimidation | ~14 | PlayerCombat |
| **KI** | Kinesthesia | ~20 | PlayerCombat |
| **ME** | Memory | 9 | CharacterMetric |
| **PS** | Physical Strength | 4 | CharacterMetric |
| **RE** | Reflexes | 5 | PlayerCombat |
| **RF** | Reflexes Fine | 10 | PlayerCombat |
| **SE** | Senses | 6 | CharacterMetric |
| **US** | Use (tool use) | ~14 | DiscoverGameItem |

---

## Condition types

Each neuron has an unlock condition. Three types exist:

### 1. GameConditionDiscoverGameItem
**Used by:** DI, CR, BU, IA, IF, US branches
**How it works:** Unlock by discovering (interacting with) a specific game item for the first time.
**Parameters:** `GameItemName` — the item to discover.

Example items referenced: `Basalt`, `Granite`, `Chopper`, `Scraper`, `DeadBranch`, `Honey`, `Kapok_Fiber`, `AloeResin_Grinded`, `Obsidian`

### 2. GameConditionCharacterMetric
**Used by:** FO, FE, HE, ME, PS, SE branches
**How it works:** Unlock by reaching a threshold on a character metric (eating, drinking, etc.)
**Parameters:**
- `Metric` — Which metric to track (ECharacterMetric enum)
- `Threshold` — How many times (float, usually 1.0)
- `MonitorMode` — When to start counting (EMetricMonitorMode::FromActivation)
- `Unit` — Unit of measurement (EMetricUnit::Unit)

**Known metrics (FO01 branch):**
| Metric | Meaning |
|--------|---------|
| BerryConsumed | Ate a berry |
| CotyledonFoodConsumed | Ate a cotyledon |
| DrupeFoodConsumed | Ate a drupe (stone fruit) |
| EggConsumed_NotPoisoned | Ate an egg without getting poisoned |
| InsectConsumed | Ate an insect |
| MammalFoodConsumed_NotPoisoned | Ate mammal meat safely |
| MolluskConsumed | Ate a mollusk |
| MushroomConsumed_NotPoisoned | Ate a mushroom safely |
| OviparousFoodConsumed_NotPoisoned | Ate reptile/bird meat safely |
| RootConsumed | Ate a root |
| VegetalConsumed | Ate a vegetable |

**Important discovery:** All food thresholds are set to **1.0** — you only need to eat one of each type. The evolution system rewards **discovery**, not repetition.

### 3. GameConditionPlayerCombat
**Used by:** DO, IN, KI, RE, RF branches
**How it works:** Unlock by fighting specific animals.
**Parameters:**
- `AttackerDescriptorName` — Which animal to fight
- `Outcomes` — Required combat outcome
- `States` — Combat states to achieve

**Animals referenced in KI01:**
- Predator_GiantOtter
- Predator_Hippo
- Predator_Warthog
- Predator_WhiteRhino
- Quadruped_AfricanBuffalo
- Quadruped_Elephant

---

## Difficulty levels

Each neuron has a difficulty rating:

```
EEvolutionLevel::Easy
EEvolutionLevel::Medium
EEvolutionLevel::Hard
```

This affects the visual display in the evolution menu (the "RPG menu" internally).

---

## Node group structure (Blueprint)

Each `EVO_VL01_XX##.uasset` is a `BlueprintGeneratedClass` inheriting from `EvolutionNodeGroup`. Structure:

```
EvolutionNodeGroup
├── Nodes (ArrayProperty)          ← List of sub-nodes
├── CompletionCondition            ← When is the group complete
├── CompletionEvaluator            ← How to evaluate completion
├── Rule (EGameNodeGroupConcurrentEvaluatorRule)
│   └── Usually "Never" (nodes aren't concurrent)
└── Per-node data:
    ├── NodeName (NameProperty)    ← e.g., "EVO_VL01_DI01_01"
    ├── Condition (ObjectProperty) ← Reference to condition class
    └── GameItemName / Metric / AttackerDescriptorName
```

---

## Evolution data table (VL01_EvolutionData)

The master DataTable (89 KB) contains entries for every neuron in the game. Each row has:

| Field | Type | Description |
|-------|------|-------------|
| Node ID | FName | e.g., "EVO_VL01_DI01_01" |
| GameItemName | FName | Item required to unlock |
| OtherItemName | FName | Secondary item (optional) |
| Level | EEvolutionLevel | Easy/Medium/Hard |
| Description | ? | Text description |

Referenced categories in the DataTable:
- `Category_Berry`, `Category_Carcass`, `Category_Cotyledon`
- `Category_Drupe`, `Category_Egg`, `Category_Eumycota`
- `Category_FishingStation`, `Category_Insect`, `Category_Leopard`
- `Category_Mammal`, `Category_Mollusca`, `Category_Oviparous`
- `Category_Root`, `Category_Vegetal`

Referenced items: `Basalt`, `Granite`, `Obsidian`, `Chopper`, `Scraper`, `DeadBranch`, `DeadStick`, `SharpStick`, `BedTwoPlaces`, `BranchWall`, `Beehive`, `Fern`, `Honey`, `LiftableRock`, `PokableHole`, etc.

---

## Modding possibilities

### What you CAN change (with UAssetAPI)
- **Threshold values** — Make neurons require more/fewer actions to unlock
- **Difficulty levels** — Change Easy/Medium/Hard ratings
- **Item references** — Change which item unlocks which neuron (by changing FName references)

### What you CANNOT change easily
- **Add entirely new branches** — Requires new Blueprint assets + registration in the tracker
- **Change condition types** — Switching from DiscoverItem to CharacterMetric requires Blueprint restructuring
- **Add new metrics** — ECharacterMetric is a C++ enum, not extendable via assets

### Recommended approach
1. Use **UAssetGUI** to open `VL01_EvolutionData.uasset`
2. Browse the DataTable rows to understand the full structure
3. Modify values (thresholds, difficulty levels)
4. Export via UAssetAPI, repack with repak

---

## Related files

```
Ancestors/Content/Prod/Data/GameSystems/Evolution/
├── EVO_VL01.uasset                    ← Main evolution asset
├── EVO_VL01_Template.uasset           ← Base template for node groups
├── EVO_VL01_[XX][##].uasset           ← Node groups (17 branches)
├── VL01_EvolutionData.uasset          ← Master DataTable (89 KB)
├── VL01_FulfillmentData.uasset        ← Completion data
└── SYS_GIC_EvolutionTracker.uasset    ← Progress tracker

Ancestors/Content/Prod/Data/UI/Menu/InGameMenu/RPG_menu/
├── BP_EvolutionMenu.uasset            ← Evolution menu UI
├── BP_EvolutionGroupItem.uasset       ← Group UI widget
└── BP_EvolutionItem.uasset            ← Individual neuron UI widget

C++ classes (from PDB):
├── EvolutionNode.gen.cpp
├── EvolutionNodeAction.gen.cpp
├── EvolutionNodeCondition.gen.cpp
├── EvolutionNodeData.gen.cpp
├── EvolutionNodeGroup.gen.cpp
├── EvolutionTracker.gen.cpp
├── RPGNode.gen.cpp
├── RPGNodeGroup.gen.cpp
└── RPGTracker.gen.cpp
```
