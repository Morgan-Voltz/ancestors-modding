"""
patch_health.py — Modifier la sante des animaux dans Ancestors: The Humankind Odyssey

Usage:
    python patch_health.py <animal> <new_health>
    python patch_health.py --list
    python patch_health.py --all <multiplier>

Exemples:
    python patch_health.py leopard 1.0       # Leopard = 1 HP
    python patch_health.py elephant 50.0     # Elephant = 50 HP
    python patch_health.py --list            # Afficher les valeurs actuelles
    python patch_health.py --all 0.5         # Diviser toute la sante par 2

Le script extrait le fichier original du .pak, le modifie, et cree un
fichier .pak patch pret a etre copie dans Content/Paks/.
"""

import struct
import os
import sys
import subprocess
import shutil

# Configuration
GAME_DIR = r"C:\Program Files (x86)\Steam\steamapps\common\Ancestors The Humankind Odyssey"
PAK_FILE = os.path.join(GAME_DIR, "Ancestors", "Content", "Paks", "Ancestors-WindowsNoEditor.pak")
REPAK = os.path.expanduser("~/tools/repak/repak.exe")
MOD_DIR = os.path.expanduser("~/ancestors_mod")
OUTPUT_PAK = os.path.join(MOD_DIR, "HealthMod_P.pak")
INSTALL_DIR = os.path.join(GAME_DIR, "Ancestors", "Content", "Paks")

# Animal database: {name: (pak_path, file_size, health_offset, original_health)}
ANIMALS = {
    "buffalo":      ("Ancestors/Content/Prod/Data/GameSystems/Animals_AI/AfricanBuffalo/VL01_CDSHealth_Buffalo.uasset",        1163, 1147, 10.0),
    "crocodile":    ("Ancestors/Content/Prod/Data/GameSystems/Animals_AI/Crocodile/VL01_CDSHealth_Crocodile.uasset",            1164, 1148, 12.0),
    "elephant":     ("Ancestors/Content/Prod/Data/GameSystems/Animals_AI/Elephant/VL01_CDSHealth_Elephant.uasset",              1160, 1144, 20.0),
    "gazelle":      ("Ancestors/Content/Prod/Data/GameSystems/Animals_AI/Gazelle/VL01_CDSHealth_Gazelle.uasset",                1156, 1140,  4.0),
    "giantotter":   ("Ancestors/Content/Prod/Data/GameSystems/Animals_AI/GiantOtter/VL01_CDSHealth_GiantOtter.uasset",          1168, 1152,  3.0),
    "hippo":        ("Ancestors/Content/Prod/Data/GameSystems/Animals_AI/Hippo/VL01_CDSHealth_Hippo.uasset",                    1148, 1132, 10.0),
    "hyena":        ("Ancestors/Content/Prod/Data/GameSystems/Animals_AI/Hyena/VL01_CDSHealth_Hyena.uasset",                    1148, 1132,  6.0),
    "jackal":       ("Ancestors/Content/Prod/Data/GameSystems/Animals_AI/Jackal/VL01_CDSHealth_Jackal.uasset",                  1152, 1136,  6.0),
    "leopard":      ("Ancestors/Content/Prod/Data/GameSystems/Animals_AI/Leopard/VL01_CDSHealth_Leopard.uasset",                1156, 1140,  9.0),
    "python":       ("Ancestors/Content/Prod/Data/GameSystems/Animals_AI/Crawlers/Python/VL01_CDSHealth_PythonCrawler.uasset",  1182, 1166,  4.0),
    "scolopendra":  ("Ancestors/Content/Prod/Data/GameSystems/Animals_AI/Crawlers/Scolopendra/VL01_Scolopendra_CDSHealth.uasset", 1181, 1165, 3.0),
    "warthog":      ("Ancestors/Content/Prod/Data/GameSystems/Animals_AI/Warthog/VL01_CDSHealth_Warthog.uasset",                1156, 1140,  6.0),
    "whiterhino":   ("Ancestors/Content/Prod/Data/GameSystems/Animals_AI/WhiteRhino/VL01_CDSHealth_WhiteRhino.uasset",          1168, 1152, 10.0),
    "zebra":        ("Ancestors/Content/Prod/Data/GameSystems/Animals_AI/Zebra/VL01_CDSHealth_Zebra.uasset",                    1148, 1132,  3.0),
}


def extract_asset(pak_path_internal):
    """Extrait un asset du .pak et retourne ses bytes."""
    result = subprocess.run(
        [REPAK, "get", PAK_FILE, pak_path_internal],
        capture_output=True
    )
    if result.returncode != 0:
        print(f"ERREUR: impossible d'extraire {pak_path_internal}")
        print(result.stderr.decode())
        sys.exit(1)
    return bytearray(result.stdout)


def patch_health(data, offset, new_value, expected_size):
    """Modifie la valeur HealthMax dans les donnees de l'asset."""
    if len(data) != expected_size:
        print(f"ATTENTION: taille inattendue ({len(data)} vs {expected_size} attendu)")

    old_value = struct.unpack_from('<f', data, offset)[0]
    struct.pack_into('<f', data, offset, new_value)
    return old_value


def list_animals():
    """Affiche la liste des animaux et leur sante originale."""
    print(f"\n{'Animal':<15} {'Sante originale':<18} {'Pak path'}")
    print("-" * 90)
    for name, (path, size, offset, health) in sorted(ANIMALS.items()):
        print(f"  {name:<15} {health:<18.1f} {path}")
    print()


def build_mod(modifications):
    """Construit le .pak avec toutes les modifications."""
    # Nettoyer le dossier mod
    if os.path.exists(MOD_DIR):
        # Ne supprimer que les sous-dossiers Ancestors/
        ancestors_dir = os.path.join(MOD_DIR, "Ancestors")
        if os.path.exists(ancestors_dir):
            shutil.rmtree(ancestors_dir)

    for animal, new_health in modifications.items():
        pak_path, expected_size, offset, original = ANIMALS[animal]

        # Extraire
        data = extract_asset(pak_path)

        # Patcher
        old = patch_health(data, offset, new_health, expected_size)
        print(f"  {animal:<15} {old:.1f} -> {new_health:.1f}")

        # Ecrire dans la structure de mod
        out_path = os.path.join(MOD_DIR, pak_path)
        os.makedirs(os.path.dirname(out_path), exist_ok=True)
        with open(out_path, 'wb') as f:
            f.write(data)

    # Packager
    print(f"\nPackaging...")
    result = subprocess.run(
        [REPAK, "pack", "--version", "V5", "--compression", "Zlib",
         "--mount-point", "../../../", MOD_DIR, OUTPUT_PAK],
        capture_output=True, text=True
    )
    if result.returncode != 0:
        print(f"ERREUR de packaging: {result.stderr}")
        sys.exit(1)

    pak_size = os.path.getsize(OUTPUT_PAK)
    print(f"Mod cree: {OUTPUT_PAK} ({pak_size:,} bytes)")

    # Copier dans le jeu
    install_path = os.path.join(INSTALL_DIR, "HealthMod_P.pak")
    shutil.copy2(OUTPUT_PAK, install_path)
    print(f"Installe dans: {install_path}")
    print("\nLance le jeu pour tester !")


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(0)

    if sys.argv[1] == "--list":
        list_animals()
        sys.exit(0)

    if sys.argv[1] == "--all":
        if len(sys.argv) < 3:
            print("Usage: patch_health.py --all <value_or_multiplier>")
            print("  --all 1.0     -> tous les animaux a 1.0 HP (valeur absolue)")
            print("  --all x0.5    -> multiplier toute la sante par 0.5 (prefixe x)")
            sys.exit(1)
        arg = sys.argv[2]
        if arg.startswith("x"):
            multiplier = float(arg[1:])
            print(f"Multiplication de toute la sante par {multiplier}:")
            mods = {name: max(0.1, info[3] * multiplier) for name, info in ANIMALS.items()}
        else:
            value = float(arg)
            print(f"Tous les animaux a {value} HP:")
            mods = {name: value for name in ANIMALS}
        build_mod(mods)
        sys.exit(0)

    # Single animal modification
    animal = sys.argv[1].lower()
    if animal not in ANIMALS:
        print(f"Animal inconnu: {animal}")
        print(f"Animaux disponibles: {', '.join(sorted(ANIMALS.keys()))}")
        sys.exit(1)

    if len(sys.argv) < 3:
        print(f"Usage: patch_health.py {animal} <new_health>")
        sys.exit(1)

    new_health = float(sys.argv[2])
    print(f"Modification de la sante de {animal}:")
    build_mod({animal: new_health})


if __name__ == "__main__":
    main()
