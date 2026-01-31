============================================================
S.T.A.L.K.E.R. XML TRANSLATOR TOOL (v0.561)
============================================================

[ENG] ENGLISH
------------------------------------------------------------
A professional translation tool for S.T.A.L.K.E.R. (X-Ray Engine).
Features: Project Management, Auto-Setup, AI Support, Smart Navigation.

WHATS NEW IN v0.561:
- Stable UI: Clean retro-style interface (ASCII safe).
- Internal Editor: Edit text directly in the terminal window.
- Fixes: 'Back' button and 'Search' are now working perfectly.
- Help: Added command list via [h] key.

QUICK START:
1. Run 'ST_Setup.exe' first.
   - Select your language (EN/LT).
   - It will auto-detect files and create 'localization.ltx'.
2. Run 'Stalker_Translator.exe'.
   - Select your project and start translating.

CONTROLS:
[e] Edit   - Type translation manually (Internal Editor).
[g] Google - Auto-translate with Google.
[a] AI     - Translate with Gemini AI (Context aware).
[l] Lock   - Toggle Lock (prevent accidental changes).
[s] Search - Find string by ID or Text.
[b] Back   - Go to previous line.
[f] Files  - Select another file.
[h] Help   - Show all commands.
[q] Quit   - Save and Exit.

------------------------------------------------------------
[LTU] LIETUVIŲ
------------------------------------------------------------
Profesionalus įrankis S.T.A.L.K.E.R. serijos žaidimų vertimui.

NAUJIENOS (v0.561):
- Stabilumas: Sutvarkyta sąsaja, nebėra "iškraipytų" simbolių.
- Vidinis redaktorius: Galima rašyti vertimą tiesiai lange (be Notepad).
- Pataisymai: Veikia paieška [s] ir grįžimas atgal [b].

KAIP PRADĖTI:
1. Pirmiausia paleiskite 'ST_Setup.exe'.
   - Pasirinkite kalbą (LTU).
   - Programa automatiškai ras failus ir sukurs 'localization.ltx'.
2. Paleiskite 'Stalker_Translator.exe'.
   - Pasirinkite projektą ir pradėkite vertimą.

VALDYMAS:
[e] Redaguoti - Įrašyti vertimą ranka.
[g] Google    - Automatinis Google vertimas.
[a] AI        - Gemini AI vertimas (reikia API rakto).
[l] Užrakinti - Užrakina eilutę nuo pakeitimų.
[s] Paieška   - Rasti tekstą pagal ID.
[b] Atgal     - Grįžti viena eilute atgal.
[f] Failai    - Pasirinkti kitą failą.
[h] Pagalba   - Rodyti komandų sąrašą.
[q] Išeiti    - Išsaugoti ir uždaryti.

============================================================
DEPENDENCIES (OPTIONAL / NEBŪTINA)
============================================================
This tool works in "Survivor Mode" without any dependencies.
For AI and Colors, install:
pip install beautifulsoup4 deep-translator colorama google-genai prompt_toolkit
