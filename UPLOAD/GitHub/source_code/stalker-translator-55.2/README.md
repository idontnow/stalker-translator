# ☢️ S.T.A.L.K.E.R. XML Translator Tool

![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20Linux-brightgreen)
![Python](https://img.shields.io/badge/python-3.10+-blue)
![License](https://img.shields.io/badge/license-MIT-orange)

**A professional, community-driven tool for translating S.T.A.L.K.E.R. series games (Shadow of Chernobyl, Clear Sky, Call of Pripyat) and X-Ray engine mods.**

> **NOTE:** This is a **CLI (Command Line Interface)** tool that runs in a terminal window. While primarily tested with *S.T.A.L.K.E.R.: Clear Sky* (for a Lithuanian localization project), the architecture supports all X-Ray engine games.

---

## ✨ Features

* **📂 Project Manager:** Manage multiple translation projects (SoC, CS, CoP, Mods) simultaneously and switch between them easily.
* **🌍 Multilingual Interface:** The tool's menus and setup wizard are available in **English, Lithuanian, Ukrainian, and Russian**.
* **🧠 Smart Navigation:** Remembers exactly where you left off in every file. Includes search functionality and duplicate handling.
* **🛡️ Automated Backups & Encoding:**
    * Keeps a `Master_UTF8` backup to preserve special characters.
    * Automatically converts files to the engine-friendly `windows-1250` encoding with `windows-1251` headers to prevent crashes.
    * Creates manual snapshots of your progress.
* **🔤 Smart Character Mapping:** Automatically remaps unsupported characters (defined in `mapping.json`) to compatible equivalents (e.g., converting `Ė` to `E`) if the game font (`_cent`/`_west`) doesn't support them.
* **🤖 AI Integration:** Optional support for **Google Translate** and **Google Gemini AI** for context-aware translation of slang and lore.
* **🧟 Survivor Mode:** Runs robustly even without external dependencies (in black & white mode with AI features disabled).

---

## 🚀 Download & Install (For Users)

Download the latest standalone version from the [Releases Page](https://github.com/idontnow/stalker-translator/releases/).

1.  Extract the `STALKER_Translator_Tool_vXX.zip` file.
2.  Run **`ST_Setup.exe`** to initialize your project and generate `localization.ltx`.
3.  Run **`Stalker_Translator.exe`** and select your project to start working.

> **⚠️ Windows Users:** Since this is a free open-source tool, it is not digitally signed with a premium certificate. You might see a blue **Windows SmartScreen** warning.
> Click **"More Info"** -> **"Run Anyway"**.

---

## 📖 How to Use (Step-by-Step)

### 1. Preparation
Before starting, ensure you have your game files unpacked or a `gamedata` folder ready.

* **CREATE a Target Folder:** This is where your translated `.xml` files will live.
    * *Example:* `C:\Games\Stalker\gamedata\configs\text\lit` (or `\lat`, `\nl`).
* **(Optional) CHOOSE a Reference Folder:** The original source files to compare against.
    * *Example:* `C:\Games\Stalker\gamedata\configs\text\eng`.

> **IMPORTANT:** The number of files and their filenames in your **Target Folder** MUST match the **Reference Folder**.
>
> *If you are starting from scratch:* Simply copy all `.xml` files from the original `...\text\eng` folder into your new `...\text\lit` folder before running the tool.

### 2. Run the Setup Wizard (`ST_Setup.exe`)
1.  **Select Language:** Choose the tool's interface language (EN/LT/UA/RU).
2.  **Game Text Dir:** Paste the path to your **Target Folder** (from Step 1).
    * *Tip:* In Windows Explorer, right-click the folder -> "Copy as path".
3.  **Reference Dir:** Paste the path to your original files (e.g., `...\text\eng`).
    * *Note:* If left empty, the tool will run in "Single Mode" (translation only, no comparison).
4.  **Font Prefix:** Choose `_cent` (Eastern Europe) or `_west` (Western Europe). The tool will automatically generate/update the `localization.ltx` file for you.

### 3. Translate (`Stalker_Translator.exe`)
1.  Select your configured project from the menu.
2.  **[f] File List:** Choose a file to translate.
3.  **[e] Edit:** Opens the current text block in your default editor (Notepad/Nano).
    * The English text is commented out (`#`) for context.
    * Edit the translation below it, save, and close the editor.
4.  **[g] Google / [a] AI:** Use these hotkeys to auto-translate the current line (requires internet).

---

## 🛠️ For Developers (Python Source)

If you want to run the tool from source code or contribute:

```bash
git clone [https://github.com/idontnow/stalker-translator.git](https://github.com/idontnow/stalker-translator.git)
cd stalker-translator

# Optional: Install dependencies for Colors & AI support
pip install -r requirements.txt

# Run the tools
python setup_project_Public.py
python stalker_translator_Public.py
```

**Note:** The tool supports a "Survivor Mode". Even if you don't install the libraries from requirements.txt, the script will still run using built-in Python tools, but features like UI colors, Google Translate, and Gemini AI API will be disabled.

## 📜 Credits & Acknowledgments

Created by [idontnow](https://github.com/idontnow).

* **GSC Game World:** Huge thanks for creating the legendary **S.T.A.L.K.E.R.** universe and the X-Ray Engine. This tool is a tribute to your work.
* **Development Assistant:** Code logic, architecture, and multilingual support were developed with the assistance of **Google Gemini AI**.
* **Modding Community:** Thanks to all stalkers from various fan forums who documented the X-Ray engine's file structures and "anomalies" over the years.

---

### ⚖️ Disclaimer
This software is an unofficial fan-made tool. It is not affiliated with or endorsed by GSC Game World.

**S.T.A.L.K.E.R.** and **X-Ray Engine** are trademarks of GSC Game World.
