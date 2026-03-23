# Journal des decouvertes et lecons apprises

> Mis a jour le 2026-03-22

---

## 2026-03-22 — Session 1 : Exploration et premier mod

### Decouvertes

#### Version moteur
- **UE4.20** (confirme par Ancestors.uproject: `ANCESTORS_LIVE_4.20`)
- Pak V5 quand meme (le format pak V5 est utilise a partir de UE4.20)
- 4 modules : Ancestors, AncestorsEditor, PanacheEngine, PanacheGame
- Chemin Perforce du studio : `d:\p4\upload_ancestors_steam\game\`

#### Structure des fichiers .pak
- Deux fichiers .pak : principal (3.75 Go, 18 105 fichiers) + VL01E01 (2.98 Go, 14 610 fichiers)
- Les deux paks contiennent quasi les memes .uasset (14 608 en commun)
- Le pak principal a en plus : audio (.wem), images (.png), localisations, configs
- **Pas de chiffrement AES** — acces direct a tous les assets
- Format : Pak V5 (UE4.21-4.22), compression Zlib, mount point `../../../`
- Pas de fichiers .uexp separes — tout est dans les .uasset

#### Systeme de sante (CDSHealth)
- Chaque animal a son propre fichier `VL01_CDSHealth_[Animal].uasset`
- Classe C++ de base : `CDSHealth` du module `PanacheGame`
- Type d'asset : BlueprintGeneratedClass (pas DataTable)
- Propriete : `HealthMax` (FloatProperty)
- Echelle : 3.0 (zebra) a 20.0 (elephant)
- Le float se trouve a un offset variable (1132-1166) selon la longueur du nom
- Le byte `-8.0` (0xC1000000) apparait dans tous les fichiers — marqueur/default

#### Systeme de vitalite du joueur (CDSVitality)
- `EnergyRegenPerSecond` = 0.03 a offset 1524
- 9 proprietes float identifiees (thresholds, ratios, regen)
- Modifiable avec le meme pipeline que les animaux

#### Systeme de nutrition (CDSRegimen)
- `HoursBeforeLifeThreateningSituation` = 30.0 a offset 1968
- `MinutesBeforeDeathWhenLifeThreatened` = 20.0 a offsets 2026 et 2468
- `StartingFoodPercentage` / `StartingLiquidPercentage` / `StartingSleepPercentage` = 1.0

#### Audio
- Le jeu utilise **Wwise** (Audiokinetic), pas le systeme audio natif UE4
- 389 fichiers .wem + 11 banques .bnk
- Plugin Wwise reference dans le .pak

#### Armes (DataTable)
- `CH1_GID_Weapons.uasset` est un DataTable (type `GameItemDataWeapons`)
- 3 types : EWeaponType::Rock, ::Stick, ::Unarmed
- ~17 armes : Basalt, BlueAgate, Chopper, Granite, etc.
- Structure de rows de ~127 bytes chacune
- Parsing binaire brut insuffisant — besoin UAssetAPI

#### Evolution
- Systeme hybride : DataTable central (89 Ko) + Blueprints individuels par groupe
- 17 branches identifiees (DI, DO, FE, FO, HE, IA, IF, IN, KI, ME, PS, RE, RF, SE, US, BU, CR)
- 3 types de conditions :
  - GameConditionDiscoverGameItem (decouverte d'items)
  - GameConditionCharacterMetric (metriques : manger, boire)
  - GameConditionPlayerCombat (combat)
- Thresholds de nourriture = 1.0 (deblocage par premiere decouverte)
- Niveaux : Easy, Medium, Hard

#### Modeles 3D
- Squelette partage `Quadruped_Skeleton` avec 77 bones
- Hierarchie : root > pelvis > legs/tail, torso > spine > chest > arms/neck > head
- Sockets pre-definis : Stick1-6, socket_freeze
- 2 material slots sur les animaux : BODY + EYES
- PhysicsAsset par animal

#### PDB (symboles de debug)
- 625 Mo de symboles — extremement rare pour un jeu commercial
- 508 fichiers source Blueprint identifies (.gen.cpp)
- Architecture CDS composable complete decouverte
- Fonctions cles : Spawn (4366x), Die (1023x), TakeDamage (6x)
- Classes : ClanMember (40570x), Settlement (9599x), Neuron (3118x)

### Lecons apprises

#### Ce qui marche
1. Modifier des FloatProperty dans des BlueprintGeneratedClass en binaire brut
2. Repacker avec repak V5 Zlib mount "../../../"
3. Le suffixe _P.pak est charge apres les paks de base (override)
4. Plusieurs assets modifies dans un seul .pak patch

#### Ce qui ne marche PAS
1. **Modifier les textures en brute force** — les metadonnees entre mipmaps (FBulkData headers) sont ecrasees, ce qui fait crasher le jeu. Il faut un outil qui comprend le format (FModel/UAssetAPI).
2. **Parser les DataTables en brute force** — la serialisation FName est trop complexe sans parser correctement le header UE4. UAssetAPI est necessaire.
3. **Ajouter des lignes/rows** a un DataTable en binaire — necessite de modifier la name table et les offsets du header.

#### Bonnes pratiques
- Toujours verifier la valeur attendue avant de patcher (`assert old_val == expected`)
- Ne jamais changer la taille d'un fichier .uasset
- Garder le meme format pak (V5, Zlib, mount point) que l'original
- Tester avec une modification minimale d'abord (un seul float)
- Toujours pouvoir desinstaller : supprimer le _P.pak suffit
