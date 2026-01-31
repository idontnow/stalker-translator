import os
import shutil
import json
import sys
from pathlib import Path

# --- LOCALIZATION DICTIONARY (ASCII SAFE) ---
LANG = {
    "eng": {
        "TITLE": "S.T.A.L.K.E.R. TRANSLATOR - SETUP WIZARD",
        "DEP_CHECK": "[Dependency Check]", "MISSING": "MISSING", "OK": "OK", "INTERNAL": "OK (Internal Engine)",
        "STEP_1": "[1/4] Global Settings", "USE_AI": "Use Gemini AI? (y/n)", "API_KEY": "   Gemini API Key", "EDITOR": "Text Editor",
        "STEP_2": "[2/4] Create Project", "PROJ_NAME": "Project Name", "EXISTS": "exists. Overwrite? (y/n)",
        "STEP_3": "[3/4] Paths & Structure", "GAME_DIR": "   GAME TEXT DIR (location of .xml files)", "REF_DIR": "   REFERENCE DIR (Enter if none)",
        "SCANNING": "   [*] Scanning files...", "FOUND": "   [+] Found {} .xml files.", "NOT_FOUND": "   [-] Folder not found:", "ERROR": "   [-] Error scanning:",
        "CS_DETECT": "   [*] Detected Clear Sky file structure!", "USE_CS": "   Use CS categories (Story/Map/UI)? (y/n)", "CS_APPLIED": "   [+] Clear Sky structure applied.", "ALL_ONE_LIST": "   [i] All files put in one list.",
        "STEP_4": "[4/4] Finalize & Localization", "GAME_TITLE": "   Game Title", "LANG_CODE": "   Language Code (e.g. ltu)",
        "FONT_TITLE": "\n   [FONT SETTINGS]", "FONT_Q": "   Which font prefix to use?", "FP_1": "   [1] _cent (Eastern Europe/LT - Recommended)", "FP_2": "   [2] _west (Western Europe)", "FP_3": "   [3] _cent ;_west (Both)", "FP_4": "   [4] Custom", "FP_CHOICE": "   Choice", "FP_ENTER": "   Enter prefix",
        "LTX_BACKUP": "   [+] Backup created: localization.ltx.bak",
        "LTX_GEN": "   [*] Generating localization.ltx at:", "LTX_OK": "   [+] localization.ltx created/updated successfully!", "LTX_FAIL": "   [-] Failed to write localization.ltx:", "LTX_NO_CONFIGS": "   [-] Could not determine 'configs' folder.",
        "DONE": "\n[+] Setup Complete!", "RUN_NOW": "Now run: Stalker_Translator.exe", "REQUIRED": "[-] This field is required!"
    },
    "ltu": {
        "TITLE": "S.T.A.L.K.E.R. VERTIMO IRANKIS - NUSTATYMAI",
        "DEP_CHECK": "[Priklausomybiu patikra]", "MISSING": "TRUKSTA", "OK": "GERAI", "INTERNAL": "GERAI (Vidinis variklis)",
        "STEP_1": "[1/4] Globalus nustatymai", "USE_AI": "Naudoti Gemini AI? (y/n)", "API_KEY": "   Gemini API Raktas", "EDITOR": "Redaktorius",
        "STEP_2": "[2/4] Projekto kurimas", "PROJ_NAME": "Projekto pavadinimas", "EXISTS": "egzistuoja. Perrasyti? (y/n)",
        "STEP_3": "[3/4] Failu keliai", "GAME_DIR": "   GAME TEXT DIR (kur yra .xml failai)", "REF_DIR": "   REFERENCE DIR (Enter jei nera)",
        "SCANNING": "   [*] Skenuojami failai...", "FOUND": "   [+] Rasta {} .xml failu.", "NOT_FOUND": "   [-] Aplankas nerastas:", "ERROR": "   [-] Klaida:",
        "CS_DETECT": "   [*] Atpazinta Clear Sky struktura!", "USE_CS": "   Naudoti CS kategorijas (Story/Map/UI)? (y/n)", "CS_APPLIED": "   [+] Pritaikyta Clear Sky struktura.", "ALL_ONE_LIST": "   [i] Visi failai viename sarase.",
        "STEP_4": "[4/4] Issaugojimas", "GAME_TITLE": "   Zaidimo pavadinimas", "LANG_CODE": "   Kalbos kodas (pvz. ltu)",
        "FONT_TITLE": "\n   [SRIFTO NUSTATYMAI]", "FONT_Q": "   Koki font_prefix naudoti?", "FP_1": "   [1] _cent (Rytu Europa/LT - Rekomenduojama)", "FP_2": "   [2] _west (Vakaru Europa)", "FP_3": "   [3] _cent ;_west (Abu)", "FP_4": "   [4] Kita (Irasyti)", "FP_CHOICE": "   Pasirinkimas", "FP_ENTER": "   Irasykite prefix",
        "LTX_BACKUP": "   [+] Sukurta kopija: localization.ltx.bak",
        "LTX_GEN": "   [*] Generuojamas localization.ltx faile:", "LTX_OK": "   [+] localization.ltx sukurtas sekmingai!", "LTX_FAIL": "   [-] Nepavyko irasyti localization.ltx:", "LTX_NO_CONFIGS": "   [-] Nepavyko rasti 'configs' aplanko.",
        "DONE": "\n[+] Viskas paruosta!", "RUN_NOW": "Dabar paleiskite: Stalker_Translator.exe", "REQUIRED": "[-] Sis laukas privalomas!"
    }
}
LANG["ukr"] = LANG["eng"]; LANG["rus"] = LANG["eng"]

# --- PRESETS ---
CS_PRESET = {
    "0": {"name": "UI & System", "files": ["ui_st_credits.xml", "ui_st_inventory.xml", "ui_st_keybinding.xml", "ui_st_mm.xml", "ui_st_mp.xml", "ui_st_other.xml", "ui_st_pda.xml", "ui_st_pda_tutorial.xml", "ui_st_screen.xml", "st_items_artefacts.xml", "st_items_equipment.xml", "st_items_outfit.xml", "st_items_quest.xml", "st_items_weapons.xml", "st_items_weapons_upgrades.xml", "mp_st_adip_map.xml", "st_mp_mapdesc.xml", "st_mp_speechmenu.xml", "st_mp_teamdesc.xml"]},
    "1": {"name": "Prologue: Swamps", "files": ["st_dialogs_marsh.xml", "st_characters_marsh.xml", "st_land_names_marsh.xml", "st_quests_marsh.xml"]},
    "2": {"name": "The South: Cordon & Garbage", "files": ["st_dialogs_escape.xml", "st_characters_escape.xml", "st_land_names_escape.xml", "st_quests_escape.xml", "st_dialogs_garbage.xml", "st_characters_garbage.xml", "st_land_names_garbage.xml", "st_quests_garbage.xml"]},
    "3": {"name": "Faction Wars", "files": ["st_dialogs_darkvalley.xml", "st_characters_darkvalley.xml", "st_land_names_darkvalley.xml", "st_quests_darkvalley.xml", "st_dialogs_agroprom.xml", "st_characters_agroprom.xml", "st_land_names_agroprom.xml", "st_quests_agroprom.xml", "st_dialogs_agroprom_underground.xml", "st_quests_agroprom_underground.xml"]},
    "4": {"name": "Science & Red Forest", "files": ["st_dialogs_yantar.xml", "st_characters_yantar.xml", "st_land_names_yantar.xml", "st_quests_yantar.xml", "st_dialogs_redforest.xml", "st_characters_redforest.xml", "st_land_names_redforest.xml", "st_quests_red_forest.xml"]},
    "5": {"name": "Path to North", "files": ["st_dialogs_military.xml", "st_characters_military.xml", "st_land_names_military.xml", "st_quests_military.xml", "st_dialogs_limansk.xml", "st_characters_limansk.xml", "st_land_names_limansk.xml", "st_quests_limansk.xml"]},
    "6": {"name": "Endgame", "files": ["st_dialogs_hospital.xml", "st_characters_hospital.xml", "st_land_names_hospital.xml", "st_quests_hospital.xml", "st_dialogs.xml", "st_quests_katacomb.xml"]},
    "7": {"name": "Misc & System", "files": ["st_characters.xml", "st_dialog_manager.xml", "st_generate_fnames.xml", "st_generate_snames.xml", "st_smart_terrain_names.xml", "st_subtitles.xml", "st_treasures.xml", "st_quests_general.xml"]},
    "9": {"name": "ALL FILES (A-Z)", "files": []}
}

DEFAULT_CHAR_MAP = {'ė':'e', 'Ė':'E', 'į':'i', 'Į':'I', 'ų':'u', 'Ų':'U', 'ū':'u', 'Ū':'U', '„':'"', '“':'"', '–':'-', '—':'-', '…':'...', '\u00A0':' ', '\u200B':''}
L_CODE = "eng"

def get_base_path():
    if getattr(sys, 'frozen', False): return Path(sys.executable).parent
    else: return Path(__file__).parent

def check_dependencies():
    print(f"\n{LANG[L_CODE]['DEP_CHECK']}")
    try: import colorama; print(f"[+] colorama: {LANG[L_CODE]['OK']}")
    except: print(f"[-] colorama: {LANG[L_CODE]['MISSING']}")

    try:
        from bs4 import BeautifulSoup
        try:
            BeautifulSoup("<t></t>", "xml")
            print(f"[+] beautifulsoup4 (XML): {LANG[L_CODE]['OK']}")
        except:
             print(f"[+] beautifulsoup4: {LANG[L_CODE]['INTERNAL']}")
    except: print(f"[-] beautifulsoup4: {LANG[L_CODE]['MISSING']}")

    try: from deep_translator import GoogleTranslator; print(f"[+] deep-translator: {LANG[L_CODE]['OK']}")
    except: print(f"[-] deep-translator: {LANG[L_CODE]['MISSING']}")
    try: from google import genai; print(f"[+] google-genai: {LANG[L_CODE]['OK']}")
    except: print(f"[-] google-genai: {LANG[L_CODE]['MISSING']}")

def get_input(prompt, default=None):
    d_text = f" [{default}]" if default else ""
    while True:
        val = input(f"{prompt}{d_text}: ").strip()
        if val: return val
        if default is not None: return default
        print(LANG[L_CODE]['REQUIRED'])

def create_localization_ltx(work_dir, lang_code, font_prefix):
    try:
        text_dir = Path(work_dir)
        configs_dir = text_dir.parent.parent
        if configs_dir.name != "configs": configs_dir = text_dir.parent
        ltx_path = configs_dir / "localization.ltx"

        if ltx_path.exists():
            try:
                backup_path = ltx_path.with_suffix(".ltx.bak")
                shutil.copy2(ltx_path, backup_path)
                print(LANG[L_CODE]['LTX_BACKUP'])
            except: pass

        print(f"\n{LANG[L_CODE]['LTX_GEN']} {ltx_path}")
        content = f"""; Generated by S.T.A.L.K.E.R. Translator Tool\n[string_table]\nlanguage\t= {lang_code}\nfont_prefix\t= {font_prefix}\n"""
        try:
            with open(ltx_path, "w", encoding="windows-1250") as f: f.write(content)
            print(LANG[L_CODE]['LTX_OK'])
        except Exception as e: print(f"{LANG[L_CODE]['LTX_FAIL']} {e}")
    except Exception as e: print(f"{LANG[L_CODE]['LTX_NO_CONFIGS']} {e}")

def wizard():
    global L_CODE
    print("\n====================================================")
    print("   Select Language / Pasirinkite kalba")
    print("====================================================")
    print("   [1] English")
    print("   [2] Lietuviu")

    choice = input(">> ").strip()
    if choice == '2': L_CODE = "ltu"
    else: L_CODE = "eng"

    print("\n====================================================")
    print(f"   {LANG[L_CODE]['TITLE']} (v0.561)")
    print("====================================================")

    check_dependencies()
    base_path = get_base_path()
    config_path = base_path / "config.json"
    projects_dir = base_path / "projects"

    print(f"\n{LANG[L_CODE]['STEP_1']}")
    use_ai = get_input(LANG[L_CODE]['USE_AI'], "n").lower() == 'y'
    api_key = ""
    if use_ai: api_key = get_input(LANG[L_CODE]['API_KEY'])

    editor = get_input(f"{LANG[L_CODE]['EDITOR']} (internal/nano/notepad)", "internal")

    config_data = {"last_active_project": "", "api_key": api_key, "use_ai": use_ai, "editor_command": editor, "daily_char_limit": 1000000, "ui_language": L_CODE}

    print(f"\n{LANG[L_CODE]['STEP_2']}")
    proj_name = get_input(LANG[L_CODE]['PROJ_NAME'], "stalker_project")
    proj_dir = projects_dir / proj_name
    if proj_dir.exists():
        if get_input(f"   '{proj_name}' {LANG[L_CODE]['EXISTS']}", "n").lower() != 'y': return
    proj_dir.mkdir(parents=True, exist_ok=True)

    print(f"\n{LANG[L_CODE]['STEP_3']}")
    work_dir = get_input(LANG[L_CODE]['GAME_DIR'])
    ref_dir = get_input(LANG[L_CODE]['REF_DIR'], "")
    print(LANG[L_CODE]['SCANNING'])

    found_files = []
    try:
        if os.path.exists(work_dir):
            found_files = sorted([f for f in os.listdir(work_dir) if f.lower().endswith('.xml')])
            print(LANG[L_CODE]['FOUND'].format(len(found_files)))
        else: print(f"{LANG[L_CODE]['NOT_FOUND']} {work_dir}")
    except Exception as e: print(f"{LANG[L_CODE]['ERROR']} {e}")

    segments_data = {}
    is_clear_sky = "st_dialogs_marsh.xml" in found_files or "st_quests_marsh.xml" in found_files

    if is_clear_sky:
        print(LANG[L_CODE]['CS_DETECT'])
        if get_input(LANG[L_CODE]['USE_CS'], "y").lower() == 'y':
            segments_data = CS_PRESET.copy(); segments_data["9"]["files"] = found_files
            print(LANG[L_CODE]['CS_APPLIED'])
        else: segments_data = {"0": {"name": "All Files", "files": found_files}}
    else:
        segments_data = {"0": {"name": "All Files", "files": found_files}}
        if found_files: print(LANG[L_CODE]['ALL_ONE_LIST'])

    print(f"\n{LANG[L_CODE]['STEP_4']}")
    game_name = get_input(LANG[L_CODE]['GAME_TITLE'], "S.T.A.L.K.E.R. Clear Sky" if is_clear_sky else "S.T.A.L.K.E.R.")
    lang_code = get_input(LANG[L_CODE]['LANG_CODE'], "ltu")

    print(LANG[L_CODE]['FONT_TITLE'])
    print(LANG[L_CODE]['FONT_Q'])
    print(LANG[L_CODE]['FP_1']); print(LANG[L_CODE]['FP_2']); print(LANG[L_CODE]['FP_3']); print(LANG[L_CODE]['FP_4'])
    fp_choice = get_input(LANG[L_CODE]['FP_CHOICE'], "1")
    font_prefix = "_cent"
    if fp_choice == '2': font_prefix = "_west"
    elif fp_choice == '3': font_prefix = "_cent ;_west"
    elif fp_choice == '4': font_prefix = get_input(LANG[L_CODE]['FP_ENTER'])

    create_localization_ltx(work_dir, lang_code, font_prefix)

    project_data = {
        "game_name": game_name, "language_code": lang_code, "font_prefix": font_prefix,
        "directories": {
            "work_dir": work_dir, "reference_dir": ref_dir,
            "backup_master": "Master_UTF8_Backup", "backup_game_ready": "HALT_Backup",
            "backup_original": "Original_Backup", "snapshots": "User_Snapshots"
        },
        "encoding": {"master": "utf-8", "game_physical": "windows-1250", "game_header_fake": "windows-1251"}
    }

    with open(config_path, "w", encoding="utf-8") as f: json.dump(config_data, f, indent=4)
    with open(proj_dir / "project.json", "w", encoding="utf-8") as f: json.dump(project_data, f, indent=4)
    with open(proj_dir / "mapping.json", "w", encoding="utf-8") as f: json.dump(DEFAULT_CHAR_MAP, f, indent=4, ensure_ascii=False)
    with open(proj_dir / "segments.json", "w", encoding="utf-8") as f: json.dump(segments_data, f, indent=4)
    config_data["last_active_project"] = proj_name
    with open(config_path, "w", encoding="utf-8") as f: json.dump(config_data, f, indent=4)

    print(LANG[L_CODE]['DONE'])
    print(LANG[L_CODE]['RUN_NOW'])

if __name__ == "__main__":
    wizard()
