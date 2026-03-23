# Asset Map — Ancestors: The Humankind Odyssey

> Genere le 2026-03-22 — Phase 1 Exploration
> Source : `Ancestors-WindowsNoEditor.pak` (18 105 fichiers, 3.75 Go)
> Outil : repak v0.2.3

---

## Informations techniques du .pak

| Propriete | Valeur |
|-----------|--------|
| Pak Version | V5 (RelativeChunkOffsets) — UE4.21-4.22 |
| Mount Point | `../../../` |
| Compression | Zlib |
| Chiffrement | **NON** (ni index, ni contenu) |
| Fichiers | 18 105 |

### Second .pak : VL01E01.pak

| Propriete | Valeur |
|-----------|--------|
| Taille | 2.98 Go |
| Fichiers | 14 610 |
| Meme version/compression | Oui |
| Note | Probablement le contenu du Volume 01 Episode 01 (le jeu) |

---

## Types de fichiers

| Extension | Nombre | Description |
|-----------|--------|-------------|
| `.uasset` | 14 142 | Assets UE4 (meshes, textures, blueprints, datatables, materials...) |
| `.res` | 2 680 | Fichiers de ressources (probablement Wwise ou custom) |
| `.umap` | 440 | Maps/Levels UE4 |
| `.wem` | 389 | Audio Wwise Encoded Media |
| `.png` | 227 | Images (UI, icones) |
| `.locres` | 43 | Localisations (traductions) |
| `.uplugin` | 42 | Descripteurs de plugins UE4 |
| `.ufont` | 24 | Polices |
| `.ini` | 21 | Configuration |
| `.json` | 13 | Donnees JSON |
| `.bnk` | 11 | Banques audio Wwise |
| `.ttf` | 13 | Polices TrueType |

---

## Structure des dossiers (Ancestors/Content/)

### Vue d'ensemble — 14 346 fichiers

```
Ancestors/Content/
├── Prod/                          9 110 fichiers — COEUR DU JEU
│   ├── Data/                      7 103
│   │   ├── Art/                   2 444  (modeles, textures, vegetation, rochers)
│   │   ├── UI/                    2 406  (interface utilisateur)
│   │   ├── GameSystems/             705  (IA animaux, evolution, items, progression)
│   │   ├── Audio/                   678  (evenements audio Wwise)
│   │   ├── VFX/                     500  (effets visuels)
│   │   ├── Materials/               112  (materiaux)
│   │   ├── CustomAnimSets/          111  (animations custom)
│   │   ├── LD/                       78  (Level Design)
│   │   ├── TimeOfDay/                45  (cycle jour/nuit)
│   │   ├── PostProcess/               9  (effets post-process)
│   │   ├── LUT/                       8  (color grading)
│   │   └── BlueprintLibrary/          7  (bibliotheques de fonctions BP)
│   └── Maps/                      2 007  (niveaux du monde)
│
├── Character/                     4 310 fichiers — PERSONNAGES & ANIMAUX
│   ├── Camera/                    1 642  (cameras)
│   ├── Humanoid/                  1 247  (hominides jouables)
│   ├── Animal/                    1 069  (faune)
│   ├── Dead/                        351  (modeles morts/cadavres)
│   └── Behavior/                      1
│
├── Cinematic/                       736  (cinematiques)
├── GUI/                              82  (widgets UI)
├── Marketplace/                      51  (assets UE Marketplace)
├── Localization/                     15  (traductions)
├── BaseMeshes/                        8
├── INTROPANACHE/                      6  (intro studio)
└── (autres petits dossiers)
```

---

## Animaux — Structure detaillee

### Character/Animal/ — 1 069 fichiers

Chaque espece a son propre dossier avec meshes, textures, animations :

| Espece | Fichiers | Notes |
|--------|----------|-------|
| Bird (Oiseaux) | 123 | Crane, EagleBateleur, Parrot, Pelagornis, Seagull, VultureCinereous |
| Feline | 103 | Leopard principalement |
| Insect | 101 | Scolopendra (mille-pattes geant), autres |
| Bovid | 95 | Buffles, gazelles |
| Snake | 72 | Python, BlackMamba, GreenMamba |
| Hyena | 70 | |
| Swine | 59 | Phacocheres |
| Canine | 55 | Chacals |
| Otter | 55 | Loutre geante |
| Equus | 52 | Zebres |
| Elephant | 48 | |
| Hippo | 48 | |
| Crocodile | 47 | |
| Rhino | 46 | |
| Fish | 37 | |
| Primate | 13 | |
| Snail | 8 | Escargots |
| Bat | 7 | Chauves-souris |
| Amphibian | 6 | |

### Assets partages (racine Animal/)

Decouverte critique — un **squelette partage** entre quadrupedes :

```
Quadruped_Skeleton.uasset          ← Squelette commun quadrupede
Quadruped_AnimBP.uasset            ← Animation Blueprint partage
Quadruped_LookAt.uasset            ← Systeme de regard
Quadruped_PhysicsAsset.uasset      ← Asset physique partage
M_Animal_Body.uasset               ← Material corps
M_Animal_Eyes.uasset               ← Material yeux
M_Animal_Fur.uasset                ← Material fourrure
M_Animal_Alpha.uasset              ← Material alpha (transparence)
```

**Implication pour le modding** : beaucoup d'animaux partagent le meme squelette
(`Quadruped_Skeleton`). Si on cree un nouvel animal quadrupede avec ce squelette,
il pourrait potentiellement reutiliser les animations existantes !

---

## GameSystems — Le coeur de la logique

### Animals_AI/ — 265 fichiers

IA des animaux, organise par espece :

| Animal | Fichiers | Contenu probable |
|--------|----------|-----------------|
| Crawlers (reptiles/insectes) | 33 | IA rampante |
| Leopard | 24 | IA predateur |
| AfricanBuffalo | 18 | IA herbivore agressif |
| Crocodile | 18 | IA embuscade aquatique |
| GiantOtter | 17 | |
| Hippo | 17 | |
| Elephant | 16 | |
| Hyena | 16 | IA meute |
| Jackal | 16 | |
| Warthog | 16 | |
| WhiteRhino | 16 | |
| Gazelle | 14 | IA fuite |
| Zebra | 14 | |
| GiantBird | 6 | IA aerienne |

Assets partages d'IA :
- `VL01_CDDFear_Predators.uasset` — Donnees de peur des predateurs
- `VL01_CDDPerception_Predators.uasset` — Perception des predateurs
- `VL01_*_CDSDamage.uasset` — Donnees de degats (Big/Medium/Small)
- `BP_DynamicFormation_*.uasset` — Formations de groupe
- `BP_*_LookAtMetrics.uasset` — Metriques de regard par espece

### Evolution/ — 50 fichiers

L'arbre d'evolution neuronal !

```
EVO_VL01.uasset                    ← Asset principal d'evolution
EVO_VL01_Template.uasset           ← Template
EVO_VL01_BU01.uasset               ← Branche ?
EVO_VL01_CR01.uasset               ← Branche ?
EVO_VL01_DI01..DI08.uasset         ← 8 nœuds "DI" (Dexterite/Intelligence ?)
EVO_VL01_DO01..DO03.uasset         ← 3 nœuds "DO" (Dodge/Domination ?)
EVO_VL01_FE01.uasset               ← Nœud "FE" (Fear ?)
EVO_VL01_FO01.uasset               ← Nœud "FO" (Food ?)
EVO_VL01_HE01..HE02.uasset         ← 2 nœuds "HE" (Health ?)
EVO_VL01_IA01.uasset               ← Nœud "IA" (Intelligence Artificielle ?)
EVO_VL01_IF01..IF09.uasset         ← 9 nœuds "IF" (Intelligence/Fabrication ?)
EVO_VL01_IN01..IN03.uasset         ← 3 nœuds "IN" (Intimidation ?)
EVO_VL01_KI01..KI04.uasset         ← 4 nœuds "KI" (Kinesthesia ?)
EVO_VL01_ME01.uasset               ← Nœud "ME" (Memory ?)
EVO_VL01_PS01.uasset               ← Nœud "PS" (Physical Strength ?)
EVO_VL01_RE01.uasset               ← Nœud "RE" (Reflexes ?)
EVO_VL01_RF01..RF03.uasset         ← 3 nœuds "RF" (Reflex ?)
EVO_VL01_SE01.uasset               ← Nœud "SE" (Senses ?)
EVO_VL01_US01..US03.uasset         ← 3 nœuds "US" (Use ?)

VL01_EvolutionData.uasset          ← DONNEES D'EVOLUTION (a examiner en priorite)
VL01_FulfillmentData.uasset        ← Donnees d'accomplissement
SYS_GIC_EvolutionTracker.uasset    ← Systeme de suivi d'evolution
```

### GameItems/ — 36 fichiers

Definition des items et de leurs proprietes :

```
CH1_GID_Abilities.uasset           ← Capacites
CH1_GID_Additives.uasset           ← Additifs (crafting ?)
CH1_GID_Aging.uasset               ← Vieillissement
CH1_GID_Alteration.uasset          ← Alterations d'etat
CH1_GID_BonusAbilities.uasset      ← Capacites bonus
CH1_GID_CharacterBehavior.uasset   ← Comportement du personnage
CH1_GID_CharacterSpawning.uasset   ← Spawn des personnages
CH1_GID_Construction.uasset        ← Construction
CH1_GID_ConsumePortion.uasset      ← Consommation de nourriture
CH1_GID_Corpses.uasset             ← Cadavres
CH1_GID_Cure.uasset                ← Soins
CH1_GID_Damage.uasset              ← Degats
CH1_GID_Discovered.uasset          ← Decouvertes
CH1_GID_Impact.uasset              ← Impact
CH1_GID_Intimidation.uasset        ← Intimidation
CH1_GID_ItemUse.uasset             ← Utilisation d'objets
CH1_GID_Physical.uasset            ← Stats physiques
CH1_GID_Poison.uasset              ← Poison
CH1_GID_PowerStone.uasset          ← Pierre de pouvoir (meteorites ?)
CH1_GID_Sense.uasset               ← Sens
CH1_GID_Settlement.uasset          ← Campement
CH1_GID_Tool.uasset                ← Outils
CH1_GID_WeaponDamage.uasset        ← Degats des armes
CH1_GID_Weapons.uasset             ← Armes
GID_Categorization.uasset          ← Systeme de categorisation
GID_CategoryTypes.uasset           ← Types de categories
```

### GameProgression/ — Eras et progression

```
VL01_GP_Era02..Era06.uasset        ← 5 eres de jeu
GP_Eras.uasset                     ← Definition des eres
GP_Meteorites.uasset               ← Systeme de meteorites
GP_Meteorite_01..12.uasset         ← 12 meteorites
GP_MeteoriteLandmark_00..06        ← Points de repere meteorites
GP_SideObjectives.uasset           ← Objectifs secondaires
Progression_Ancestors.uasset       ← Systeme de progression principal
```

---

## Maps — Structure du monde

### Prod/Maps/ — 2 007 fichiers

```
Prod/Maps/
├── Volume01/               ← Le monde du jeu
│   ├── Common/             ← Assets partages entre episodes
│   │   ├── GameProgression/
│   │   └── SYS/
│   └── VL01E01/            ← Volume 01, Episode 01 (le jeu entier)
│       ├── GameProgression/
│       ├── Story/
│       └── Tutorials/
└── MainMenu/               ← Menu principal
```

> Note : le jeu est structure en "Volumes" et "Episodes" (VL01E01).
> Le second .pak s'appelle `VL01E01.pak` — il contient probablement les
> maps/levels de cet episode. Cela suggere que Panache avait prevu
> d'ajouter d'autres volumes/episodes qui n'ont jamais ete realises.

---

## Audio — Wwise

Le jeu utilise **Wwise** (Audiokinetic) pour tout l'audio :

- 389 fichiers `.wem` dans `Ancestors/Binaries/Audio/Windows/`
- 11 fichiers `.bnk` (banques Wwise)
- 678 fichiers dans `Prod/Data/Audio/` (evenements, switches, RTPC)

---

## Decouvertes cles pour le modding

### Bonnes nouvelles

1. **Pas de chiffrement** — acces direct a tous les assets
2. **Squelette partage** (`Quadruped_Skeleton`) — nouveaux quadrupedes possibles
3. **GameSystems en assets separes** — IA, evolution, items sont des .uasset individuels, pas du C++ pur
4. **DataTables presents** (49 trouves) — surtout pour l'art (rochers, nids, patches de vegetation)
5. **319 Blueprints** (BP_) — une partie significative de la logique est en BP
6. **Fichier .pdb present** — les symboles de debug de l'exe sont disponibles

### Points d'attention

1. Les DataTables trouves sont surtout pour le placement d'objets naturels (rochers, vegetation), pas directement pour les stats de gameplay
2. Le systeme d'evolution utilise des assets individuels par noeud — il faudra les analyser pour comprendre le format
3. Les GameItems (GID_*) sont nombreux mais il faut determiner s'ils sont des DataTables modifiables ou des Blueprints compiles
4. La structure Volume/Episode suggere un jeu prevu pour etre extensible

### Prochaines etapes

- [ ] Extraire et analyser un fichier EVO_VL01_*.uasset pour comprendre le format de l'arbre d'evolution
- [ ] Extraire et analyser un fichier CH1_GID_*.uasset pour comprendre le format des GameItems
- [ ] Extraire un animal complet (ex: Crocodile) — mesh + textures + animations
- [ ] Analyser le VL01_EvolutionData.uasset — potentiellement le fichier le plus important
- [ ] Lister le contenu du second .pak (VL01E01.pak)
