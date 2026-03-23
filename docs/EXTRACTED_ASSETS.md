# Inventaire des assets extraits

> Genere le 2026-03-22
> Sources : UModel (18 032 fichiers) + FModel (15 077 fichiers + 2 783 PNG)

---

## Resume

| Type | Nombre | Format | Outil d'extraction |
|------|--------|--------|-------------------|
| SkeletalMesh (modeles animes) | 55 | .psk | UModel |
| StaticMesh (objets statiques) | 1 082 | .pskx | UModel |
| Animations | 3 079 | .psa | UModel |
| Textures | 3 065 + 2 783 | .tga / .png | UModel / FModel |
| Materials | 1 730 | .mat | UModel |
| Audio (Wwise) | 389 | .wem | FModel (raw) |
| Banques audio | 11 | .bnk | FModel (raw) |
| Proprietes assets | 5 946 | .txt | UModel |

---

## Modeles 3D — Animaux (27 SkeletalMesh)

### Oiseaux (6)

| Espece | Fichier | Taille |
|--------|---------|--------|
| Grue couronnee | Crane_Skelmesh.psk | 390 Ko |
| Aigle bateleur | EagleBateleur_Skelmesh.psk | 966 Ko |
| Perroquet | Parrot_Skelmesh.psk | 135 Ko |
| Pelagornis | Pelagornis_Skelmesh.psk | 532 Ko |
| Mouette | Seagull_Skelmesh.psk | 266 Ko |
| Vautour cinereous | VultureCinereous_Skelmesh.psk | 1.7 Mo |

### Mammiferes (15)

| Espece | Fichier | Taille |
|--------|---------|--------|
| Buffle d'Afrique | AfricanBuffalo_Skelmesh.psk | 441 Ko |
| Gazelle | Gazelle_Skelmesh.psk | 430 Ko |
| Chacal | Jackal_Skelmesh.psk | 904 Ko |
| Leopard (3 variantes) | Leopard_Skelmesh.psk | 2.0 Mo |
| | Leopard2_Skelmesh.psk | 2.4 Mo |
| | Leopard3_Skelmesh.psk | 2.0 Mo |
| Stegotetrabelodon (elephant) | Stegotetrabelodon_Skelmesh.psk | 657 Ko |
| Zebre | Zebra_Skelmesh.psk | 750 Ko |
| Hippopotame | Hippo_Skelmesh.psk | 710 Ko |
| Hyene tachetee | SpottedHyena2_Skelmesh.psk | 1.7 Mo |
| Loutre geante | GiantOtter_Skelmesh.psk | 663 Ko |
| Rhinoceros blanc | WhiteRhino_Skelmesh.psk | 719 Ko |
| Phacochere | Warthog_Skelmesh.psk | 808 Ko |
| Singe vervet | VervetMonkey_Skelmesh.psk | 678 Ko |

### Reptiles et insectes (5)

| Espece | Fichier | Taille |
|--------|---------|--------|
| Crocodile | Crocodylus_Skelmesh.psk | 971 Ko |
| Python | Python_Proc_Skelmesh.psk | 421 Ko |
| Mamba vert | SnakePoisonous_Proc_Skelmesh.psk | 179 Ko |
| Mamba noir | SnakePoisonousBlack_Proc_Skelmesh.psk | 179 Ko |
| Scolopendre geant | Scolopendra_Proc_Skelmesh.psk | 1.2 Mo |

### Poissons (2)

| Espece | Fichier | Taille |
|--------|---------|--------|
| Bar (vivant) | Bass_Skelmesh.psk | 270 Ko |
| Bar (endommage) | Bass_Damaged_Skelmesh.psk | 315 Ko |

---

## Modeles 3D — Hominides (26 SkeletalMesh)

### Lignee evolutive complete

| Espece | Variantes | Taille mesh |
|--------|-----------|-------------|
| **Sahelanthropus** | Male, Femelle, Bebe, BabyBag | 2.7 Mo (M/F) |
| **Orrorin** | Male, Femelle, Bebe, BabyBag, Enfant | 2.7 Mo (M/F) |
| **Ardipithecus** | Male, Femelle, Bebe, BabyBag, Enfant | 2.6 Mo (M/F) |
| **Australopithecus Afarensis** | Male, Femelle, Bebe, BabyBag | 2.6 Mo (M/F) |
| **Australopithecus Africanus** | Male, Femelle, Bebe, BabyBag, Enfant | 3.2 Mo (M/F) |
| **Homo Ergaster** | Male, Femelle, Bebe | 1.8 Mo (M/F) |

> Note : les modeles "Child" (30 Ko) sont probablement des references/proxys, pas des meshes complets.
> Les "BabyBag" sont les modeles du sac a bebe porte sur le dos.

---

## Animations (3 079 fichiers .psa)

| Categorie | Nombre | Contenu |
|-----------|--------|---------|
| Hominides (PreHomo) | 888 | Locomotion, actions, interactions |
| Camera locomotion | 511 | Mouvements camera |
| Camera actions | 375 | Actions camera |
| Camera combat | 270 | Camera de combat |
| Bovides (Buffalo/Gazelle) | 68 | Idle, marche, course, combat |
| Felins (Leopard) | 65 | Idle, chasse, attaque, fuite |
| Hyene | 52 | Comportements de meute |
| Cinematiques intro | 50 | Presentation |
| Serpents | 47 | Rampement, attaque |
| Loutre | 43 | Nage, sol |
| Canides (Chacal) | 43 | Comportements |
| Phacochere | 40 | Charge, idle |
| Oiseaux | 39 | Vol, atterrissage |
| Cinematiques mort (Leopard) | 37 | Sequences de mort |

---

## Textures (5 848 fichiers)

### Par UModel (.tga) — 3 065 fichiers

| Categorie | Nombre | Contenu |
|-----------|--------|---------|
| UI (interface) | 1 367 | Icones, menus, HUD |
| Art (environnement) | 675 | Rochers, sol, eau |
| Maps (terrain) | 384 | Heightmaps, landscape |
| Hominides | 121 | Peau, vetements, poils |
| VFX | 79 | Effets visuels |
| Oiseaux | 37 | Plumes, yeux |
| Insectes | 36 | Textures arthropodes |
| Materials | 25 | Textures de base |
| Poissons | 16 | Ecailles |
| Felins | 12 | Fourrure leopard |

### Par FModel (.png) — 2 783 fichiers

Principalement des textures de **landscape** (terrain du monde ouvert) :
- Format : `T_LandscapeProxy_*_LOD1_D.png` (diffuse) et `_N.png` (normal)
- Coordonnees : grille 50x50 a 60x60 — c'est la carte du monde !

---

## Cadavres (20 especes)

Chaque animal a des modeles de cadavre avec etapes de decomposition :

| Animal | Fichiers | Contenu |
|--------|----------|---------|
| Humanoid | 297 | Toutes les especes d'hominides |
| Leopard | 24 | 4 etapes decomposition + variantes |
| Meat (viande) | 22 | Morceaux de viande generiques |
| Scolopendra | 15 | Cadavre + parties |
| Stegotetrabelodon | 15 | Gros cadavre elephant |
| Python | 15 | Serpent mort |
| Buffalo/Crocodile/Hippo/Rhino | 13 chacun | Etapes decomposition |
| Eagle/Hyena/Otter/Pelagornis | 11 chacun | Carcasses |
| Gazelle/Jackal/Warthog/Zebra | 9-11 chacun | Carcasses |

---

## Objets statiques (1 082 StaticMesh)

| Categorie | Nombre | Contenu |
|-----------|--------|---------|
| Art (environnement) | 747 | Rochers, arbres, vegetation, nids, structures |
| Maps (niveau) | 107 | Elements de niveau |
| Cadavres humains | 41 | Variantes de cadavres |
| VFX | 40 | Particules et effets |
| Insectes | 19 | Modeles d'insectes statiques |
| Poissons | 8 | Variantes de poissons |
| UI | 10 | Elements 3D d'interface |
| Escargots | 4 | Modeles d'escargots |

---

## Chemins des exports

```
UModel exports:
  umodel_win32/UmodelExport/Game/Character/Animal/    — Animaux (modeles + textures + anims)
  umodel_win32/UmodelExport/Game/Character/Humanoid/  — Hominides
  umodel_win32/UmodelExport/Game/Character/Dead/      — Cadavres
  umodel_win32/UmodelExport/Game/Character/Camera/    — Cameras
  umodel_win32/UmodelExport/Game/Prod/Data/Art/       — Environnement
  umodel_win32/UmodelExport/Game/Prod/Data/UI/        — Interface
  umodel_win32/UmodelExport/Game/Prod/Data/VFX/       — Effets visuels
  umodel_win32/UmodelExport/Game/Prod/Maps/           — Terrain

FModel exports:
  Output/Exports/Ancestors/                           — Export brut des .uasset
  Output/Exports/ (PNG)                               — Textures de landscape
```

---

## Usage dans Blender

### Importer un modele animal
1. Installer l'addon PSK/PSA : https://github.com/matyalatte/Blender3D-Import-PSK-PSA
2. File > Import > ActorX (.psk)
3. Selectionner le .psk de l'animal
4. Le modele s'importe avec son squelette

### Importer les animations
1. File > Import > ActorX (.psa)
2. Selectionner le .psa correspondant
3. Les animations se chargent sur le squelette

### Appliquer les textures
1. Les textures .tga sont dans le sous-dossier Textures/ de chaque animal
2. `_D.tga` = Diffuse (couleur)
3. `_N.tga` = Normal map
4. `_R.tga` = Roughness
5. Creer un material PBR dans Blender et connecter chaque texture
