# Troubleshooting — Common Problems and Solutions

---

## Game crashes on startup

### "Critical error" dialog at launch

**Cause:** A mod file is corrupted or incompatible.

**Fix:**
1. Delete ALL `_P.pak` files from `[Game]\Ancestors\Content\Paks\`
2. Launch the game to confirm it works without mods
3. Re-apply your mod

**If it still crashes:** Verify game files via Steam (right-click → Properties → Verify integrity).

### Crash after modifying a texture

**Cause:** UE4 textures have internal metadata (mipmap headers, FBulkData structures) between each detail level. Overwriting these bytes corrupts the texture.

**Fix:** Do NOT modify texture bytes directly. Use FModel to export as PNG, edit in an image editor, then reimport with UAssetAPI or the UE4 editor.

**What happens internally:**
```
Texture .uasset structure:
[Header] [Properties] [Mip0 metadata] [Mip0 pixels] [Mip1 metadata] [Mip1 pixels] ...
                       ^^^^^^^^^^^^                   ^^^^^^^^^^^^
                       DO NOT TOUCH THESE              OR THESE
```

---

## Mod has no effect

### Game loads but nothing changed

**Possible causes:**

1. **Missing `_P` suffix** — The pak file MUST end with `_P.pak` (e.g., `MyMod_P.pak`)
2. **Wrong mount point** — Must be `../../../` (three levels up)
3. **Wrong pak version** — Must be V5 with Zlib compression
4. **Wrong internal path** — The file path inside the pak must EXACTLY match the original

**Check your pak:**
```bash
repak info MyMod_P.pak
# Should show: version V5, mount point ../../../, compression Zlib

repak list MyMod_P.pak
# Should show paths like: Ancestors/Content/Prod/Data/...
```

5. **VL01E01.pak override** — The second pak may load AFTER yours and override your changes. Try renaming your mod to `ZZZ_P.pak` to ensure it loads last (alphabetical order).

---

## UModel errors

### "Serializing behind stopper" error

**Cause:** UModel tries to read a mod `.pak` that has a minimal index structure.

**Fix:** Remove all `_P.pak` files from the Paks folder before running UModel. Put them back after you're done exploring.

### "Unversioned" or version mismatch

**Fix:** In UModel settings, set the engine version override to **UE4.20**.

---

## repak errors

### "Failed to pack"

**Cause:** Usually a path issue.

**Fix:**
- Make sure the input directory exists and contains files
- Use forward slashes in paths, even on Windows
- Don't include the pak file itself inside the input directory

### Wrong file size after patching

**Cause:** Your modification changed the number of bytes in the file.

**Fix:** You must NEVER change the file size. Only overwrite existing bytes with the same number of bytes. If you need to change string lengths or add data, use UAssetAPI instead of binary patching.

---

## Python errors

### "No module named tkinter"

**Fix:** Install Python from [python.org](https://www.python.org/downloads/), NOT from the Windows Store. The Windows Store version sometimes lacks tkinter.

Or install it separately:
```bash
pip install tk
```

### "struct.error: unpack requires a buffer of X bytes"

**Cause:** The file you're trying to patch is smaller than expected, or the offset is wrong.

**Fix:** Verify the file size matches what's expected. The offsets in this documentation are for the vanilla game files — if you've already patched the file once, re-extract the original from the pak.

---

## General tips

### Always start fresh
When debugging, always re-extract the original file from the pak. Don't try to patch an already-patched file.

### Test one change at a time
If you're modifying multiple files, test each one individually first to isolate problems.

### Back up before experimenting
```bash
repak info YourMod_P.pak    # Verify before installing
```

### The nuclear option
If everything is broken:
1. Delete all `_P.pak` files from `Content/Paks/`
2. Steam → Right-click game → Properties → Installed Files → Verify integrity
3. Start over

Your save files are in `Ancestors/Saved/SaveGames/` and are separate from the game files.
