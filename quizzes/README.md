# Published Quiz Packages

This directory contains public, distributable copies of Kotomi quiz packages.

Each child directory is one package and contains its `app.json` descriptor plus the Python files listed by `../quiz_update_manifest.json`.

These directories are generated from the private Kotomi repository's `apps/` sources. Do not hand-edit package files here. Make the change in Kotomi, run the quiz publishing tool, then publish the resulting package update here.

Package directories intentionally do not contain hand-maintained README files because every file inside a package is part of its published inventory.

Packages 1.1.8 require Kotomi 1.1.7 for independent Mobile text, button lettering and touch-target sizes. Quiz buttons default to the launcher menu’s 16 sp. Size and behaviour includes Reset sizes and Cancel. Android and KotomiMobile on Windows share these controls.

Pakiety 1.1.8 wymagają Kotomi 1.1.7 do niezależnej regulacji tekstu, napisów przycisków i obszarów dotykowych Mobile. Przyciski quizów mają domyślnie 16 sp, tak jak menu główne. Rozmiar i zachowanie zawiera Przywróć rozmiary oraz Anuluj. Android i KotomiMobile na Windowsie korzystają z tych samych kontrolek.

## Two-package sentence quiz migration

The built-in Quiz catalog contains exactly `grammar` and `lessons`. The launcher
still lists individual Studio profiles; the Quiz Update screen lists executable
packages, not profiles. New sentence quizzes are Content definitions, not new
executable downloads.

Install Application 1.1.11 first, then Content revision 72+, then approve catalog
1.1.13 (Grammar 1.1.12; Lessons unchanged at 1.1.9). Older Content blocks package
retirement. The catalog explicitly retires only the known `verbs`, `adjectives`
and `availability` first-party descriptors and Python code under their managed
package directories, including stale bytecode. Unlisted third-party packages,
settings and saved progress remain. Downloads and hashes are validated before
an atomic replacement/removal transaction; failures roll back the transaction.
Successful cleanup is not offered repeatedly. Restart after Quiz Update.

After installing the new Grammar package, Content below revision 72 and catalogs
that reinstall retired engines are rejected. To return to an older architecture,
restore a complete compatible installation backup, not one channel in isolation.
Application Update does not delete quiz packages, and Quiz Update does not carry
Content XML. Fresh installation archives include only Grammar and Lessons.
