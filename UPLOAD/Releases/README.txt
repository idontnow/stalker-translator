================================================================================
   S.T.A.L.K.E.R. XML TRANSLATOR TOOL
   A professional, community-driven localization tool.
================================================================================

PLATFORMS: Windows | Linux
LICENSE:   MIT

This tool solves the specific headaches of X-Ray engine modding: file encoding
crashes, missing characters, massive XML file navigation, and project management.

================================================================================
   UNIQUE FEATURES & EXAMPLES
================================================================================

1. THE PROJECT MANAGER
   Stop mixing up your files. The tool allows you to create separate workspaces
   for different games or mods.

   * The Problem: You are translating a mod for Clear Sky but also want to fix
     a typo in Shadow of Chernobyl. Usually, you'd have to constantly change
     folders manually.

   * The Solution: When you launch the tool, it asks:
       [1] Clear_Sky_Lithuanian
       [2] SoC_Bugfix_Mod
       [N] Create New Project
     You can switch contexts instantly. Each project keeps its own settings,
     progress, and file paths.

--------------------------------------------------------------------------------

2. THE "HYBRID ENCODING" SYSTEM
   This is the tool's most powerful feature. The X-Ray engine is notorious for
   crashing if it encounters a character it doesn't understand (like UTF-8
   symbols in a non-UTF-8 environment).

   * The Problem: You want to translate a line using special characters (e.g.,
     Lithuanian Ė, Į, Ų). The game crashes or shows "hieroglyphs" because it
     requires 'windows-1250' or 'windows-1251' encoding.

   * The Solution: The tool maintains THREE versions of your file simultaneously:
     1. Master Backup (UTF-8): Keeps your perfect translation with all special
        characters for future editing.
     2. Game-Ready File: Automatically converts unsupported characters (e.g.,
        turns 'Ė' into 'E') based on 'mapping.json' and applies the correct
        Windows encoding headers so the game runs without crashing.
     3. Original Backup: Keeps the source file safe.

--------------------------------------------------------------------------------

3. AI & CLOUD TRANSLATION
   Integrated directly into your workflow. No need to Alt-Tab to a browser.

   * Function: Press [g] for Google Translate or [a] for Gemini AI.

   * Example:
     - Source (Eng): "Don't just stand there, come in!"
     - Press [a] (Gemini): The AI understands the context is S.T.A.L.K.E.R.
       and translates it using appropriate slang for your language.

--------------------------------------------------------------------------------

4. SMART NAVIGATION & PERSISTENCE
   The tool remembers exactly where you left off.

   * The Scenario: You are translating 'st_dialogs_marsh.xml', which has 500
     lines. You stop at line 142 to go to sleep.
   * Next Day: When you load the project, the tool immediately jumps to
     Line 142. You never lose your place.

--------------------------------------------------------------------------------

5. THE SETUP AUTOMATOR
   Manual configuration of 'localization.ltx' is a common source of crashes.

   * The Function: When you run 'ST_Setup.exe', it scans your folder.
   * Example: It detects files like 'st_quests_marsh.xml' and identifies the
     game as Clear Sky. It then asks:
       "Which font prefix to use?
        [1] _cent (Eastern Europe)
        [2] _west (Western Europe)"
   * Result: It automatically generates or updates the
     'gamedata/configs/localization.ltx' file with the correct settings.

--------------------------------------------------------------------------------

6. SURVIVOR MODE
   The tool is built to be "Ironclad."

   * The Scenario: You are on a fresh Windows installation without Python,
     XML libraries, or Admin rights.
   * The Result: The tool detects missing libraries (like 'lxml') and
     automatically switches to an internal Regex Engine. It loses the fancy
     colors and AI features, but the core translation and file saving
     functionality WILL still work.

================================================================================
   QUICK START GUIDE
================================================================================

STEP 1: DOWNLOAD & EXTRACT
   Extract the .zip file anywhere on your computer.

STEP 2: INITIALIZE (ST_Setup.exe)
   Run the setup tool. It will ask for two paths:

   1. GAME TEXT DIR: The folder where you want your new translation files to be.
      (Example: C:\Games\Stalker_CS\gamedata\configs\text\lit)

   2. REFERENCE DIR: The folder where the original files are (e.g., English).
      (Example: C:\Games\Stalker_CS\gamedata\configs\text\eng)

   * The tool will generate the necessary project configuration and the
     'localization.ltx' file.

STEP 3: TRANSLATE (Stalker_Translator.exe)
   1. Launch the translator and select your project.
   2. Press [f] to view the file list and pick a file.
   3. You will see the interface:

      📂 st_items_weapons.xml [██-------] 20%
      ------------------------------------------------------------
      🔹 ID: wpn_ak74_desc
      🇬🇧  Assault rifle, 5.45x39mm. Reliable and common.
      📝  [ Your translation will appear here ]
      ------------------------------------------------------------
      [e] Edit [g] Google [a] AI [Enter] Next

   4. Press [e] to open your text editor (Notepad/Nano).
   5. Type your translation under the commented-out English text. Save and close.
   6. Press [Enter] to verify and move to the next line.

================================================================================
   CONTROLS REFERENCE
================================================================================

[e] Edit ...... Opens current string in text editor.
[f] File Menu . Switch to a different XML file.
[g] Google .... Auto-translate using Google Translate.
[a] AI ........ Context-aware translation (Requires API Key).
[l] Lock ...... Locks the string (prevents accidental changes).
[s] Search .... Find a string by ID or Text content.
[b] Back ...... Go to the previous string.
[q] Quit ...... Saves progress and exits.

================================================================================
   DISCLAIMER
================================================================================

This software is an unofficial fan-made tool. It is not affiliated with or
endorsed by GSC Game World. S.T.A.L.K.E.R. and X-Ray Engine are trademarks
of GSC Game World.
