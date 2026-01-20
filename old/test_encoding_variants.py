import os
import shutil
from pathlib import Path
import json

# Bandysime šį tekstą įrašyti į "Quit to Windows" mygtuką, kad iškart matytum rezultatą.
TEST_STRING = "TEST: ĄČĘĖĮŠŲŪŽ (Išėjimas)"

def load_json(path):
    with open(path, 'r', encoding='utf-8') as f: return json.load(f)

def run_test_gen():
    base_path = Path(".")
    try:
        config = load_json(base_path / "config.json")
        proj_name = config["last_active_project"]
        proj_dir = base_path / "projects" / proj_name
        project_conf = load_json(proj_dir / "project.json")
    except:
        print("❌ Nerastas konfigas. Paleiskite setup vedlį.")
        return

    work_dir = Path(project_conf["directories"]["work_dir"])
    master_dir = work_dir / project_conf["directories"]["backup_master"]
    target_file = "ui_st_mm.xml" # Pagrindinio meniu failas

    if not (master_dir / target_file).exists():
        print(f"❌ Nerastas {target_file} backup aplanke!")
        return

    print(f"🔬 Generuojami testiniai failai aplanke: {work_dir}")

    # Nuskaitome originalų turinį
    with open(master_dir / target_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Pakeičiame "Quit to Windows" tekstą į mūsų testinį
    # Ieškome string id="ui_mm_quit2windows"
    import re
    pattern = re.compile(r'(<string\s+id\s*=\s*["\']ui_mm_quit2windows["\']>.*?<text>)(.*?)(</text>)', re.DOTALL | re.IGNORECASE)

    # Jei nerandame quit2windows, bandome tiesiog pakeisti pirmą pasitaikiusį stringą testui
    if pattern.search(content):
        content = pattern.sub(fr'\1{TEST_STRING}\3', content)
    else:
        print("⚠️ Nerastas Quit mygtukas, tekstas nebus pakeistas, tik koduotė.")

    # --- VARIANTAS 1: UTF-8 su 1251 Headeriu (Modernus Hack) ---
    # Tai veikė anksčiau pas tave?
    v1_name = "ui_st_mm_VARIANT_1_UTF8.xml"
    header_1251 = '<?xml version="1.0" encoding="windows-1251" ?>\n'
    with open(work_dir / v1_name, 'wb') as f:
        f.write(header_1251.encode('utf-8')) # Headeris
        f.write(content.encode('utf-8'))     # Kūnas UTF-8
    print(f"   Created: {v1_name} (UTF-8 body, 1251 header)")

    # --- VARIANTAS 2: Windows-1257 (Baltic) ---
    # Tai yra standartinė LT koduotė. Jei žaidimas palaiko LT, tai turi būt šitas.
    v2_name = "ui_st_mm_VARIANT_2_WIN1257.xml"
    try:
        with open(work_dir / v2_name, 'wb') as f:
            f.write(header_1251.encode('windows-1257')) # Headeris (koduotas kaip 1257)
            f.write(content.encode('windows-1257'))     # Kūnas 1257
        print(f"   Created: {v2_name} (Windows-1257 body)")
    except UnicodeEncodeError:
        print(f"   ⚠️ Nepavyko sukurti Varianto 2 (kai kurie simboliai netelpa į 1257?)")

    # --- VARIANTAS 3: Windows-1250 (Central Europe) ---
    # Standartas lenkams/čekams. Palaiko Š, Ž, Č, Ą, Ę, bet ne Ė, Į, Ų, Ū.
    # Ė, Į, Ų, Ū keičiame į E, I, U, U.
    v3_name = "ui_st_mm_VARIANT_3_WIN1250.xml"
    charmap_1250 = {'ė':'e', 'Ė':'E', 'į':'i', 'Į':'I', 'ų':'u', 'Ų':'U', 'ū':'u', 'Ū':'U'}
    content_1250 = content
    for k, v in charmap_1250.items(): content_1250 = content_1250.replace(k, v)

    with open(work_dir / v3_name, 'wb') as f:
        f.write(header_1251.encode('windows-1250'))
        f.write(content_1250.encode('windows-1250', errors='replace'))
    print(f"   Created: {v3_name} (Windows-1250 body, Ė->E conversion)")

    print("\n🏁 TESTAVIMO INSTRUKCIJA:")
    print(f"Eikite į: {work_dir}")
    print("Rasite 3 naujus failus. Pervadinkite juos paeiliui į 'ui_st_mm.xml' ir paleiskite žaidimą.")
    print("Žiūrėkite į mygtuką 'Išeiti į Windows' (Quit to Windows).")

if __name__ == "__main__":
    run_test_gen()
