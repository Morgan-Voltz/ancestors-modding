# Animal Database — Complete Reference

> All 14 moddable animal species with stats, file paths, and technical details.

---

## Overview

All animals in the game use the **CDS (Component Data Set)** system. Each animal has separate files for health, navigation, communication, perception, and behavior.

Most quadrupeds share the `Quadruped_Skeleton` (77 bones), which means animations can be shared between species.

---

## Health stats (vanilla values)

| # | Animal | HealthMax | Tier | Behavior | Offset |
|---|--------|-----------|------|----------|--------|
| 1 | Elephant (Stegotetrabelodon) | **20.0** | Boss | Passive unless provoked | 1144 |
| 2 | Crocodile (Crocodylus) | **12.0** | Tank | Ambush predator, water | 1148 |
| 3 | African Buffalo | **10.0** | Tough | Aggressive herbivore | 1147 |
| 4 | Hippopotamus | **10.0** | Tough | Territorial, water | 1132 |
| 5 | White Rhinoceros | **10.0** | Tough | Charge attack | 1152 |
| 6 | Leopard | **9.0** | Apex | Stalker, ambush | 1140 |
| 7 | Spotted Hyena | **6.0** | Pack | Pack hunter | 1132 |
| 8 | Jackal | **6.0** | Pack | Scavenger, pack | 1136 |
| 9 | Warthog | **6.0** | Medium | Charge, aggressive | 1140 |
| 10 | Gazelle | **4.0** | Prey | Flees on sight | 1140 |
| 11 | Python | **4.0** | Ambush | Constriction | 1166 |
| 12 | Giant Otter | **3.0** | Small | Water predator | 1152 |
| 13 | Zebra | **3.0** | Prey | Herd, flees | 1132 |
| 14 | Giant Centipede (Scolopendra) | **3.0** | Insect | Venomous | 1165 |

---

## Detailed species profiles

### Elephant (Stegotetrabelodon)

The prehistoric ancestor of modern elephants. Largest animal in the game.

```
Health:     20.0 HP (highest in game)
Category:   Character/Animal/Elephant/Stegotetrabelodon/
Skeleton:   Quadruped_Skeleton (shared)
Mesh:       Stegotetrabelodon_Skelmesh.psk (657 KB)
```

**Files:**
| File | Path |
|------|------|
| Health | `.../Animals_AI/Elephant/VL01_CDSHealth_Elephant.uasset` |
| Navigation | `.../Animals_AI/Elephant/VL01_CDSNavigation_Elephant.uasset` |
| AI Controller | `.../Animals_AI/Elephant/BP_ElephantQuadAIController.uasset` |
| Mesh | `.../Character/Animal/Elephant/Stegotetrabelodon/Mesh/Stegotetrabelodon_Skelmesh.uasset` |
| Carcass | `.../Character/Dead/Stegotetrabelodon/` (15 files) |

**Textures:** Diffuse (_D), Normal (_N), Roughness (_R), Blood (_Blood_D), Eyes

---

### Crocodile (Crocodylus)

Semi-aquatic ambush predator. Can attack in water and on land.

```
Health:     12.0 HP
Category:   Character/Animal/Crocodile/Crocodylus/
Skeleton:   Quadruped_Skeleton (shared)
Mesh:       Crocodylus_Skelmesh.psk (971 KB)
Materials:  BODY + EYES (2 material slots)
```

**Files:**
| File | Path |
|------|------|
| Health | `.../Animals_AI/Crocodile/VL01_CDSHealth_Crocodile.uasset` |
| Navigation | `.../Animals_AI/Crocodile/VL01_CDSNavigation_Crocodile.uasset` |
| Communication | `.../Animals_AI/Crocodile/VL01_CDSCommunicate_Crocodile.uasset` |
| Perception | `.../Animals_AI/Crocodile/VL01_Perception_Crocodile.uasset` |
| Reaction | `.../Animals_AI/Crocodile/VL01_ReactionHandler_Crocodile.uasset` |
| AI Controller | `.../Animals_AI/Crocodile/BP_CrocodileQuadAIController.uasset` |
| Ground Metrics | `.../Animals_AI/Crocodile/BP_CrocodileGroundMetrics.uasset` |
| Swim Metrics | `.../Animals_AI/Crocodile/BP_CrocodileSurfaceSwimMetrics.uasset` |
| Schedule | `.../Animals_AI/Crocodile/BP_Crocodile_Schedule.uasset` |
| Attack Kit | `.../Animals_AI/Crocodile/VL01E01_Crocodile_HomoAttackKit.uasset` |

**Attitudes (4 states):**
- `BP_Crocodile_Attitude_Normal.uasset`
- `BP_Crocodile_Attitude_Aggressive.uasset`
- `BP_Crocodile_Attitude_Stealth.uasset`
- `BP_Crocodile_Attitude_Wounded.uasset`

**Animations (37 total):**
- Idle: 10 (normal, threatening, turns)
- Move: 16 (ground walk/run, swim slow/normal/fast, starts/stops)
- Attack: 4 (ground + water, start + hit)
- Combat: 4 (countered by rock/stick, last hit)
- Resist: 1

**Associated items:**
- Crocodile eggs (3 variants: whole, broken, punctured)
- Crocodile nest
- Crocodile carcass (4 decomposition stages)

---

### Leopard

The main predator threat. Has 3 mesh variants (standard, Leopard2, Leopard3 — likely LODs or color variants including black leopard).

```
Health:     9.0 HP
Variants:   Standard, Black Leopard, White Leopard
Category:   Character/Animal/Feline/Leopard/
Skeleton:   Quadruped_Skeleton (shared)
Mesh:       Leopard_Skelmesh.psk (2.0 MB)
```

**Unique features:**
- 3 mesh variants (Leopard, Leopard2, Leopard3)
- Black Leopard sub-variant with its own predator pack
- White Leopard with separate health file and AI controller
- 65 animations (most of any animal)
- 37 death cinematics
- LookAt metrics, formation behavior

**Attitudes:** Normal, Aggressive, Stealth, Wounded

---

### Spotted Hyena

Pack predator. Hunts in groups.

```
Health:     6.0 HP
Category:   Character/Animal/Hyena/SpottedHyena/
Skeleton:   Quadruped_Skeleton (shared)
Mesh:       SpottedHyena2_Skelmesh.psk (1.7 MB)
Animations: 52
```

---

### African Buffalo

Aggressive herbivore. Will attack when provoked.

```
Health:     10.0 HP
Category:   Character/Animal/Bovid/AfricanBuffalo/
Skeleton:   Quadruped_Skeleton (shared)
Mesh:       AfricanBuffalo_Skelmesh.psk (441 KB)
```

---

### Gazelle

Prey animal. Flees from predators and the player.

```
Health:     4.0 HP
Category:   Character/Animal/Bovid/Gazelle/
Skeleton:   Quadruped_Skeleton (shared)
Mesh:       Gazelle_Skelmesh.psk (430 KB)
```

---

### Zebra

Herd prey animal.

```
Health:     3.0 HP
Category:   Character/Animal/Equus/Zebra/
Skeleton:   Quadruped_Skeleton (shared)
Mesh:       Zebra_Skelmesh.psk (750 KB)
```

---

### Jackal

Pack scavenger and small predator.

```
Health:     6.0 HP
Category:   Character/Animal/Canine/Jackal/
Skeleton:   Quadruped_Skeleton (shared)
Mesh:       Jackal_Skelmesh.psk (904 KB)
Animations: 43
```

---

### Warthog

Aggressive small herbivore. Charges at threats.

```
Health:     6.0 HP
Category:   Character/Animal/Swine/Warthog/
Skeleton:   Quadruped_Skeleton (shared)
Mesh:       Warthog_Skelmesh.psk (808 KB)
Animations: 40
```

---

### Hippopotamus

Territorial semi-aquatic herbivore.

```
Health:     10.0 HP
Category:   Character/Animal/Hippo/Hippo/
Skeleton:   Quadruped_Skeleton (shared)
Mesh:       Hippo_Skelmesh.psk (710 KB)
```

---

### White Rhinoceros

Heavy herbivore with charge attack.

```
Health:     10.0 HP
Category:   Character/Animal/Rhino/WhiteRhino/
Skeleton:   Quadruped_Skeleton (shared)
Mesh:       WhiteRhino_Skelmesh.psk (719 KB)
```

---

### Giant Otter

Small water predator.

```
Health:     3.0 HP
Category:   Character/Animal/Otter/GiantOtter/
Skeleton:   Quadruped_Skeleton (shared)
Mesh:       GiantOtter_Skelmesh.psk (663 KB)
Animations: 43
```

---

### Python

Large constricting snake. Uses procedural animation.

```
Health:     4.0 HP
Category:   Character/Animal/Snake/Python_Proc/
Skeleton:   Own skeleton (not Quadruped)
Mesh:       Python_Proc_Skelmesh.psk (421 KB)
Type:       Crawler (procedural animation)
```

---

### Venomous Snakes (Mamba)

Two variants: Green Mamba and Black Mamba. Procedural animation.

```
Health:     Not in standard CDSHealth (separate system)
Category:   Character/Animal/Snake/SnakePoisonous_Proc/
Meshes:     SnakePoisonous_Proc_Skelmesh.psk (179 KB)
            SnakePoisonousBlack_Proc_Skelmesh.psk (179 KB)
Type:       Crawler
```

---

### Giant Centipede (Scolopendra)

Large venomous arthropod. Procedural animation.

```
Health:     3.0 HP
Category:   Character/Animal/Insect/Scolopendra_Proc/
Skeleton:   Own skeleton (not Quadruped)
Mesh:       Scolopendra_Proc_Skelmesh.psk (1.2 MB)
Type:       Crawler
```

---

## Non-moddable animals (no CDSHealth)

These animals exist in the game but don't have individual health files:

| Animal | Category | Type | Notes |
|--------|----------|------|-------|
| Vervet Monkey | Primate | SkeletalMesh | Passive NPC |
| Crane | Bird | SkeletalMesh | Ambient wildlife |
| Eagle Bateleur | Bird/Giant | SkeletalMesh | Aerial predator |
| Pelagornis | Bird/Giant | SkeletalMesh | Aerial predator |
| Seagull | Bird | SkeletalMesh | Ambient |
| Vulture | Bird | SkeletalMesh | Ambient |
| Parrot | Bird | SkeletalMesh | Ambient |
| Bass (Fish) | Fish | SkeletalMesh | Catchable |
| Toad | Amphibian | Static? | Ambient |
| Snail | Snail | Static | Ambient |
| Bat | Bat | Static | Ambient (sleeping) |

Giant birds (Eagle, Pelagornis) have separate health files:
- `VL01_CDSHealth_Eagle.uasset`
- `VL01_CDSHealth_Pelagornis.uasset`

---

## Shared skeleton — Quadruped_Skeleton

77 bones shared by all quadruped mammals:

```
bone_root
├── bone_pelvis (+scale)
│   ├── bone_l_leg1→2→3→4→5
│   ├── bone_r_leg1→2→3→4→5
│   └── bone_tail1→2→3→4→5→6→7
├── bone_torso
│   └── bone_spine1→2→3→4 (+scale each)
│       └── bone_chest
│           ├── bone_l_arm1→2→3→4→5→6
│           ├── bone_r_arm1→2→3→4→5→6
│           └── bone_neck1→2→3→4
│               └── bone_head
│                   ├── bone_jaw, bone_tongue1→2→3
│                   ├── bone_l/r_eye, bone_l/r_ear
│                   ├── bone_l/r_eyelid_upper/lower
│                   ├── bone_nose, bone_nose1→7
│                   └── bone_l/r_lip_upper_front/back
└── bone_breath1→2→3

Sockets: Stick1-6, socket_freeze
```

**For new animal creation:** If you rig a new model to this exact bone hierarchy, it can use ALL existing quadruped animations.

---

## Per-animal file pattern

Every animal with AI follows this file pattern:

```
GameSystems/Animals_AI/[Animal]/
├── VL01_CDSHealth_[Animal].uasset          ← Health (HealthMax float)
├── VL01_CDSNavigation_[Animal].uasset      ← Movement parameters
├── VL01_CDSCommunicate_[Animal].uasset     ← Sound/communication
├── VL01_Perception_[Animal].uasset         ← Detection range
├── VL01_ReactionHandler_[Animal].uasset    ← Behavior reactions
├── BP_[Animal]QuadAIController.uasset      ← Main AI controller
├── BP_[Animal]GroundMetrics.uasset         ← Ground movement stats
├── BP_[Animal]_Schedule.uasset             ← Daily schedule
├── BP_[Animal]_AttitudeKit.uasset          ← Attitude state machine
├── BP_Formation_[Animal].uasset            ← Group behavior
├── BP_PredatorPack_[Animal].uasset         ← Pack spawning
├── VL01E01_[Animal]_HomoAttackKit.uasset   ← Player attack behavior
├── Attitudes/
│   ├── BP_[Animal]_Attitude_Normal.uasset
│   ├── BP_[Animal]_Attitude_Aggressive.uasset
│   ├── BP_[Animal]_Attitude_Stealth.uasset
│   └── BP_[Animal]_Attitude_Wounded.uasset
```

Not all animals have all files. Crawlers (snakes, centipede) have a different structure.
