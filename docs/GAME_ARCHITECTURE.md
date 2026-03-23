# Architecture technique du jeu — Decouvertes Phase 1

> Genere le 2026-03-22 — Analyse des assets extraits
> Statut : Phase 1-2 completees
> Version moteur : **UE4.20** (confirme par Ancestors.uproject: "ANCESTORS_LIVE_4.20")

---

## Vue d'ensemble de l'architecture

Le jeu utilise une architecture **hybride** :
- **C++ natif** (`/Script/PanacheGame`, `/Script/Ancestors`) pour le moteur de jeu
- **Blueprints** pour la logique specifique des animaux, items, et systemes
- **DataTables** pour les donnees tabulaires (armes, placement d'objets)
- **Custom Data Structs** (CDS) pour les parametres de chaque animal

### Modules identifies

| Module | Chemin script | Role |
|--------|--------------|------|
| `PanacheGame` | `/Script/PanacheGame` | Framework du studio — classes de base (CDSHealth, EvolutionNodeGroup, etc.) |
| `Ancestors` | `/Script/Ancestors` | Code specifique au jeu |
| `CoreUObject` | `/Script/CoreUObject` | Classes UE4 de base |
| `Engine` | `/Script/Engine` | Moteur UE4 |
| `AkAudio` | `/Script/AkAudio` | Integration Wwise |

---

## Systeme de sante des animaux (CDSHealth)

### Qu'est-ce que "CDS" ?

CDS = **Custom Data Set** (ou Component Data Set). C'est un pattern du framework
PanacheGame : chaque aspect d'un animal (sante, navigation, communication, perception)
est separe dans son propre fichier Blueprint qui herite d'une classe C++ de base.

### Fichiers CDSHealth par animal

Chaque animal a son propre fichier `VL01_CDSHealth_[Animal].uasset`.
Ce sont des **BlueprintGeneratedClass** qui heritent de `CDSHealth`.
Ils contiennent au minimum une propriete `HealthMax` (FloatProperty).

### Valeurs de sante decouvertes

| Animal | HealthMax | Tier |
|--------|-----------|------|
| Elephant | 20.0 | Boss |
| Crocodile | 12.0 | Tank |
| African Buffalo | 10.0 | Costaud |
| Hippo | 10.0 | Costaud |
| White Rhino | 10.0 | Costaud |
| Leopard | 9.0 | Predateur fort |
| Hyena | 6.0 | Predateur moyen |
| Jackal | 6.0 | Predateur moyen |
| Warthog | 6.0 | Moyen |
| Gazelle | 4.0 | Proie |
| Python | 4.0 | Crawler |
| Giant Otter | 3.0 | Petit |
| Zebra | 3.0 | Proie |
| Scolopendra | 3.0 | Insecte |

**Observation** : le systeme de sante utilise une echelle reduite (3-20),
pas des centaines de HP. Une valeur de `-8.0` est presente dans tous les
fichiers — probablement un seuil de regeneration ou un parametre de base.

### Autres fichiers CDS par animal

Chaque animal a aussi :
- `VL01_CDSNavigation_[Animal].uasset` — parametres de deplacement
- `VL01_CDSCommunicate_[Animal].uasset` — sons, communication
- `VL01_Perception_[Animal].uasset` — rayon de detection, sens
- `VL01_ReactionHandler_[Animal].uasset` — reactions aux stimuli

---

## Systeme d'armes (DataTable)

Le fichier `CH1_GID_Weapons.uasset` est un **DataTable** (type `GameItemDataWeapons`).

### Structure d'une ligne du DataTable

| Propriete | Type | Description |
|-----------|------|-------------|
| WeaponType | EWeaponType | Rock, Stick, ou Unarmed |
| InjuryMesh | SoftObjectProperty | Reference au mesh de blessure |
| SocketsGroup | ? | Groupe de sockets pour l'attachement |

### Armes du jeu

**Type Rock (pierres)** :
Basalt, BlueAgate, Chopper, Granite, Granite_Grinder, Meteorite,
Obsidian, Powerstone, Ruby, Scraper, Sphalerite, Tourmaline

**Type Stick (batons)** :
BoneClub, DeadBranch, DeadStick, SharpStick, Stick

**Type Unarmed** :
Unarmed (mains nues)

---

## Systeme d'evolution (EvolutionNodeGroup + EvolutionData)

### Architecture

L'evolution est structuree en deux couches :

1. **VL01_EvolutionData.uasset** (89 Ko) — DataTable principal contenant
   les references a tous les noeuds d'evolution, leurs items associes,
   niveaux de difficulte, et categories.

2. **EVO_VL01_[XX][NN].uasset** — Blueprints individuels par branche/groupe
   d'evolution (heritent de `EvolutionNodeGroup`).

### Branches d'evolution

| Code | Signification probable | Nombre de noeuds |
|------|----------------------|------------------|
| BU | Build (Construction) | 3 |
| CR | Crafting | 4 |
| DI | Dexterity/Intelligence | ~40+ |
| DO | Dodge/Domination | ~18 |
| FE | Fear (Peur) | 4 |
| FO | Food (Nourriture) | 9 |
| HE | Health (Sante) | 5 |
| IA | Interpersonal/Awareness | 6 |
| IF | Intelligence/Fabrication | ~50+ |
| IN | Intimidation | ~14 |
| KI | Kinesthesia | ~20 |
| ME | Memory (Memoire) | 9 |
| PS | Physical Strength | 4 |
| RE | Reflexes | 5 |
| RF | Reflexes Fine | 10 |
| SE | Senses (Sens) | 6 |
| US | Use (Utilisation outils) | ~14 |

### Proprietes d'un noeud d'evolution

- `Nodes` (ArrayProperty) — sous-noeuds du groupe
- `CompletionCondition` — condition de completion
- `CompletionEvaluator` — evaluateur de completion
- `GameConditionDiscoverGameItem` — se debloque en decouvrant un item
- `GameItemName` — nom de l'item requis
- `MustLockForCustomGameSpeciesData` — verrouillage d'espece
- `NodeName` — nom du noeud
- `EGameNodeGroupConcurrentEvaluatorRule` — regle de concurrence

### Types de conditions par branche

| Branche | Classe de condition | Parametres | Exemple |
|---------|-------------------|-----------|---------|
| DI (Dexterity) | `GameConditionDiscoverGameItem` | GameItemName | Decouvrir un item specifique |
| FO (Food) | `GameConditionCharacterMetric` | Metric, Threshold, MonitorMode, Unit | Manger X portions d'un type |
| KI (Kinesthesia) | `GameConditionPlayerCombat` | AttackerDescriptorName, Outcomes, States | Combattre certains animaux |

#### Metriques de nourriture (FO01)

`ECharacterMetric::BerryConsumed`, `CotyledonFoodConsumed`, `DrupeFoodConsumed`,
`EggConsumed_NotPoisoned`, `InsectConsumed`, `MammalFoodConsumed_NotPoisoned`,
`MolluskConsumed`, `MushroomConsumed_NotPoisoned`, `OviparousFoodConsumed_NotPoisoned`,
`RootConsumed`, `VegetalConsumed`

**Observation** : les Threshold sont tous a 1.0 — chaque noeud se debloque en
mangeant une seule portion. L'evolution est basee sur la decouverte, pas la repetition.

### Niveaux de difficulte

```
EEvolutionLevel::Easy
EEvolutionLevel::Medium
EEvolutionLevel::Hard
```

---

## Items et FoodDispensers

### Structure d'un FoodDispenser (ex: ANC_Coconut_Seed)

Les items sont des **Blueprints** (BlueprintGeneratedClass) heritant d'Actor.
Ils sont composes de composants :

| Composant | Role |
|-----------|------|
| `StaticMeshComponent` | Mesh visuel de l'objet |
| `InteractionComponent` (LeanInteractionComponent) | Gestion des interactions joueur |
| `SenseStimulisComponent` (LeanStimulusComponent) | Detection sensorielle |
| `VisualChangerComponent` (LeanVisualChangerComponent) | Changements visuels |
| `GameItemDescriptor` (LeanGameItemDescriptor) | Donnees de gameplay |
| `ConstructionSpaceVolume` | Volume de construction |

### References par item

Chaque item reference :
- Un **mesh** (StaticMesh ou SkeletalMesh)
- Un **evenement audio Wwise** (ex: `Play_FOL_Handling_Hard`)
- Un **systeme de particules** (VFX)
- Des **parametres physiques** (masse, damping, collision)

---

## Structure d'un animal complet

En prenant le Crocodile comme reference, un animal est compose de :

### Assets visuels (Character/Animal/Crocodile/)
```
Mesh/
  Crocodylus_Skelmesh.uasset          ← Modele 3D + squelette
  Crocodylus_PhysicsAsset.uasset      ← Collision physique

Textures/
  Crocodylus_02_D.uasset              ← Diffuse (couleur)
  Crocodylus_02_R.uasset              ← Roughness
  Crocodylus_N.uasset                 ← Normal map
  Crocodylus_02_Blood_D.uasset        ← Texture sang
  Crocodylus_Eyes_D.uasset            ← Yeux

Material/
  M_Crocodylus_MIC.uasset             ← Material Instance (corps)
  M_Crocodylus_Eyes_MIC.uasset        ← Material Instance (yeux)
  M_Crocodylus_Blood_MIC.uasset       ← Material Instance (sang)

Anim/
  Loco/Idle/   ← 10 animations d'idle (normal, threatening, turns)
  Loco/Move/   ← 16 animations de deplacement (sol + nage)
  Atk/         ← 4 animations d'attaque
  Combat/      ← Animations de combat (countered, ending)
  Resist/      ← Animation de resistance
```

### Assets de gameplay (GameSystems/Animals_AI/Crocodile/)
```
BP_CrocodileQuadAIController.uasset   ← Controleur IA principal
BP_Crocodile_Schedule.uasset          ← Planning journalier
BP_Crocodile_AttitudeKit.uasset       ← Kit d'attitudes
BP_Formation_Crocodile.uasset         ← Comportement de groupe
BP_CrocodileGroundMetrics.uasset      ← Metriques au sol
BP_CrocodileSurfaceSwimMetrics.uasset ← Metriques de nage
BP_Crocodile_LookatMetrics.uasset     ← Metriques de regard
BP_PredatorPack_Crocodile_Single.uasset ← Pack predateur (solitaire)

Attitudes/
  BP_Crocodile_Attitude_Normal.uasset
  BP_Crocodile_Attitude_Aggressive.uasset
  BP_Crocodile_Attitude_Stealth.uasset
  BP_Crocodile_Attitude_Wounded.uasset

VL01_CDSHealth_Crocodile.uasset       ← Sante (HealthMax = 12.0)
VL01_CDSNavigation_Crocodile.uasset   ← Deplacement
VL01_CDSCommunicate_Crocodile.uasset  ← Communication
VL01_Perception_Crocodile.uasset      ← Perception
VL01_ReactionHandler_Crocodile.uasset ← Reactions
VL01E01_Crocodile_HomoAttackKit.uasset ← Kit d'attaque vs joueur
```

### Assets contextuels
```
Dead/Crocodile/       ← Cadavre (4 etats de decomposition + textures)
Nests/Crocodile/      ← Nid + oeufs (meshes, textures, materials)
FoodDispensers/       ← Items liees (oeufs, carcasses)
Audio/                ← Evenements sonores (combats inter-animaux)
CustomAnimSets/       ← Animations contextuelles (repos, sommeil)
```

---

## Conclusions pour le modding

### Ce qui est modifiable facilement (Phase 2)

1. **Stats de sante** — Modifier le float HealthMax dans les CDSHealth
2. **Textures** — Remplacer les textures _D, _N, _R
3. **DataTable d'armes** — Ajouter/modifier des armes
4. **Sons** — Remplacer les .wem Wwise

### Ce qui est modifiable avec effort (Phase 3)

1. **Noeuds d'evolution** — Les Blueprints EVO sont individuels et structurés
2. **IA des animaux** — Les attitudes et comportements sont en Blueprints separés
3. **Meshes 3D** — Le squelette partage `Quadruped_Skeleton` facilite les ajouts
4. **Items/FoodDispensers** — Structure Blueprint documentée

### Ce qui reste complexe (Phase 4)

1. **Logique de spawn** — Pas encore identifie comment les animaux sont places dans le monde
2. **Nouvelles branches d'evolution** — Necessite de comprendre comment `VL01_EvolutionData` reference les groupes
3. **Nouvelles maps** — 440 .umap a comprendre

### Architecture du projet (depuis Ancestors.uproject)

Le projet est compose de 4 modules C++ :

| Module | Type | Phase chargement | Dependances |
|--------|------|------------------|-------------|
| **Ancestors** | Runtime | Default | Engine, AIModule, CoreUObject, PanacheGame, UMG, PanacheEngine |
| **AncestorsEditor** | Editor | Default | AudiokineticTools |
| **PanacheEngine** | Runtime | PreDefault | Engine |
| **PanacheGame** | Runtime | PreDefault | Engine, CoreUObject, AIModule, PanacheEngine, AkAudio, UMG |

Plugins actifs : `PanacheAnalytics`, `AncestorsShaders`, `GamepadUMGPlugin`, `WinDualShock`
Chemin Perforce du studio : `d:\p4\upload_ancestors_steam\game\`

### Decouverte bonus : fichier .pdb (625 Mo !)

Le fichier `Ancestors-Win64-Shipping.pdb` (symboles de debug) est present.
C'est **extremement rare** pour un jeu commercial distribue. 625 Mo de symboles !

#### Classes C++ decouvertes via le PDB

**Systemes principaux :**

| Classe/Systeme | Occurrences PDB | Description |
|----------------|----------------|-------------|
| `ClanMember` | 40 570 | Systeme de clan (le plus gros systeme du jeu) |
| `Settlement` | 9 599 | Campements |
| `LevelStreaming` | 6 277 | Streaming de niveaux (chargement du monde) |
| `Intimidation` | 3 969 | Systeme d'intimidation |
| `Generation` | 3 676 | Generations (changement de generation) |
| `PanacheGame` | 3 585 | Framework du studio |
| `Neuron` | 3 118 | Systeme neuronal (arbre d'evolution) |
| `FearZone` | 1 865 | Zones de peur |
| `EvolutionNode` | 954 | Noeuds d'evolution |
| `FoodDispenser` | 415 | Distributeurs de nourriture |
| `CDSHealth` | 388 | Systeme de sante |
| `WeaponDamage` | 231 | Degats des armes |

**Classes specifiques :**
- `UCDSHealth` — sante des entites
- `UQuadrupedCharacterService` — service des quadrupedes
- `UPredatorAttackEvent` — evenements d'attaque
- `FEvolutionSpeciesInfo` — infos especes
- `FGameItemDataWeaponDamage` — donnees de degats d'armes
- `NeuronalEnergySource` / `NeuronalEnergyBooster` — sources d'energie neuronale
- `HEClanMemberNaming` — nommage des membres du clan
- `GCSIntimidation` — systeme d'intimidation de groupe
- `EnterFearZone` / `ExitFearZone` — entree/sortie de zones de peur
- `PlayerSettlement` / `ConditionSettlement` — systeme de campement
- `GetGainedNeuralEnergy` / `CanGainNeuronalEnergy` / `HasUnlimitedNeuronalEnergyGain` — fonctions cles

**Fichiers source identifies (.gen.cpp = Blueprints compiles) :**
- `EvolutionNodeGroup.gen.cpp`
- `NeuronalEnergySource.gen.cpp`
- `NeuronalEnergyBooster.gen.cpp`
- `IntimidationTypes.gen.cpp`
- `GCSIntimidation.gen.cpp`
- `HEClanMemberNaming.gen.cpp`
- `PlayerSettlement.gen.cpp`

Le PDB permettra (Phase 4) :
- De nommer les fonctions dans Ghidra/IDA
- De comprendre les classes C++ du framework PanacheGame
- De mapper les structures memoire pour Cheat Engine
- D'identifier les points d'injection pour les hooks DLL
