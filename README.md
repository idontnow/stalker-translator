# ☢️ S.T.A.L.K.E.R. XML Translator Tool

![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20Linux-brightgreen)
![Version](https://img.shields.io/badge/version-0.561-blue)
![License](https://img.shields.io/badge/license-MIT-orange)

**A professional, community-driven tool designed to streamline the localization process for S.T.A.L.K.E.R. (Shadow of Chernobyl, Clear Sky, Call of Pripyat) and X-Ray Engine mods.**

> **NOTE:** This is a **CLI (Command Line Interface)** tool. It is designed to be lightweight, fast, and keyboard-driven.

---

## ✨ Features (v0.561)

* **🛡️ Robust Encoding:** Automatically handles `windows-1250/1251` encoding to prevent game crashes, while keeping a UTF-8 master backup.
* **📂 Project Manager:** Switch between different mods or games instantly.
* **🖥️ Retro CLI Interface:** Clean, hacker-style terminal UI that works perfectly on Windows CMD and Linux (Wine).
* **📝 Internal Editor:** Edit translations directly in the tool without opening pop-up windows (powered by `prompt_toolkit`).
* **🤖 AI Integration:** Built-in support for **Google Translate** and **Gemini AI** for context-aware translation.
* **🧠 Smart Navigation:** Remembers your position in every file. Includes Search (`s`) and Audit/Sanity modes.
* **🧟 Survivor Mode:** Runs robustly even without external dependencies (in black & white mode with AI features disabled).

---

## 🚀 Quick Start (Windows)

1.  Download the latest `.zip` from the **[Releases Page](../../releases)**.
2.  Extract the archive.
3.  Run **`ST_Setup.exe`** to initialize your project.
4.  Run **`Stalker_Translator.exe`** to start translating.

> **⚠️ Note:** Since this is an open-source tool, Windows SmartScreen might show a warning. Click **"More Info"** -> **"Run Anyway"**.

---

## ⌨️ Controls

| Key | Action | Description |
| :--- | :--- | :--- |
| **`e`** | **Edit** | Type translation manually (Internal Editor). |
| **`g`** | **Google** | Auto-translate using Google Translate. |
| **`a`** | **AI** | Context-aware translation (Gemini). |
| **`l`** | **Lock** | Toggle string lock (prevent accidental edits). |
| **`s`** | **Search** | Find a string by ID or Text content. |
| **`b`** | **Back** | Go to the previous line. |
| **`f`** | **Files** | Switch to a different XML file. |
| **`h`** | **Help** | Show command list. |
| **`q`** | **Quit** | Save progress and exit. |

---

# 🛠️ For Developers

To run from source:
```bash
git clone [https://github.com/idontnow/stalker-translator.git](https://github.com/idontnow/stalker-translator.git)
pip install -r requirements.txt
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
