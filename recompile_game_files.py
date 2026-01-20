import os
import json
import re
from pathlib import Path

# --- VARIANTO 3 LOGIKA (Windows-1250) ---
# Keičiame TIK tas raides, kurių nėra Windows-1250 koduotėje.
# Š, Ž, Č, Ą, Ę - PALIEKAME, nes jos veikia!
CHAR_MAP = {
    'ė': 'e', 'Ė': 'E',
    'į': 'i', 'Į': 'I',
    'ų': 'u', 'Ų': 'U',
    'ū': 'u', 'Ū': 'U',
    '„': '"', '“': '"', '–': '-', '—': '-', '…': '...', '\u00A0': ' ', '\u200B': ''
}

def load_json(path):
    with open(path, 'r', encoding='utf-8') as f: return json.load(f)

def downgrade_text(text):
    if not text: return ""
    for bad, good in CHAR_MAP.items():
        text = text.replace(bad, good)
    return text

def make_pretty_xml(xml_str):
    xml_str = re.sub(r'<\?xml.*?\?>', '', xml_str, flags=re.IGNORECASE).strip()
    xml_str = re.sub(r'>\s+<', '><', xml_str)
    xml_str = xml_str.replace('<string_table>', '<string_table>\n')
    xml_str = xml_str.replace('<string id=', '\t<string id=')
    xml_str = xml_str.replace('<text>', '\n\t\t<text>')
    xml_str = xml_str.replace('</string>', '\n\t</string>\n')
    xml_str = xml_str.replace('</string_table>', '</string_table>')
    return re.sub(r'\n\s*\n', '\n', xml_str).strip()

def recompile():
    base_path = Path(".")
    try:
        config = load_json(base_path / "config.json")
        proj_name = config["last_active_project"]
        proj_dir = base_path / "projects" / proj_name
        project_conf = load_json(proj_dir / "project.json")
    except:
        print("❌ Konfigūracijos klaida.")
        return

    work_dir = Path(project_conf["directories"]["work_dir"])
    master_dir = work_dir / project_conf["directories"]["backup_master"]

    # --- FIKS狈OTA SĖKMINGA KONFIGŪRACIJA ---
    enc_master = "utf-8"
    enc_phys = "windows-1250"      # FIZINĖ: Central Europe
    header_fake_str = "windows-1251" # HEADERIS: Kirilica (kad necrashintų)

    header = f'<?xml version="1.0" encoding="{header_fake_str}" ?>\n'.encode(header_fake_str)

    print(f"🚀 Master Backup -> Game Files")
    print(f"⚙️  Logika: Windows-1250 (Palaiko: Š, Ž, Č, Ą, Ę. Keičia: Ė, Į, Ų, Ū)")

    if not master_dir.exists(): return

    count = 0
    files = [f for f in os.listdir(master_dir) if f.endswith(".xml")]

    for fname in files:
        try:
            with open(master_dir / fname, 'r', encoding=enc_master) as f:
                content = f.read()

            clean_content = make_pretty_xml(content)
            final_text = downgrade_text(clean_content)

            # Svarbu: errors='replace' jei netyčia liktų koks simbolis
            body = final_text.encode(enc_phys, errors='replace')

            with open(work_dir / fname, 'wb') as f:
                f.write(header)
                f.write(body)
            count += 1
            print(f"   ✅ {fname}")
        except Exception as e:
            print(f"   ❌ {fname}: {e}")

    print(f"\n✨ Baigta! Failų: {count}")

if __name__ == "__main__":
    recompile()
