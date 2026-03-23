"""
Ancestors: The Humankind Odyssey — Difficulty Mod Manager
Configurateur de difficulte avec interface graphique.

By DaddyOurs — https://github.com/DaddyOurs
First modding tool ever made for Ancestors: The Humankind Odyssey.
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import struct
import subprocess
import os
import shutil
import sys
import winreg

VERSION = "1.0.0"

# ============================================================
# AUTO-DETECTION
# ============================================================

def find_game_dir():
    """Auto-detect game installation directory."""
    # 1. Check if we're inside the game directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    for parent in [script_dir, os.path.dirname(script_dir)]:
        pak = os.path.join(parent, "Ancestors", "Content", "Paks", "Ancestors-WindowsNoEditor.pak")
        if os.path.exists(pak):
            return parent

    # 2. Common Steam paths
    steam_paths = [
        r"C:\Program Files (x86)\Steam\steamapps\common\Ancestors The Humankind Odyssey",
        r"C:\Program Files\Steam\steamapps\common\Ancestors The Humankind Odyssey",
        r"D:\Steam\steamapps\common\Ancestors The Humankind Odyssey",
        r"D:\SteamLibrary\steamapps\common\Ancestors The Humankind Odyssey",
        r"E:\SteamLibrary\steamapps\common\Ancestors The Humankind Odyssey",
    ]
    for p in steam_paths:
        if os.path.exists(os.path.join(p, "Ancestors", "Content", "Paks")):
            return p

    # 3. Try Steam registry
    try:
        key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\WOW6432Node\Valve\Steam")
        steam_path = winreg.QueryValueEx(key, "InstallPath")[0]
        winreg.CloseKey(key)
        p = os.path.join(steam_path, "steamapps", "common", "Ancestors The Humankind Odyssey")
        if os.path.exists(os.path.join(p, "Ancestors", "Content", "Paks")):
            return p
    except (OSError, FileNotFoundError):
        pass

    return None


def find_repak():
    """Find repak.exe — bundled with the mod or in tools."""
    # 1. Bundled next to this script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    for candidate in [
        os.path.join(script_dir, "repak.exe"),
        os.path.join(script_dir, "tools", "repak.exe"),
    ]:
        if os.path.exists(candidate):
            return candidate

    # 2. User tools directory
    user_repak = os.path.join(os.path.expanduser("~"), "tools", "repak", "repak.exe")
    if os.path.exists(user_repak):
        return user_repak

    # 3. In PATH
    for p in os.environ.get("PATH", "").split(os.pathsep):
        candidate = os.path.join(p, "repak.exe")
        if os.path.exists(candidate):
            return candidate

    return None


# ============================================================
# CONFIGURATION (auto-detected)
# ============================================================

GAME_DIR = find_game_dir()
REPAK = find_repak()

if GAME_DIR:
    PAK_FILE = os.path.join(GAME_DIR, "Ancestors", "Content", "Paks", "Ancestors-WindowsNoEditor.pak")
    PAKS_DIR = os.path.join(GAME_DIR, "Ancestors", "Content", "Paks")
else:
    PAK_FILE = None
    PAKS_DIR = None

MOD_DIR = os.path.join(os.path.expanduser("~"), "ancestors_mod")
OUTPUT_PAK_NAME = "AncestorsDifficultyMod_P.pak"

# ============================================================
# ANIMAL DATABASE
# ============================================================

ANIMALS = {
    "Elephant":     ("Ancestors/Content/Prod/Data/GameSystems/Animals_AI/Elephant/VL01_CDSHealth_Elephant.uasset",              1144, 20.0),
    "Crocodile":    ("Ancestors/Content/Prod/Data/GameSystems/Animals_AI/Crocodile/VL01_CDSHealth_Crocodile.uasset",            1148, 12.0),
    "Buffalo":      ("Ancestors/Content/Prod/Data/GameSystems/Animals_AI/AfricanBuffalo/VL01_CDSHealth_Buffalo.uasset",        1147, 10.0),
    "Hippo":        ("Ancestors/Content/Prod/Data/GameSystems/Animals_AI/Hippo/VL01_CDSHealth_Hippo.uasset",                    1132, 10.0),
    "Rhino":        ("Ancestors/Content/Prod/Data/GameSystems/Animals_AI/WhiteRhino/VL01_CDSHealth_WhiteRhino.uasset",          1152, 10.0),
    "Leopard":      ("Ancestors/Content/Prod/Data/GameSystems/Animals_AI/Leopard/VL01_CDSHealth_Leopard.uasset",                1140,  9.0),
    "Hyena":        ("Ancestors/Content/Prod/Data/GameSystems/Animals_AI/Hyena/VL01_CDSHealth_Hyena.uasset",                    1132,  6.0),
    "Jackal":       ("Ancestors/Content/Prod/Data/GameSystems/Animals_AI/Jackal/VL01_CDSHealth_Jackal.uasset",                  1136,  6.0),
    "Warthog":      ("Ancestors/Content/Prod/Data/GameSystems/Animals_AI/Warthog/VL01_CDSHealth_Warthog.uasset",                1140,  6.0),
    "Gazelle":      ("Ancestors/Content/Prod/Data/GameSystems/Animals_AI/Gazelle/VL01_CDSHealth_Gazelle.uasset",                1140,  4.0),
    "Python":       ("Ancestors/Content/Prod/Data/GameSystems/Animals_AI/Crawlers/Python/VL01_CDSHealth_PythonCrawler.uasset",  1166,  4.0),
    "Giant Otter":  ("Ancestors/Content/Prod/Data/GameSystems/Animals_AI/GiantOtter/VL01_CDSHealth_GiantOtter.uasset",          1152,  3.0),
    "Zebra":        ("Ancestors/Content/Prod/Data/GameSystems/Animals_AI/Zebra/VL01_CDSHealth_Zebra.uasset",                    1132,  3.0),
    "Scolopendra":  ("Ancestors/Content/Prod/Data/GameSystems/Animals_AI/Crawlers/Scolopendra/VL01_Scolopendra_CDSHealth.uasset", 1165, 3.0),
}

# Player vitality: (pak_path, offset, original_value, description)
PLAYER_VITALITY = {
    "pak_path": "Ancestors/Content/Prod/Maps/Volume01/Common/Character/Controller/HumanAI/VL01_HumanAI_Shared_CDSVitality.uasset",
    "params": {
        "Energy Regen/s": (1524, 0.03, "Regeneration d'energie par seconde"),
    }
}

PLAYER_REGIMEN = {
    "pak_path": "Ancestors/Content/Prod/Maps/Volume01/Common/Character/Controller/HumanAI/VL01_HumanAI_Shared_CDSRegimen.uasset",
    "params": {
        "Hours Before Starvation":    (1968, 30.0, "Heures avant danger de mort (faim)"),
        "Minutes Before Death (food)": (2026, 20.0, "Minutes avant mort par faim"),
        "Hours Before Sleep Death":   (2170, 16.0, "Heures avant danger de mort (sommeil)"),
        "Minutes Before Death (sleep)": (2468, 20.0, "Minutes avant mort par sommeil"),
    }
}

# ============================================================
# PRESETS
# ============================================================

PRESETS = {
    "Default (Vanilla)": {
        "animal_multiplier": 1.0,
        "energy_regen": 0.03,
        "hours_starve": 30.0,
        "min_death_food": 20.0,
        "hours_sleep": 16.0,
        "min_death_sleep": 20.0,
    },
    "Easy — Relaxed Exploration": {
        "animal_multiplier": 0.5,
        "energy_regen": 0.10,
        "hours_starve": 120.0,
        "min_death_food": 60.0,
        "hours_sleep": 64.0,
        "min_death_sleep": 60.0,
    },
    "Hard — True Survival": {
        "animal_multiplier": 1.5,
        "energy_regen": 0.02,
        "hours_starve": 18.0,
        "min_death_food": 10.0,
        "hours_sleep": 10.0,
        "min_death_sleep": 10.0,
    },
    "Brutal — Prehistoric Nightmare": {
        "animal_multiplier": 3.0,
        "energy_regen": 0.015,
        "hours_starve": 8.0,
        "min_death_food": 5.0,
        "hours_sleep": 6.0,
        "min_death_sleep": 5.0,
    },
    "God Mode — Invincible": {
        "animal_multiplier": 0.1,
        "energy_regen": 10.0,
        "hours_starve": 9999.0,
        "min_death_food": 9999.0,
        "hours_sleep": 9999.0,
        "min_death_sleep": 9999.0,
    },
}

# ============================================================
# MOD BUILDER
# ============================================================

def extract_asset(pak_path_internal):
    """Extract an asset from the pak file."""
    result = subprocess.run(
        [REPAK, "get", PAK_FILE, pak_path_internal],
        capture_output=True
    )
    if result.returncode != 0:
        raise RuntimeError(f"Failed to extract {pak_path_internal}")
    return bytearray(result.stdout)


def patch_float(data, offset, original, new_value):
    """Patch a float value in asset data."""
    old = struct.unpack_from('<f', data, offset)[0]
    if abs(old - original) > 0.01:
        raise ValueError(f"Unexpected value at offset {offset}: {old} (expected {original})")
    struct.pack_into('<f', data, offset, new_value)


def build_mod(animal_mult, energy_regen, hours_starve, min_death_food, hours_sleep, min_death_sleep):
    """Build the mod pak with given parameters."""
    # Clean mod directory
    ancestors_dir = os.path.join(MOD_DIR, "Ancestors")
    if os.path.exists(ancestors_dir):
        shutil.rmtree(ancestors_dir)

    patched_files = []

    # Patch animal health
    for name, (pak_path, offset, original) in ANIMALS.items():
        data = extract_asset(pak_path)
        new_val = max(0.5, original * animal_mult)
        patch_float(data, offset, original, new_val)

        out_path = os.path.join(MOD_DIR, pak_path)
        os.makedirs(os.path.dirname(out_path), exist_ok=True)
        with open(out_path, 'wb') as f:
            f.write(data)
        patched_files.append(name)

    # Patch player vitality
    vit_path = PLAYER_VITALITY["pak_path"]
    vit_data = extract_asset(vit_path)
    offset, orig, _ = PLAYER_VITALITY["params"]["Energy Regen/s"]
    patch_float(vit_data, offset, orig, energy_regen)
    out_path = os.path.join(MOD_DIR, vit_path)
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, 'wb') as f:
        f.write(vit_data)

    # Patch player regimen
    reg_path = PLAYER_REGIMEN["pak_path"]
    reg_data = extract_asset(reg_path)
    params = PLAYER_REGIMEN["params"]
    patch_float(reg_data, params["Hours Before Starvation"][0], params["Hours Before Starvation"][1], hours_starve)
    patch_float(reg_data, params["Minutes Before Death (food)"][0], params["Minutes Before Death (food)"][1], min_death_food)
    patch_float(reg_data, params["Hours Before Sleep Death"][0], params["Hours Before Sleep Death"][1], hours_sleep)
    patch_float(reg_data, params["Minutes Before Death (sleep)"][0], params["Minutes Before Death (sleep)"][1], min_death_sleep)
    out_path = os.path.join(MOD_DIR, reg_path)
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, 'wb') as f:
        f.write(reg_data)

    # Pack
    output_pak = os.path.join(MOD_DIR, OUTPUT_PAK_NAME)
    result = subprocess.run(
        [REPAK, "pack", "--version", "V5", "--compression", "Zlib",
         "--mount-point", "../../../", MOD_DIR, output_pak],
        capture_output=True, text=True
    )
    if result.returncode != 0:
        raise RuntimeError(f"Pack failed: {result.stderr}")

    return output_pak


def install_mod(pak_path):
    """Copy mod pak to game directory."""
    dest = os.path.join(PAKS_DIR, OUTPUT_PAK_NAME)
    shutil.copy2(pak_path, dest)
    return dest


def uninstall_mod():
    """Remove mod pak from game directory."""
    dest = os.path.join(PAKS_DIR, OUTPUT_PAK_NAME)
    if os.path.exists(dest):
        os.remove(dest)
        return True
    return False


def is_mod_installed():
    """Check if mod is currently installed."""
    return os.path.exists(os.path.join(PAKS_DIR, OUTPUT_PAK_NAME))


# ============================================================
# GUI
# ============================================================

class ModManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title(f"Ancestors — Difficulty Mod Manager v{VERSION}")
        self.root.geometry("720x700")
        self.root.resizable(False, False)
        self.root.configure(bg="#1a1a2e")

        self.style = ttk.Style()
        self.style.theme_use("clam")
        self._configure_styles()

        self.vars = {}
        self._build_ui()
        self._load_preset("Default (Vanilla)")
        self._update_status()

    def _configure_styles(self):
        bg = "#1a1a2e"
        fg = "#e0e0e0"
        accent = "#e94560"
        card = "#16213e"
        entry_bg = "#0f3460"

        self.style.configure(".", background=bg, foreground=fg, font=("Segoe UI", 10))
        self.style.configure("Title.TLabel", font=("Segoe UI", 16, "bold"), foreground=accent, background=bg)
        self.style.configure("Subtitle.TLabel", font=("Segoe UI", 11, "bold"), foreground="#f5c518", background=bg)
        self.style.configure("Card.TFrame", background=card, relief="flat")
        self.style.configure("Card.TLabel", background=card, foreground=fg, font=("Segoe UI", 9))
        self.style.configure("CardTitle.TLabel", background=card, foreground="#f5c518", font=("Segoe UI", 10, "bold"))
        self.style.configure("Value.TLabel", background=card, foreground=accent, font=("Segoe UI", 10, "bold"))
        self.style.configure("Status.TLabel", font=("Segoe UI", 10), background=bg)
        self.style.configure("Installed.TLabel", foreground="#00e676", background=bg, font=("Segoe UI", 10, "bold"))
        self.style.configure("NotInstalled.TLabel", foreground="#ff5252", background=bg, font=("Segoe UI", 10, "bold"))

        self.style.configure("Accent.TButton", font=("Segoe UI", 11, "bold"), background=accent, foreground="white")
        self.style.map("Accent.TButton", background=[("active", "#c73e54")])
        self.style.configure("Preset.TButton", font=("Segoe UI", 9), background=entry_bg, foreground=fg)
        self.style.map("Preset.TButton", background=[("active", "#1a4a8a")])
        self.style.configure("Danger.TButton", font=("Segoe UI", 10), background="#ff5252", foreground="white")
        self.style.map("Danger.TButton", background=[("active", "#d32f2f")])

        self.style.configure("Custom.Horizontal.TScale", background=card, troughcolor=entry_bg)

    def _build_ui(self):
        bg = "#1a1a2e"

        # Header
        header = ttk.Frame(self.root)
        header.pack(fill="x", padx=20, pady=(15, 5))
        ttk.Label(header, text="ANCESTORS", style="Title.TLabel").pack(side="left")
        ttk.Label(header, text="  Difficulty Mod Manager", style="Subtitle.TLabel").pack(side="left", pady=(3, 0))

        # Status bar
        status_frame = ttk.Frame(self.root)
        status_frame.pack(fill="x", padx=20, pady=(0, 10))
        ttk.Label(status_frame, text="Statut: ", style="Status.TLabel").pack(side="left")
        self.status_label = ttk.Label(status_frame, text="...", style="NotInstalled.TLabel")
        self.status_label.pack(side="left")

        # Presets
        preset_frame = ttk.Frame(self.root)
        preset_frame.pack(fill="x", padx=20, pady=(0, 10))
        ttk.Label(preset_frame, text="Presets:", style="Subtitle.TLabel").pack(side="left", padx=(0, 10))
        for name in PRESETS:
            short = name.split(" — ")[0] if " — " in name else name.split(" (")[0]
            btn = ttk.Button(preset_frame, text=short, style="Preset.TButton",
                           command=lambda n=name: self._load_preset(n))
            btn.pack(side="left", padx=3)

        # Scrollable content
        canvas = tk.Canvas(self.root, bg=bg, highlightthickness=0)
        canvas.pack(fill="both", expand=True, padx=20, pady=(0, 5))

        content = ttk.Frame(canvas)
        canvas.create_window((0, 0), window=content, anchor="nw")

        # --- Animals Section ---
        self._section_label(content, "Animaux — Sante")

        animal_card = ttk.Frame(content, style="Card.TFrame", padding=10)
        animal_card.pack(fill="x", pady=(0, 10))

        ttk.Label(animal_card, text="Multiplicateur de sante globale", style="CardTitle.TLabel").grid(row=0, column=0, columnspan=3, sticky="w", pady=(0, 5))

        self.vars["animal_multiplier"] = tk.DoubleVar(value=1.0)
        self.animal_mult_label = ttk.Label(animal_card, text="x1.0", style="Value.TLabel")
        self.animal_mult_label.grid(row=1, column=2, sticky="e")

        slider = ttk.Scale(animal_card, from_=0.1, to=5.0, variable=self.vars["animal_multiplier"],
                          orient="horizontal", style="Custom.Horizontal.TScale",
                          command=lambda v: self._update_animal_label())
        slider.grid(row=1, column=0, columnspan=2, sticky="ew", padx=(0, 10))
        animal_card.columnconfigure(0, weight=1)

        # Animal preview table
        self.animal_preview = ttk.Frame(animal_card, style="Card.TFrame")
        self.animal_preview.grid(row=2, column=0, columnspan=3, sticky="ew", pady=(10, 0))
        self._update_animal_preview()

        # --- Player Energy Section ---
        self._section_label(content, "Joueur — Energie")

        energy_card = ttk.Frame(content, style="Card.TFrame", padding=10)
        energy_card.pack(fill="x", pady=(0, 10))

        self.vars["energy_regen"] = tk.DoubleVar(value=0.03)
        self._slider_row(energy_card, 0, "Regen energie / seconde", self.vars["energy_regen"], 0.005, 10.0, "energy_label", "{:.3f}")

        # --- Player Survival Section ---
        self._section_label(content, "Joueur — Survie")

        survival_card = ttk.Frame(content, style="Card.TFrame", padding=10)
        survival_card.pack(fill="x", pady=(0, 10))

        self.vars["hours_starve"] = tk.DoubleVar(value=30.0)
        self.vars["min_death_food"] = tk.DoubleVar(value=20.0)
        self.vars["hours_sleep"] = tk.DoubleVar(value=16.0)
        self.vars["min_death_sleep"] = tk.DoubleVar(value=20.0)

        self._slider_row(survival_card, 0, "Heures avant famine", self.vars["hours_starve"], 2.0, 9999.0, "starve_label", "{:.0f}h")
        self._slider_row(survival_card, 1, "Minutes avant mort (faim)", self.vars["min_death_food"], 1.0, 9999.0, "death_food_label", "{:.0f}min")
        self._slider_row(survival_card, 2, "Heures avant epuisement", self.vars["hours_sleep"], 2.0, 9999.0, "sleep_label", "{:.0f}h")
        self._slider_row(survival_card, 3, "Minutes avant mort (sommeil)", self.vars["min_death_sleep"], 1.0, 9999.0, "death_sleep_label", "{:.0f}min")

        # Update canvas scroll region
        content.update_idletasks()
        canvas.configure(scrollregion=canvas.bbox("all"))

        # --- Buttons ---
        btn_frame = ttk.Frame(self.root)
        btn_frame.pack(fill="x", padx=20, pady=(5, 15))

        ttk.Button(btn_frame, text="Appliquer le mod", style="Accent.TButton",
                  command=self._apply_mod).pack(side="left", padx=(0, 10), ipady=5, ipadx=15)
        ttk.Button(btn_frame, text="Restaurer (vanilla)", style="Danger.TButton",
                  command=self._restore).pack(side="left", ipady=5, ipadx=10)

        # Credits
        ttk.Label(self.root, text=f"DaddyOurs — Ancestors Modding Project v{VERSION}",
                 font=("Segoe UI", 8), foreground="#555", background="#1a1a2e").pack(pady=(0, 5))

    def _section_label(self, parent, text):
        ttk.Label(parent, text=text, style="Subtitle.TLabel").pack(anchor="w", pady=(10, 3))

    def _slider_row(self, parent, row, label, var, min_val, max_val, label_key, fmt):
        ttk.Label(parent, text=label, style="Card.TLabel").grid(row=row, column=0, sticky="w", pady=3)

        self.__dict__[label_key] = ttk.Label(parent, text="...", style="Value.TLabel")
        self.__dict__[label_key].grid(row=row, column=2, sticky="e", padx=(10, 0))

        slider = ttk.Scale(parent, from_=min_val, to=max_val, variable=var,
                          orient="horizontal", style="Custom.Horizontal.TScale",
                          command=lambda v, k=label_key, f=fmt, va=var: self.__dict__[k].configure(text=f.format(va.get())))
        slider.grid(row=row, column=1, sticky="ew", padx=10)
        parent.columnconfigure(1, weight=1)

        # Initial label update
        self.__dict__[label_key].configure(text=fmt.format(var.get()))

    def _update_animal_label(self):
        mult = self.vars["animal_multiplier"].get()
        self.animal_mult_label.configure(text=f"x{mult:.1f}")
        self._update_animal_preview()

    def _update_animal_preview(self):
        for w in self.animal_preview.winfo_children():
            w.destroy()

        mult = self.vars["animal_multiplier"].get()
        cols = 4
        animals_sorted = sorted(ANIMALS.items(), key=lambda x: -x[1][2])

        for i, (name, (_, _, orig)) in enumerate(animals_sorted):
            new_val = max(0.5, orig * mult)
            color = "#00e676" if new_val < orig else "#ff5252" if new_val > orig else "#e0e0e0"
            text = f"{name}: {new_val:.1f}"
            lbl = tk.Label(self.animal_preview, text=text, fg=color, bg="#16213e",
                          font=("Segoe UI", 8), anchor="w")
            lbl.grid(row=i // cols, column=i % cols, sticky="w", padx=5, pady=1)

    def _load_preset(self, name):
        preset = PRESETS[name]
        self.vars["animal_multiplier"].set(preset["animal_multiplier"])
        self.vars["energy_regen"].set(preset["energy_regen"])
        self.vars["hours_starve"].set(preset["hours_starve"])
        self.vars["min_death_food"].set(preset["min_death_food"])
        self.vars["hours_sleep"].set(preset["hours_sleep"])
        self.vars["min_death_sleep"].set(preset["min_death_sleep"])
        self._update_animal_label()
        self._update_all_labels()

    def _update_all_labels(self):
        self.energy_label.configure(text=f"{self.vars['energy_regen'].get():.3f}")
        self.starve_label.configure(text=f"{self.vars['hours_starve'].get():.0f}h")
        self.death_food_label.configure(text=f"{self.vars['min_death_food'].get():.0f}min")
        self.sleep_label.configure(text=f"{self.vars['hours_sleep'].get():.0f}h")
        self.death_sleep_label.configure(text=f"{self.vars['min_death_sleep'].get():.0f}min")

    def _update_status(self):
        if is_mod_installed():
            self.status_label.configure(text="Mod installe", style="Installed.TLabel")
        else:
            self.status_label.configure(text="Pas de mod (vanilla)", style="NotInstalled.TLabel")

    def _apply_mod(self):
        try:
            # Remove old mods first
            for old_mod in ["GodMode_P.pak", OUTPUT_PAK_NAME]:
                old_path = os.path.join(PAKS_DIR, old_mod)
                if os.path.exists(old_path):
                    os.remove(old_path)

            pak_path = build_mod(
                animal_mult=self.vars["animal_multiplier"].get(),
                energy_regen=self.vars["energy_regen"].get(),
                hours_starve=self.vars["hours_starve"].get(),
                min_death_food=self.vars["min_death_food"].get(),
                hours_sleep=self.vars["hours_sleep"].get(),
                min_death_sleep=self.vars["min_death_sleep"].get(),
            )
            install_mod(pak_path)
            self._update_status()
            messagebox.showinfo("Mod applique",
                "Le mod a ete installe avec succes !\n\n"
                "Lance le jeu pour voir les changements.\n"
                "Pour desinstaller, clique sur 'Restaurer'.")
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de la creation du mod:\n{e}")

    def _restore(self):
        # Remove all mod paks
        removed = []
        for mod_name in ["GodMode_P.pak", OUTPUT_PAK_NAME]:
            path = os.path.join(PAKS_DIR, mod_name)
            if os.path.exists(path):
                os.remove(path)
                removed.append(mod_name)

        self._update_status()
        if removed:
            messagebox.showinfo("Restaure", f"Mod(s) supprime(s): {', '.join(removed)}\n\nLe jeu est revenu en vanilla.")
        else:
            messagebox.showinfo("Rien a faire", "Aucun mod n'etait installe.")


# ============================================================
# MAIN
# ============================================================

def main():
    global GAME_DIR, PAK_FILE, PAKS_DIR, REPAK

    # Check repak
    if not REPAK or not os.path.exists(REPAK):
        root = tk.Tk()
        root.withdraw()
        messagebox.showerror("repak.exe introuvable",
            "repak.exe n'a pas ete trouve.\n\n"
            "Placez repak.exe dans le meme dossier que ce programme,\n"
            "ou installez-le dans ~/tools/repak/")
        root.destroy()
        return

    # Check game directory
    if not GAME_DIR or not os.path.exists(str(PAK_FILE)):
        root = tk.Tk()
        root.withdraw()
        messagebox.showinfo("Jeu non detecte",
            "Le dossier du jeu n'a pas ete detecte automatiquement.\n\n"
            "Veuillez selectionner le dossier d'installation\n"
            "(celui qui contient le dossier 'Ancestors').")
        selected = filedialog.askdirectory(title="Selectionner le dossier du jeu")
        root.destroy()

        if not selected:
            return

        pak_check = os.path.join(selected, "Ancestors", "Content", "Paks", "Ancestors-WindowsNoEditor.pak")
        if not os.path.exists(pak_check):
            root2 = tk.Tk()
            root2.withdraw()
            messagebox.showerror("Dossier invalide",
                f"Le fichier .pak n'a pas ete trouve dans:\n{selected}\n\n"
                "Assurez-vous de selectionner le bon dossier.")
            root2.destroy()
            return

        GAME_DIR = selected
        PAK_FILE = pak_check
        PAKS_DIR = os.path.join(GAME_DIR, "Ancestors", "Content", "Paks")

    os.makedirs(MOD_DIR, exist_ok=True)

    root = tk.Tk()
    app = ModManagerApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
