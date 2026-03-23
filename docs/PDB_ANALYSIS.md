# Analyse du PDB — Classes et systemes du jeu

> Genere le 2026-03-22
> Source : Ancestors-Win64-Shipping.pdb (625 Mo, format PDB 7.0)
> 508 fichiers source Blueprint identifies

---

## Architecture du code

Le jeu est structure en couches :

### Prefixes de classes

| Prefixe | Signification | Exemple |
|---------|---------------|---------|
| **CDS** | Component Data Set — donnees d'un composant | CDSHealth, CDSVitality |
| **CDL** | Component Data Logic — logique d'un composant | CDLAttack, CDLFlee |
| **CDD** | Component Data Definition — definition | CDDFearNPC, CDDPerceptionNPC |
| **CS** | Component System — systeme transversal | CSLocation, CSPerceptibility |
| **GC** | Game Controller — controleur de haut niveau | GCPlayerClan, GCPredatorPack |
| **GCS** | Game Controller System — sous-systeme | GCSIntimidation, GCSFormation |
| **HE** | HUD Element — element d'interface | HECombat, HEFear, HEEvolution |
| **HCtx** | Human Context — contexte d'action humain | HCtxClimb, HCtxCombat |
| **CCtx** | Character Context — contexte general | CCtxAir, CCtxSwim |
| **QCS** | Quadruped Controller System | QCSAttitude |
| **MS** | Menu Screen | MSRPGMenu, MSPause |
| **MW** | Menu Widget | MWInGameMainMenu |
| **PPB** | Post-Process Blueprint | PPBBleed, PPBPoison |
| **BP** | Blueprint (standard UE4) | BP_Leopard_Attitude |

### Systemes principaux

#### Personnage (CDS* — Component Data Sets)

Le joueur et les NPC sont composes de multiples CDS :

**Stats de base :**
- CDSHealth / GameCDSHealth — sante
- CDSVitality — energie, stamina
- CDSRegimen / CDSRegimenNPC — nourriture, hydratation, sommeil
- CDSTemperature — temperature corporelle
- CDSNavigation — deplacement

**Combat :**
- CDSCombat / CDSCombatPlayer / CDSCombatNPC
- CDSWounds / CDSWoundsPlayer — blessures
- CDSBleed / CDSBleedPlayer — saignement
- CDSPoisoning — empoisonnement

**Interaction :**
- CDSEquipment / CDSEquipmentPlayer — equipement
- CDSItemHandler / CDSItemHandlerPlayer — gestion d'items
- CDSCrafting / CDSCraftingPlayer — fabrication
- CDSConstruction — construction
- CDSStationInteractions — interactions station

**Social :**
- CDSSocialInteractions / CDSSocialInteractionsPlayer
- CDSCommunicate / CDSCommunicateHuman / CDSCommunicatePlayer
- CDSEmotional / CDSEmotionalNPC / CDSEmotionalPlayer

**Perception :**
- CDSFearPerception / CDSFearPlayer — peur
- CDSGamePerception — perception du jeu
- CDSDiscoverEnvironment / CDSDiscoveryPlayer — decouverte
- CDSSenseInspect — inspection sensorielle
- CDSHidePlayer — camouflage

**Specialises :**
- CDSDopamine — systeme de dopamine
- CDSPlayerSelfControl — controle de soi
- CDSPlayerSlowMotion — ralenti
- CDSCamouflage — camouflage
- CDSSleep / CDSSleepPlayer — sommeil

#### Animaux

- QuadrupedCharacter — personnage quadrupede
- QuadrupedAnimInstance — animation quadrupede
- QuadrupedAttitudeData — attitudes
- QuadrupedCharacterProcess — processus logique
- BirdCharacter / BirdAnimInstance — oiseaux
- CrawlerCharacter / CrawlerAnimInstance — reptiles/insectes
- BatActor — chauve-souris

#### Evolution et progression

- EvolutionNode / EvolutionNodeGroup — noeuds d'evolution
- EvolutionNodeCondition / EvolutionNodeAction — conditions et actions
- EvolutionNodeData — donnees par noeud
- EvolutionTracker — suivi
- RPGNode / RPGNodeGroup — systeme RPG (= evolution)
- RPGTracker — suivi RPG
- RPGMenu / RPGMenuBranch / RPGMenuNode — menus RPG
- NeuronalEnergySource / NeuronalEnergyBooster — energie neuronale
- PlayerProgressionTracker — progression du joueur

#### Conditions de jeu (GameCondition*)

Classes qui definissent les conditions de deblocage :

- GameConditionDiscoverGameItem — decouvrir un item
- GameConditionCharacterAction — action du personnage
- GameConditionCombat — combat
- GameConditionCrafting — fabrication
- GameConditionClan — clan
- GameConditionFear — peur
- GameConditionSettlement — campement
- GameConditionEvolutionAttempt — tentative d'evolution
- GameConditionGenerationChanged — changement de generation
- GameConditionHysteria — hysterie
- GameConditionInventory — inventaire
- GameConditionTreeTopReached — atteindre le sommet d'un arbre
- GameConditionWeather — meteo
- GameConditionDifficultyLevel — niveau de difficulte
- GameConditionEmotionnalState — etat emotionnel

#### Monde et environnement

- FearManager / FearTypes — zones de peur
- WeatherManager / WeatherTypes — meteo
- TimeOfDayManager / TimeCycleManager — cycle jour/nuit
- AncestorsLevelRandomizer — randomisation des niveaux
- NavigationManager / NavigationGenerator — navigation IA
- GameZonesManager — gestionnaire de zones
- CanopyZone / TreeTopZone / GiantBirdZone — zones specifiques
- HidingZoneComponent / HidingZoneTracker — zones de cachette
- ShelteredZone — zones abritees

#### Items et dispensers

- AncestorsGameItemDispenser — distributeur d'items
- FoodGameItemDispenser — distributeur de nourriture
- OnDemandItemDispenser — distributeur a la demande
- StashGameItemDispenser — stash
- CorpseHandler — gestion des cadavres
- ConstructionHandler / ConstructionYard — construction
- PowerstoneComponent — pierres de pouvoir (meteorites)

#### Predateurs

- PredatorManager — gestionnaire de predateurs
- PredatorEvents — evenements de predateurs
- GCPredatorPack — meutes de predateurs
- GCSurpriseAttacks — attaques surprise
- GCSIntimidation — intimidation de groupe

#### Sauvegarde

- AncestorsSaveGame / SaveGameManager
- GameCharacterSaveGame / WildlifeSaveGame
- EvolutionSaveData

---

## Fonctions cles identifiees

| Fonction | Occurrences | Description |
|----------|-------------|-------------|
| Spawner::Spawn | 4 366 | Systeme de spawn des entites |
| Die | 1 023 | Mort des entites |
| TakeDamage | 6 | Prise de degats |
| Heal/Healthy | 55 | Soins et blessures |
| ChangeGeneration | 49 | Changement de generation |
| SaveGame | 10 147 | Sauvegarde |
| LoadGame | 34 | Chargement |

---

## Implications pour le modding

### Modifiable via Blueprint patching (Phase 3)
- Conditions d'evolution (GameCondition*)
- Donnees d'attitudes des animaux
- Menus RPG/Evolution
- Donnees de progression

### Modifiable via DLL injection (Phase 4)
- Fonctions Spawn (ajouter de nouveaux spawns)
- TakeDamage (modifier le systeme de degats)
- Sauvegarde/chargement (etendre les donnees sauvegardees)

### Architecture notable
- Le jeu utilise un systeme **CDS composable** tres propre
- Chaque aspect du gameplay est separe dans son propre composant
- Les animaux quadrupedes partagent le meme squelette et systeme d'animation
- Le systeme RPG (evolution) est distinct du systeme de progression
