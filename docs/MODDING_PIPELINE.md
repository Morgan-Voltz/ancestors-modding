# Pipeline de modding — Guide complet

> Premier mod fonctionnel cree le 2026-03-22
> TestMod_P.pak : modification du HealthMax du leopard (9.0 -> 1.0)

---

## Prerequis

- **repak** v0.2.3+ (installe dans `~/tools/repak/repak.exe`)
  - Source : https://github.com/trumank/repak
  - Binaires precompiles dans les Releases GitHub
- **Python 3** (pour les scripts de patching)
- **Acces en ecriture** au dossier `Content/Paks/` du jeu

---

## Pipeline en 4 etapes

### Etape 1 — Extraire l'asset original

```bash
# Extraire un fichier specifique du .pak
repak get "Ancestors/Content/Paks/Ancestors-WindowsNoEditor.pak" \
    "Ancestors/Content/Prod/Data/GameSystems/Animals_AI/Leopard/VL01_CDSHealth_Leopard.uasset" \
    > VL01_CDSHealth_Leopard.uasset
```

**Pourquoi extraire d'abord ?** On a besoin du fichier original comme base.
On ne peut pas creer un .uasset from scratch facilement — il contient des
metadonnees binaires specifiques (name table, imports, exports, GUIDs).
On modifie uniquement les donnees qu'on veut changer.

### Etape 2 — Modifier l'asset

Pour les **valeurs numeriques** (float, int) identifiees lors de l'exploration :

```python
import struct

with open('VL01_CDSHealth_Leopard.uasset', 'rb') as f:
    data = bytearray(f.read())

# Modifier le float a l'offset identifie
# Offset 1140 = HealthMax (FloatProperty)
struct.pack_into('<f', data, 1140, 1.0)  # Nouvelle valeur

with open('output/VL01_CDSHealth_Leopard.uasset', 'wb') as f:
    f.write(data)
```

**Comment trouver l'offset ?** Deux methodes :
1. Scanner le fichier pour la valeur connue (`struct.pack('<f', 9.0)`)
2. Parser le name table et chercher le nom de la propriete

**Attention** : ne JAMAIS changer la taille du fichier ! Ajouter ou retirer
des octets casserait tous les offsets internes. On ne modifie que des valeurs
existantes en gardant la meme taille.

### Etape 3 — Packager en .pak

```bash
# Structure du dossier de mod (doit reproduire le chemin interne du pak)
# ~/ancestors_mod/
#   Ancestors/Content/Prod/Data/GameSystems/Animals_AI/Leopard/
#     VL01_CDSHealth_Leopard.uasset

# Packager
repak pack \
    --version V5 \
    --compression Zlib \
    --mount-point "../../../" \
    ~/ancestors_mod \
    ~/ancestors_mod/TestMod_P.pak
```

**Parametres critiques :**

| Parametre | Valeur | Pourquoi |
|-----------|--------|----------|
| `--version V5` | Meme version que le .pak original | Incompatibilite si different |
| `--compression Zlib` | Meme compression que l'original | Le jeu doit pouvoir lire |
| `--mount-point "../../../"` | Meme mount point que l'original | Les chemins doivent matcher |
| Suffixe `_P` dans le nom | Convention UE4 pour "Patch" | Charge apres les paks de base |

### Etape 4 — Installer le mod

```bash
# Copier dans le dossier Paks du jeu
cp TestMod_P.pak "<chemin_jeu>/Ancestors/Content/Paks/"
```

Le jeu chargera automatiquement notre .pak au demarrage. Pas besoin de
modifier quoi que ce soit d'autre.

**Pour desinstaller** : supprimer le fichier `TestMod_P.pak` du dossier Paks.

---

## Comment UE4 gere les .pak patches

```
Ordre de chargement :
1. Ancestors-WindowsNoEditor.pak     <- Assets de base
2. VL01E01.pak                       <- Contenu supplementaire
3. TestMod_P.pak                     <- Notre mod (suffixe _P)

Regle : si un asset a le meme chemin interne dans deux .pak,
         la version du DERNIER .pak charge gagne (override).
```

Le suffixe `_P` indique a UE4 que c'est un "patch pak".
UE4 charge les patch paks APRES les paks de base, par ordre alphabetique.
Si on a plusieurs mods, leur ordre de priorite est alphabetique :
`AAA_P.pak` est charge avant `ZZZ_P.pak`.

---

## Offsets connus pour le patching

### CDSHealth (sante des animaux)

Tous les fichiers `VL01_CDSHealth_*.uasset` suivent le meme pattern.
Le float HealthMax se trouve a un offset qui depend de la taille du name table
(qui varie selon la longueur du nom de l'animal).

| Animal | Fichier | Taille | Offset HealthMax | Valeur originale |
|--------|---------|--------|-----------------|-----------------|
| Leopard | VL01_CDSHealth_Leopard | 1156 | 1140 | 9.0 |
| Crocodile | VL01_CDSHealth_Crocodile | 1164 | ? | 12.0 |
| Elephant | VL01_CDSHealth_Elephant | 1160 | ? | 20.0 |
| (a completer pour chaque animal) |

**Methode pour trouver l'offset de n'importe quel animal :**
```python
target = struct.pack('<f', VALEUR_CONNUE)  # ex: 12.0 pour le crocodile
for i in range(len(data) - 3):
    if data[i:i+4] == target:
        print(f'Offset: {i}')
```

---

## Risques et precautions

| Risque | Mitigation |
|--------|-----------|
| Crash au demarrage | Le jeu ignore les .pak invalides dans la plupart des cas |
| Corruption de sauvegarde | Peu probable avec des changements de stats numeriques |
| Mise a jour Steam ecrase le mod | Le mod est un fichier separe, Steam ne le touche pas |
| Incompatibilite entre mods | Verifier que deux mods ne changent pas le meme fichier |

**Backup** : On peut toujours verifier l'integrite des fichiers via
Steam > Clic droit > Proprietes > Fichiers installes > Verifier.
Ca ne supprime PAS nos fichiers _P.pak ajoutes manuellement.

---

## Prochaines etapes

### Modification de textures
1. Extraire une texture (_D, _N, _R) avec FModel ou UModel
2. Exporter en .png
3. Modifier dans un editeur d'image
4. Reconvertir en .uasset (necessite UAssetAPI ou l'editeur UE4)
5. Packager et tester

### Modification de DataTables
1. Extraire le DataTable (ex: CH1_GID_Weapons.uasset)
2. Utiliser UAssetAPI pour lire/modifier les lignes
3. Repackager

### Ajout d'un nouvel animal (Phase 3)
1. Modeliser dans Blender avec le squelette Quadruped_Skeleton
2. Texturer (diffuse, normal, roughness)
3. Exporter en FBX, importer dans l'editeur UE4
4. Cuisiner les assets
5. Creer les fichiers CDS (Health, Navigation, etc.)
6. Enregistrer dans les systemes de spawn
7. Packager et tester
