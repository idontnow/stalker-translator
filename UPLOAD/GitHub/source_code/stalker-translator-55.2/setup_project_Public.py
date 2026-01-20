import os
import json
import sys
from pathlib import Path

# --- LOCALIZATION DICTIONARY ---
LANG = {
    "eng": {
        "TITLE": "S.T.A.L.K.E.R. TRANSLATOR - SETUP WIZARD",
        "DEP_CHECK": "[Dependency Check]", "MISSING": "MISSING", "OK": "OK",
        "STEP_1": "[1/4] Global Settings", "USE_AI": "Use Gemini AI? (y/n)", "API_KEY": "   Gemini API Key", "EDITOR": "Text Editor",
        "STEP_2": "[2/4] Create Project", "PROJ_NAME": "Project Name", "EXISTS": "exists. Overwrite? (y/n)",
        "STEP_3": "[3/4] Paths & Structure", "GAME_DIR": "   GAME TEXT DIR (location of .xml files)", "REF_DIR": "   REFERENCE DIR (Enter if none)",
        "SCANNING": "   🔎 Scanning files...", "FOUND": "   ✅ Found {} .xml files.", "NOT_FOUND": "   ⚠️ Folder not found:", "ERROR": "   ⚠️ Error scanning:",
        "CS_DETECT": "   💡 Detected Clear Sky file structure!", "USE_CS": "   Use CS categories (Story/Map/UI)? (y/n)", "CS_APPLIED": "   ✅ Clear Sky structure applied.", "ALL_ONE_LIST": "   ℹ️ All files put in one list.",
        "STEP_4": "[4/4] Finalize & Localization", "GAME_TITLE": "   Game Title", "LANG_CODE": "   Language Code (e.g. ltu)",
        "FONT_TITLE": "\n   [FONT SETTINGS]", "FONT_Q": "   Which font prefix to use?", "FP_1": "   [1] _cent (Eastern Europe/LT - Recommended)", "FP_2": "   [2] _west (Western Europe)", "FP_3": "   [3] _cent ;_west (Both)", "FP_4": "   [4] Custom", "FP_CHOICE": "   Choice", "FP_ENTER": "   Enter prefix",
        "LTX_GEN": "   ⚙️  Generating localization.ltx at:", "LTX_OK": "   ✅ localization.ltx created/updated successfully!", "LTX_FAIL": "   ⚠️ Failed to write localization.ltx:", "LTX_NO_CONFIGS": "   ⚠️ Could not determine 'configs' folder.",
        "DONE": "\n✅ Setup Complete!", "RUN_NOW": "Now run: Stalker_Translator.exe", "REQUIRED": "❌ This field is required!"
    },
    "ltu": {
        "TITLE": "S.T.A.L.K.E.R. VERTIMO ĮRANKIS - NUSTATYMAI",
        "DEP_CHECK": "[Priklausomybių patikra]", "MISSING": "TRŪKSTA", "OK": "GERAI",
        "STEP_1": "[1/4] Globalūs nustatymai", "USE_AI": "Naudoti Gemini AI? (y/n)", "API_KEY": "   Gemini API Raktas", "EDITOR": "Redaktorius",
        "STEP_2": "[2/4] Projekto kūrimas", "PROJ_NAME": "Projekto pavadinimas", "EXISTS": "egzistuoja. Perrašyti? (y/n)",
        "STEP_3": "[3/4] Failų keliai", "GAME_DIR": "   GAME TEXT DIR (kur yra .xml failai)", "REF_DIR": "   REFERENCE DIR (Enter jei nėra)",
        "SCANNING": "   🔎 Skenuojami failai...", "FOUND": "   ✅ Rasta {} .xml failų.", "NOT_FOUND": "   ⚠️ Aplankas nerastas:", "ERROR": "   ⚠️ Klaida:",
        "CS_DETECT": "   💡 Atpažinta Clear Sky struktūra!", "USE_CS": "   Naudoti CS kategorijas (Story/Map/UI)? (y/n)", "CS_APPLIED": "   ✅ Pritaikyta Clear Sky struktūra.", "ALL_ONE_LIST": "   ℹ️ Visi failai viename sąraše.",
        "STEP_4": "[4/4] Išsaugojimas", "GAME_TITLE": "   Žaidimo pavadinimas", "LANG_CODE": "   Kalbos kodas (pvz. ltu)",
        "FONT_TITLE": "\n   [ŠRIFTO NUSTATYMAI]", "FONT_Q": "   Kokį font_prefix naudoti?", "FP_1": "   [1] _cent (Rytų Europa/LT - Rekomenduojama)", "FP_2": "   [2] _west (Vakarų Europa)", "FP_3": "   [3] _cent ;_west (Abu)", "FP_4": "   [4] Kita (Įrašyti)", "FP_CHOICE": "   Pasirinkimas", "FP_ENTER": "   Įrašykite prefix",
        "LTX_GEN": "   ⚙️  Generuojamas localization.ltx faile:", "LTX_OK": "   ✅ localization.ltx sukurtas sėkmingai!", "LTX_FAIL": "   ⚠️ Nepavyko įrašyti localization.ltx:", "LTX_NO_CONFIGS": "   ⚠️ Nepavyko rasti 'configs' aplanko.",
        "DONE": "\n✅ Viskas paruošta!", "RUN_NOW": "Dabar paleiskite: Stalker_Translator.exe", "REQUIRED": "❌ Šis laukas privalomas!"
    },
    "ukr": {
        "TITLE": "S.T.A.L.K.E.R. TRANSLATOR - НАЛАШТУВАННЯ",
        "DEP_CHECK": "[Перевірка бібліотек]", "MISSING": "ВІДСУТНЄ", "OK": "ОК",
        "STEP_1": "[1/4] Глобальні налаштування", "USE_AI": "Використовувати Gemini AI? (y/n)", "API_KEY": "   Gemini API Ключ", "EDITOR": "Редактор",
        "STEP_2": "[2/4] Створення проекту", "PROJ_NAME": "Назва проекту", "EXISTS": "існує. Перезаписати? (y/n)",
        "STEP_3": "[3/4] Шляхи файлів", "GAME_DIR": "   GAME TEXT DIR (де лежать .xml файли)", "REF_DIR": "   REFERENCE DIR (Enter якщо немає)",
        "SCANNING": "   🔎 Сканування файлів...", "FOUND": "   ✅ Знайдено {} .xml файлів.", "NOT_FOUND": "   ⚠️ Папку не знайдено:", "ERROR": "   ⚠️ Помилка:",
        "CS_DETECT": "   💡 Виявлено структуру Clear Sky!", "USE_CS": "   Використати категорії CS (Story/Map/UI)? (y/n)", "CS_APPLIED": "   ✅ Структура Clear Sky застосована.", "ALL_ONE_LIST": "   ℹ️ Всі файли в одному списку.",
        "STEP_4": "[4/4] Завершення", "GAME_TITLE": "   Назва гри", "LANG_CODE": "   Код мови (напр. ukr)",
        "FONT_TITLE": "\n   [НАЛАШТУВАННЯ ШРИФТУ]", "FONT_Q": "   Який font_prefix використати?", "FP_1": "   [1] _cent (Східна Європа - Рекомендовано)", "FP_2": "   [2] _west (Західна Європа)", "FP_3": "   [3] _cent ;_west (Обидва)", "FP_4": "   [4] Власний", "FP_CHOICE": "   Вибір", "FP_ENTER": "   Введіть prefix",
        "LTX_GEN": "   ⚙️  Створення localization.ltx у:", "LTX_OK": "   ✅ localization.ltx успішно створено!", "LTX_FAIL": "   ⚠️ Помилка запису localization.ltx:", "LTX_NO_CONFIGS": "   ⚠️ Не вдалося знайти папку 'configs'.",
        "DONE": "\n✅ Налаштування завершено!", "RUN_NOW": "Запустіть: Stalker_Translator.exe", "REQUIRED": "❌ Це поле обов'язкове!"
    },
    "rus": {
        "TITLE": "S.T.A.L.K.E.R. TRANSLATOR - НАСТРОЙКА",
        "DEP_CHECK": "[Проверка зависимостей]", "MISSING": "ОТСУТСТВУЕТ", "OK": "ОК",
        "STEP_1": "[1/4] Глобальные настройки", "USE_AI": "Использовать Gemini AI? (y/n)", "API_KEY": "   Gemini API Ключ", "EDITOR": "Редактор",
        "STEP_2": "[2/4] Создание проекта", "PROJ_NAME": "Название проекта", "EXISTS": "существует. Перезаписать? (y/n)",
        "STEP_3": "[3/4] Пути к файлам", "GAME_DIR": "   GAME TEXT DIR (где лежат .xml файлы)", "REF_DIR": "   REFERENCE DIR (Enter если нет)",
        "SCANNING": "   🔎 Сканирование файлов...", "FOUND": "   ✅ Найдено {} .xml файлов.", "NOT_FOUND": "   ⚠️ Папка не найдена:", "ERROR": "   ⚠️ Ошибка:",
        "CS_DETECT": "   💡 Обнаружена структура Clear Sky!", "USE_CS": "   Использовать категории CS (Story/Map/UI)? (y/n)", "CS_APPLIED": "   ✅ Структура Clear Sky применена.", "ALL_ONE_LIST": "   ℹ️ Все файлы в одном списке.",
        "STEP_4": "[4/4] Завершение", "GAME_TITLE": "   Название игры", "LANG_CODE": "   Код языка (напр. rus)",
        "FONT_TITLE": "\n   [НАСТРОЙКИ ШРИФТА]", "FONT_Q": "   Какой font_prefix использовать?", "FP_1": "   [1] _cent (Восточная Европа - Рекомендуется)", "FP_2": "   [2] _west (Западная Европа)", "FP_3": "   [3] _cent ;_west (Оба)", "FP_4": "   [4] Свой", "FP_CHOICE": "   Выбор", "FP_ENTER": "   Введите prefix",
        "LTX_GEN": "   ⚙️  Создание localization.ltx в:", "LTX_OK": "   ✅ localization.ltx успешно создан!", "LTX_FAIL": "   ⚠️ Ошибка записи localization.ltx:", "LTX_NO_CONFIGS": "   ⚠️ Не удалось найти папку 'configs'.",
        "DONE": "\n✅ Настройка завершена!", "RUN_NOW": "Запустите: Stalker_Translator.exe", "REQUIRED": "❌ Это поле обязательно!"
    }
}

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

# --- HELPER: GET REAL PATH FOR EXE ---
def get_base_path():
    if getattr(sys, 'frozen', False):
        return Path(sys.executable).parent
    else:
        return Path(__file__).parent

def check_dependencies():
    print(f"\n{LANG[L_CODE]['DEP_CHECK']}")
    try: import colorama; print(f"✅ colorama: {LANG[L_CODE]['OK']}")
    except: print(f"⚠️  colorama: {LANG[L_CODE]['MISSING']}")
    try: import bs4; print(f"✅ beautifulsoup4: {LANG[L_CODE]['OK']}")
    except: print(f"⚠️  beautifulsoup4: {LANG[L_CODE]['MISSING']}")
    try: from deep_translator import GoogleTranslator; print(f"✅ deep-translator: {LANG[L_CODE]['OK']}")
    except: print(f"⚠️  deep-translator: {LANG[L_CODE]['MISSING']}")
    try: from google import genai; print(f"✅ google-genai: {LANG[L_CODE]['OK']}")
    except: print(f"⚠️  google-genai: {LANG[L_CODE]['MISSING']}")

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
        print(f"\n{LANG[L_CODE]['LTX_GEN']} {ltx_path}")
        content = f"""; Generated by Stalker Translator Tool\n[string_table]\nlanguage\t= {lang_code}\nfont_prefix\t= {font_prefix}\n"""
        try:
            with open(ltx_path, "w", encoding="windows-1250") as f: f.write(content)
            print(LANG[L_CODE]['LTX_OK'])
        except Exception as e: print(f"{LANG[L_CODE]['LTX_FAIL']} {e}")
    except Exception as e: print(f"{LANG[L_CODE]['LTX_NO_CONFIGS']} {e}")

def wizard():
    global L_CODE
    print("\n====================================================")
    print("   Select Language / Pasirinkite kalbą / Оберіть мову")
    print("====================================================")
    print("   [1] English")
    print("   [2] Lietuvių")
    print("   [3] Українська")
    print("   [4] Русский")

    choice = input("👉 ").strip()
    if choice == '2': L_CODE = "ltu"
    elif choice == '3': L_CODE = "ukr"
    elif choice == '4': L_CODE = "rus"
    else: L_CODE = "eng"

    print("\n====================================================")
    print(f"   {LANG[L_CODE]['TITLE']} (v55.2)")
    print("====================================================")

    check_dependencies()

    # SVARBU: Naudojame pataisytą kelią
    base_path = get_base_path()
    config_path = base_path / "config.json"
    projects_dir = base_path / "projects"

    print(f"\n{LANG[L_CODE]['STEP_1']}")
    use_ai = get_input(LANG[L_CODE]['USE_AI'], "n").lower() == 'y'
    api_key = ""
    if use_ai: api_key = get_input(LANG[L_CODE]['API_KEY'])

    # SVARBU: Auto-detect Windows
    default_editor = "notepad" if os.name == 'nt' else "nano"
    editor = get_input(f"{LANG[L_CODE]['EDITOR']} (nano/notepad/code)", default_editor)

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
