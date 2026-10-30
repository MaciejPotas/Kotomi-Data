# Published Quiz Packages

This directory contains public, distributable copies of Kotomi quiz packages.

Each child directory is one package and contains its `app.json` descriptor plus the Python files listed by `../quiz_update_manifest.json`.

These directories are generated from the private Kotomi repository's `apps/` sources. Do not hand-edit package files here. Make the change in Kotomi, run the quiz publishing tool, then publish the resulting package update here.

Package directories intentionally do not contain hand-maintained README files because every file inside a package is part of its published inventory.

Packages 1.1.8 require Kotomi 1.1.7 for independent Mobile text, button lettering and touch-target sizes. Quiz buttons default to the launcher menu’s 16 sp. Size and behaviour includes Reset sizes and Cancel. Android and KotomiMobile on Windows share these controls.

Pakiety 1.1.8 wymagają Kotomi 1.1.7 do niezależnej regulacji tekstu, napisów przycisków i obszarów dotykowych Mobile. Przyciski quizów mają domyślnie 16 sp, tak jak menu główne. Rozmiar i zachowanie zawiera Przywróć rozmiary oraz Anuluj. Android i KotomiMobile na Windowsie korzystają z tych samych kontrolek.
