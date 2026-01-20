import os
import re
import json
import time
import datetime
import warnings
import logging
import tempfile
import subprocess
import shutil
import sys
from pathlib import Path

# --- DEPENDENCY HANDLING ---
# 1. COLORAMA
try:
    from colorama import init, Fore, Back, Style
    init(autoreset=True)
    HAS_COLOR = True
except ImportError:
    HAS_COLOR = False
    class MockColor:
        def __getattr__(self, name): return ""
    Fore = Back = Style = MockColor()

# 2. BEAUTIFULSOUP (Robust)
HAS_BS4 = False
try:
    from bs4 import BeautifulSoup
    try:
        BeautifulSoup("<t></t>", "xml")
        HAS_BS4 = True
    except Exception:
        HAS_BS4 = False
except ImportError:
    HAS_BS4 = False

# 3. PROMPT_TOOLKIT (The New Internal Editor)
try:
    from prompt_toolkit import prompt
    from prompt_toolkit.formatted_text import HTML
    HAS_PROMPT = True
except ImportError:
    HAS_PROMPT = False

# 4. TRANSLATORS
try: from deep_translator import GoogleTranslator; HAS_GTRANS = True
except ImportError: HAS_GTRANS = False
try: from google import genai; HAS_GENAI = True
except ImportError: HAS_GENAI = False

logging.basicConfig(filename='translator_error.log', level=logging.ERROR, format='%(asctime)s %(message)s')
warnings.filterwarnings("ignore")

# --- UI LANGUAGE DICTIONARY ---
LANG = {
    "eng": {
        "PM_TITLE": "=== PROJECT MANAGER ===", "FOUND_PROJ": "Found projects:", "NO_PROJ": "No projects found. Run ST_Setup.exe", "NO_PROJ_FOLDER": "No 'projects' folder. Run ST_Setup.exe",
        "NEW_PROJ": "[N] Create New Project", "QUIT": "[Q] Quit", "SELECT": "👉 Select project", "INVALID": "Invalid choice.", "CREATE_HINT": "Run 'ST_Setup.exe' to create a project.", "CLOSING": "Closing...",
        "LOADING": "Loading project: {}...", "FILES": "FILES:", "SELECT_FILE": "👉 Select file (0 back)", "NO_FILES": "No files in this segment.", "START": "Start.", "DONE": "Done!",
        "MODE_Q": "Mode [1] Audit, [2] Sanity", "LOCKED_Q": "Locked ({}). Show? [y/N]", "CONTINUE_Q": "Continue {}? [Y/n]",
        "MENU": "[e] Edit [l] Lock [s] Search [b] Back [f] File List [Enter] Next [q] Quit", "TOOL_G": "[g] Google ", "TOOL_A": "[a] AI ",
        "EDIT_PROMPT": "Type translation below (Press Enter to confirm):", "EDIT_OLD": "Original (ENG): "
    },
    "ltu": {
        "PM_TITLE": "=== PROJEKTŲ VALDYMAS ===", "FOUND_PROJ": "Rasti projektai:", "NO_PROJ": "Projektų nerasta. Paleiskite ST_Setup.exe", "NO_PROJ_FOLDER": "Nėra 'projects' aplanko. Paleiskite ST_Setup.exe",
        "NEW_PROJ": "[N] Kurti naują projektą", "QUIT": "[Q] Išeiti", "SELECT": "👉 Pasirinkite projektą", "INVALID": "Neteisingas pasirinkimas.", "CREATE_HINT": "Paleiskite 'ST_Setup.exe' projektui sukurti.", "CLOSING": "Užsidaro...",
        "LOADING": "Užkraunamas projektas: {}...", "FILES": "FAILAI:", "SELECT_FILE": "👉 Pasirinkite failą (0 atgal)", "NO_FILES": "Nėra failų šiame segmente.", "START": "Pradžia.", "DONE": "Viskas!",
        "MODE_Q": "Režimas [1] Auditas, [2] Tikrinimas", "LOCKED_Q": "Užrakinti ({}). Rodyti? [y/N]", "CONTINUE_Q": "Tęsti {}? [Y/n]",
        "MENU": "[e] Redaguoti [l] Užrakinti [s] Paieška [b] Atgal [f] Failai [Enter] Kitas [q] Išeiti", "TOOL_G": "[g] Google ", "TOOL_A": "[a] AI ",
        "EDIT_PROMPT": "Įrašykite vertimą žemiau (Enter patvirtinimui):", "EDIT_OLD": "Originalas (ENG): "
    },
    "ukr": {
        "PM_TITLE": "=== МЕНЕДЖЕР ПРОЕКТІВ ===", "FOUND_PROJ": "Знайдені проекти:", "NO_PROJ": "Проектів не знайдено. Запустіть ST_Setup.exe", "NO_PROJ_FOLDER": "Немає папки 'projects'. Запустіть ST_Setup.exe",
        "NEW_PROJ": "[N] Створити новий проект", "QUIT": "[Q] Вихід", "SELECT": "👉 Оберіть проект", "INVALID": "Невірний вибір.", "CREATE_HINT": "Запустіть 'ST_Setup.exe'", "CLOSING": "Закриття...",
        "LOADING": "Завантаження проекту: {}...", "FILES": "ФАЙЛИ:", "SELECT_FILE": "👉 Оберіть файл (0 назад)", "NO_FILES": "Немає файлів у цьому сегменті.", "START": "Початок.", "DONE": "Готово!",
        "MODE_Q": "Режим [1] Аудит, [2] Перевірка", "LOCKED_Q": "Заблоковані ({}). Показати? [y/N]", "CONTINUE_Q": "Продовжити {}? [Y/n]",
        "MENU": "[e] Редаг [l] Блок [s] Пошук [b] Назад [f] Файли [Enter] Далі [q] Вихід", "TOOL_G": "[g] Google ", "TOOL_A": "[a] AI ",
        "EDIT_PROMPT": "Введіть переклад (Enter для підтвердження):", "EDIT_OLD": "Оригінал (ENG): "
    },
    "rus": {
        "PM_TITLE": "=== МЕНЕДЖЕР ПРОЕКТОВ ===", "FOUND_PROJ": "Найденные проекты:", "NO_PROJ": "Проекты не найдены. Запустите ST_Setup.exe", "NO_PROJ_FOLDER": "Нет папки 'projects'. Запустите ST_Setup.exe",
        "NEW_PROJ": "[N] Создать новый проект", "QUIT": "[Q] Выход", "SELECT": "👉 Выберите проект", "INVALID": "Неверный выбор.", "CREATE_HINT": "Запустите 'ST_Setup.exe'", "CLOSING": "Закрытие...",
        "LOADING": "Загрузка проекта: {}...", "FILES": "ФАЙЛЫ:", "SELECT_FILE": "👉 Выберите файл (0 назад)", "NO_FILES": "Нет файлов в этом сегменте.", "START": "Начало.", "DONE": "Готово!",
        "MODE_Q": "Режим [1] Аудит, [2] Проверка", "LOCKED_Q": "Скрытые ({}). Показать? [y/N]", "CONTINUE_Q": "Продолжить {}? [Y/n]",
        "MENU": "[e] Редакт [l] Блок [s] Поиск [b] Назад [f] Файлы [Enter] Далее [q] Выход", "TOOL_G": "[g] Google ", "TOOL_A": "[a] AI ",
        "EDIT_PROMPT": "Введите перевод (Enter для подтверждения):", "EDIT_OLD": "Оригинал (ENG): "
    }
}

CTX = {"config": {}, "project": {}, "mapping": {}, "segments": {}, "paths": {}, "client": None}
L_CODE = "eng"

# --- CORE LOGIC ---

class RegexParser:
    def __init__(self, content):
        self.content = content
        self.pattern = re.compile(r'(<string\s+id\s*=\s*["\'](.*?)["\']>.*?<text>(.*?)</text>.*?</string>)', re.DOTALL | re.IGNORECASE)
        self.matches = []
        for m in self.pattern.finditer(content):
            self.matches.append({'full_block': m.group(1), 'id': m.group(2), 'text': m.group(3), 'span': m.span(3)})
    def get_tags(self):
        tags = []
        for m in self.matches:
            class MockTag:
                def __init__(self, text, pid):
                    self.string = text
                    self.parent = {'id': pid}
            tags.append(MockTag(m['text'], m['id']))
        return tags
    def update_text(self, str_id, new_text):
        specific_pattern = re.compile(f'(<string\\s+id\\s*=\\s*["\']{re.escape(str_id)}["\']>.*?<text>)(.*?)(</text>)', re.DOTALL | re.IGNORECASE)
        def replacer(match): return f"{match.group(1)}{new_text}{match.group(3)}"
        self.content = specific_pattern.sub(replacer, self.content, count=1)
        return self.content

def get_base_path():
    if getattr(sys, 'frozen', False): return Path(sys.executable).parent
    else: return Path(__file__).parent

def resolve_path(base_path_str):
    if not base_path_str: return None
    path_obj = Path(base_path_str)
    if path_obj.exists(): return str(path_obj)
    return base_path_str

def load_json(path, default=None):
    if default is None: default = {}
    if not os.path.exists(path): return default
    try:
        with open(path, 'r', encoding='utf-8') as f: return json.load(f)
    except: return default

def save_json(path, data):
    with open(path, 'w', encoding='utf-8') as f: json.dump(data, f, indent=4)

def determine_ui_language():
    base_path = get_base_path()
    cfg_path = base_path / "config.json"
    if cfg_path.exists():
        cfg = load_json(cfg_path)
        return cfg.get("ui_language", "eng")
    return "eng"

def project_selection_menu():
    global L_CODE
    base_path = get_base_path()
    projects_dir = base_path / "projects"
    config_path = base_path / "config.json"
    L_CODE = determine_ui_language()

    if not projects_dir.exists():
        print(f"{Fore.RED}{LANG[L_CODE]['NO_PROJ_FOLDER']}{Fore.RESET}"); input("Press Enter..."); sys.exit(0)

    projects = [d.name for d in projects_dir.iterdir() if d.is_dir() and (d / "project.json").exists()]
    if not projects:
        print(f"{Fore.RED}{LANG[L_CODE]['NO_PROJ']}{Fore.RESET}"); input("Press Enter..."); sys.exit(0)

    config = load_json(config_path)
    last_active = config.get("last_active_project", "")

    print(f"\n{Fore.CYAN}{LANG[L_CODE]['PM_TITLE']}{Fore.RESET}")
    print(f"{Fore.YELLOW}{LANG[L_CODE]['FOUND_PROJ']}{Fore.RESET}")

    valid_projects = sorted(projects)
    for i, p_name in enumerate(valid_projects):
        marker = f" {Fore.GREEN}(LAST){Fore.RESET}" if p_name == last_active else " "
        print(f"[{i+1}] {p_name}{marker}")

    print(f"{LANG[L_CODE]['NEW_PROJ']}")
    print(f"{LANG[L_CODE]['QUIT']}")

    default_idx = valid_projects.index(last_active) + 1 if last_active in valid_projects else -1
    prompt = f"{LANG[L_CODE]['SELECT']}" + (f" [{default_idx}]" if default_idx != -1 else "")

    choice = input(f"{prompt}: ").strip().lower()

    if choice == 'n':
        print(f"\n{Fore.GREEN}{LANG[L_CODE]['CREATE_HINT']}{Fore.RESET}"); time.sleep(2); sys.exit(0)
    elif choice == 'q': sys.exit(0)
    elif choice == '' and default_idx != -1: return valid_projects[default_idx - 1]

    try:
        idx = int(choice) - 1
        if 0 <= idx < len(valid_projects):
            selected = valid_projects[idx]
            config["last_active_project"] = selected
            save_json(config_path, config)
            return selected
    except: pass
    print(LANG[L_CODE]['INVALID']); time.sleep(1)
    return project_selection_menu()

def load_configuration(selected_project_name):
    base_path = get_base_path()
    cfg_path = base_path / "config.json"
    proj_dir = base_path / "projects" / selected_project_name

    CTX["config"] = load_json(cfg_path)
    print(f"{Fore.CYAN}{LANG[L_CODE]['LOADING'].format(selected_project_name)}{Fore.RESET}")

    CTX["project"] = load_json(proj_dir / "project.json")
    CTX["mapping"] = load_json(proj_dir / "mapping.json")
    CTX["segments"] = load_json(proj_dir / "segments.json")

    dirs = CTX["project"]["directories"]
    work_dir = resolve_path(dirs["work_dir"])
    CTX["paths"]["lit"] = work_dir
    CTX["paths"]["eng"] = resolve_path(dirs["reference_dir"])
    CTX["paths"]["master"] = os.path.join(work_dir, dirs["backup_master"])
    CTX["paths"]["halt"] = os.path.join(work_dir, dirs["backup_game_ready"])
    CTX["paths"]["orig"] = os.path.join(work_dir, dirs["backup_original"])
    CTX["paths"]["snapshots"] = os.path.join(work_dir, dirs["snapshots"])
    CTX["paths"]["session"] = proj_dir / "translator_session.json"
    CTX["paths"]["whitelist"] = proj_dir / "translator_whitelist.json"

    if HAS_GENAI and CTX["config"].get("api_key") and CTX["config"].get("use_ai"):
        try: CTX["client"] = genai.Client(api_key=CTX["config"]["api_key"])
        except: pass

def downgrade_text(text):
    if not text: return ""
    for bad, good in CTX["mapping"].items(): text = text.replace(bad, good)
    return text.strip()

def make_pretty_xml(xml_str):
    xml_str = re.sub(r'<\?xml.*?\?>', '', xml_str, flags=re.IGNORECASE).strip()
    xml_str = re.sub(r'>\s+<', '><', xml_str)
    for k, v in {'<string_table>': '<string_table>\n', '<string id=': '\t<string id=', '<text>': '\n\t\t<text>', '</string>': '\n\t</string>\n', '</string_table>': '</string_table>'}.items():
        xml_str = xml_str.replace(k, v)
    return re.sub(r'\n\s*\n', '\n', xml_str).strip()

def read_xml_content(filepath):
    for enc in ['utf-8', 'windows-1250', 'windows-1251', 'windows-1257']:
        try:
            with open(filepath, 'r', encoding=enc) as f: return f.read()
        except: continue
    return None

def save_triple_versions(soup_or_content, filename, is_bs4=True):
    enc_m = CTX["project"]["encoding"].get("master", "utf-8")
    enc_p = CTX["project"]["encoding"].get("game_physical", "windows-1250")
    h_fake = CTX["project"]["encoding"].get("game_header_fake", "windows-1251")
    header = f'<?xml version="1.0" encoding="{h_fake}" ?>\n'.encode(enc_p, errors='replace')

    if not os.path.exists(CTX["paths"]["master"]): os.makedirs(CTX["paths"]["master"])
    clean = str(soup_or_content)
    if is_bs4: clean = clean.replace('\u00A0', ' ').replace('\u200B', '')

    with open(os.path.join(CTX["paths"]["master"], filename), "w", encoding=enc_m) as f: f.write(clean)

    pretty = make_pretty_xml(clean); downgraded = downgrade_text(pretty)
    try: body = downgraded.encode(enc_p, errors='replace')
    except: body = downgraded.encode("utf-8")

    if not os.path.exists(CTX["paths"]["halt"]): os.makedirs(CTX["paths"]["halt"])
    with open(os.path.join(CTX["paths"]["halt"], filename), 'wb') as f: f.write(header); f.write(body)
    with open(os.path.join(CTX["paths"]["lit"], filename), 'wb') as f: f.write(header); f.write(body)

def backup_originals():
    if not os.path.exists(CTX["paths"]["orig"]):
        os.makedirs(CTX["paths"]["orig"])
        for f in os.listdir(CTX["paths"]["lit"]):
            if f.endswith(".xml"):
                try: shutil.copy2(os.path.join(CTX["paths"]["lit"], f), os.path.join(CTX["paths"]["orig"], f))
                except: pass

def print_ui(d):
    bar_len = 20; filled = int(bar_len * d['percent'] / 100); bar = "█" * filled + "-" * (bar_len - filled)
    lock = f" {Back.RED}{Fore.WHITE} LOCKED {Style.RESET_ALL}" if d['locked'] else ""
    src = f" {Back.MAGENTA}{Fore.WHITE} MASTER {Style.RESET_ALL}" if d['is_master'] else f" {Back.YELLOW}{Fore.BLACK} GAME {Style.RESET_ALL}"

    print(f"\033[2J\033[H{Fore.CYAN}🛠️  STALKER TRANSLATOR (v0.560){Fore.RESET}")
    print(f"Project: {CTX['config']['last_active_project']} | {d['mode']}")
    print(f"📂 {d['filename']} [{Fore.GREEN}{bar}{Fore.RESET}] {d['percent']}% ({d['current']}/{d['total']}){src}")
    print("-" * 60 + f"\n🔹 ID: {Fore.BLUE}{d['str_id']}{Fore.RESET}{lock}")
    print(f"🇬🇧 {Back.WHITE}{Fore.BLACK} {d['eng']} {Style.RESET_ALL}")
    print(f"📝 {Back.YELLOW}{Fore.BLACK} {d['lit']} {Style.RESET_ALL}")
    print("-" * 60)

    tools = ""
    if HAS_GTRANS: tools += LANG[L_CODE]['TOOL_G']
    if CTX["client"]: tools += LANG[L_CODE]['TOOL_A']
    print(f"{tools}{LANG[L_CODE]['MENU']}")

# --- NEW: UNIFIED INTERNAL EDITOR ---
def run_editor(initial_text, eng_ctx):
    # 1. Check if user configured a custom external editor
    user_editor = CTX["config"].get("editor_command", "internal")

    if user_editor != "internal":
        # EXTERNAL MODE (Notepad/Nano)
        with tempfile.NamedTemporaryFile(suffix=".tmp", mode='w+', encoding='utf-8', delete=False) as tf:
            tf.write(f"# ENG:\n# {eng_ctx}\n# LT:\n# {initial_text}\n# -------------------\n{initial_text}")
            tf_path = tf.name
        try:
            cmd = [user_editor, tf_path]
            if "nano" in user_editor: cmd.insert(1, "+6")
            subprocess.call(cmd)
            with open(tf_path, 'r', encoding='utf-8') as f: l = [x for x in f.readlines() if not x.startswith("#")]
            return "".join(l).strip() or initial_text
        except:
            # Fallback to internal if external fails
            pass
        finally:
            if os.path.exists(tf_path): os.remove(tf_path)

    # 2. INTERNAL MODE (prompt_toolkit)
    # This works in the same window, no popups.
    if HAS_PROMPT:
        print(f"\n{Fore.YELLOW}{LANG[L_CODE]['EDIT_OLD']}{Style.RESET_ALL}{eng_ctx}")
        print(f"{Fore.GREEN}{LANG[L_CODE]['EDIT_PROMPT']}{Style.RESET_ALL}")

        # 'prompt' supports default text (pre-filled with current translation)
        new_text = prompt('> ', default=initial_text)
        return new_text.strip()
    else:
        # Fallback for Survivor Mode (input() is rudimentary but works)
        print(f"\n[SURVIVOR EDITOR]")
        print(f"Original: {eng_ctx}")
        print(f"Current:  {initial_text}")
        print("Enter new text (leave empty to keep current):")
        new_input = input("> ").strip()
        return new_input if new_input else initial_text

def show_file_menu(files, prog_dict):
    print(f"\n{Fore.CYAN}📂 {LANG[L_CODE]['FILES']}{Fore.RESET}")
    for i, f in enumerate(files):
        p = prog_dict.get(f, 0); ps = f"{Fore.GREEN}({p}){Fore.RESET}" if p > 0 else ""
        print(f"[{i+1}] {f} {ps}")
    s = input(f"{LANG[L_CODE]['SELECT_FILE']}: ")
    try:
        i = int(s) - 1
        if 0 <= i < len(files): return files[i]
    except: pass
    return None

def process_file(filename, start_idx=0, whitelist=set()):
    master_p = os.path.join(CTX["paths"]["master"], filename)
    game_p = os.path.join(CTX["paths"]["lit"], filename)
    eng_p = os.path.join(CTX["paths"]["eng"], filename) if CTX["paths"]["eng"] else None

    content = ""; is_master = False
    if os.path.exists(master_p):
        try:
            with open(master_p, 'r', encoding='utf-8') as f: content = f.read(); is_master = True
        except: pass

    if not content: content = read_xml_content(game_p)
    if not content: return "SKIP", 0

    parser_obj = None; tags = []
    use_regex = True
    if HAS_BS4:
        try:
            soup = BeautifulSoup(re.sub(r'<\?xml.*?\?>', '', content, flags=re.IGNORECASE), "xml")
            tags = soup.find_all('text'); parser_obj = soup; use_regex = False
        except: use_regex = True

    if use_regex: parser_obj = RegexParser(content); tags = parser_obj.get_tags()

    eng_dict = {}
    if eng_p and os.path.exists(eng_p):
        eng_c = read_xml_content(eng_p)
        if eng_c:
            try:
                if not use_regex:
                    es = BeautifulSoup(re.sub(r'<\?xml.*?\?>', '', eng_c, flags=re.IGNORECASE), "xml")
                    eng_dict = {t.parent['id']: t.string for t in es.find_all('text') if t.string}
                else: raise Exception
            except:
                e_parser = RegexParser(eng_c)
                for t in e_parser.get_tags(): eng_dict[t.parent['id']] = t.string

    idx = start_idx
    skip_indices = set()
    while idx < len(tags):
        tag = tags[idx]; str_id = tag.parent['id']
        if idx in skip_indices: idx += 1; continue
        lit_txt = tag.string or ""; eng_txt = eng_dict.get(str_id, "")
        is_locked = str_id in whitelist

        ui_data = {
            "mode": SESSION.get("mode", "AUDIT"), "filename": filename,
            "current": idx, "total": len(tags), "percent": int((idx/len(tags))*100),
            "str_id": str_id, "eng": eng_txt, "lit": lit_txt,
            "locked": is_locked, "is_master": is_master
        }

        while True:
            print_ui(ui_data); cmd = input("👉 ").lower()
            if cmd == 'n': idx += 1; break
            elif cmd == 'q': return "QUIT", idx
            elif cmd == 'f': return "FILE_MENU", idx
            elif cmd == 'b': return "BACK", idx
            elif cmd == 'l':
                if is_locked: whitelist.remove(str_id)
                else: whitelist.add(str_id)
                save_json(CTX["paths"]["whitelist"], list(whitelist))
                ui_data['locked'] = not is_locked
            elif cmd == 'e':
                new_txt = run_editor(lit_txt, eng_txt)
                if new_txt != lit_txt:
                    if not use_regex: tag.string = new_txt; save_triple_versions(parser_obj, filename, True)
                    else: u = parser_obj.update_text(str_id, new_txt); save_triple_versions(u, filename, False)
                    lit_txt = new_txt; ui_data['lit'] = new_txt
            elif cmd == 'g' and HAS_GTRANS:
                try:
                    tr = GoogleTranslator(source='auto', target='lt').translate(eng_txt)
                    if not use_regex: tag.string = tr; save_triple_versions(parser_obj, filename, True)
                    else: u = parser_obj.update_text(str_id, tr); save_triple_versions(u, filename, False)
                    ui_data['lit'] = tr
                except: pass
            elif cmd == 'a' and CTX["client"]:
                try:
                    p = f"Translate to {CTX['project']['language_code']}. Keep special symbols. Context: S.T.A.L.K.E.R. Text: {ui_data['eng']}"
                    r = CTX["client"].models.generate_content(model="gemini-2.5-flash", contents=p)
                    tr = r.text.strip()
                    if not use_regex: tag.string = tr; save_triple_versions(parser_obj, filename, True)
                    else: u = parser_obj.update_text(str_id, tr); save_triple_versions(u, filename, False)
                    ui_data['lit'] = tr
                except: pass
            elif cmd == '': idx += 1; break
    return "DONE", len(tags)

SESSION = {}

def main():
    selected_project = project_selection_menu()
    load_configuration(selected_project)
    backup_originals()

    sess = load_json(CTX["paths"]["session"])
    whitelist = set(load_json(CTX["paths"]["whitelist"]))
    files_prog = sess.get("files_progress", {})

    print("\nSegmentai:")
    seg_list = sorted(CTX["segments"].keys())
    for k in seg_list: print(f"[{k}] {CTX['segments'][k]['name']}")
    seg_id = input("👉 [0]: ") or '0'
    files = [f for f in CTX["segments"].get(seg_id, CTX["segments"]["0"])["files"] if os.path.exists(os.path.join(CTX["paths"]["lit"], f))]

    if not files: print(LANG[L_CODE]['NO_FILES']); return

    SESSION["mode"] = "SANITY" if input(f"{LANG[L_CODE]['MODE_Q']}: ") == '2' else "AUDIT"

    ignore_lock = True
    if len(whitelist) > 0 and input(LANG[L_CODE]['LOCKED_Q'].format(len(whitelist))).lower() == 'y': ignore_lock = False

    curr_file = files[0]
    last = sess.get("last_filename")
    if last in files and input(LANG[L_CODE]['CONTINUE_Q'].format(last)).lower() != 'n': curr_file = last

    while True:
        start_line = files_prog.get(curr_file, 0)
        res, last_idx = process_file(curr_file, start_line, whitelist)
        files_prog[curr_file] = last_idx
        sess["last_filename"] = curr_file; sess["files_progress"] = files_prog
        save_json(CTX["paths"]["session"], sess)

        if res == "QUIT": break
        elif res == "FILE_MENU":
            nf = show_file_menu(files, files_prog)
            if nf: curr_file = nf
        elif res == "BACK":
            curr_idx = files.index(curr_file)
            if curr_idx > 0: curr_file = files[curr_idx - 1]
            else: print(LANG[L_CODE]['START']); time.sleep(1)
        elif res == "DONE" or res == "SKIP":
            curr_idx = files.index(curr_file)
            if curr_idx + 1 < len(files): curr_file = files[curr_idx + 1]
            else: print(LANG[L_CODE]['DONE']); break

if __name__ == "__main__":
    main()
