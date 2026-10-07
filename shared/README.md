# Shared Japanese data

`ja/` is the single source of Japanese word surfaces, semantic categories, form
catalogs, roles/particles and number/counter data. Source XML files reference
these documents using `shared_target`, joining words/forms by stable IDs.
Source overlays contain translations and instruction-language grammar only.
A word is available in a bundle when its ID appears in that bundle's overlay.
Studio writes Japanese edits here and source edits to the selected overlay.
