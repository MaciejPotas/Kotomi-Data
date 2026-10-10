# Bounded lexical examples

These checked-in examples are test inputs, not a mirror of shipped Content.
Keep only competing and incompatible words needed by behavioral tests. Never
regenerate this directory when a lesson or production dictionary grows.
Kotomi tests combine these examples with their own static engine fixture.

Tests mutate temporary copies to cover shared references, missing words,
incomplete/mixed contexts and arbitrary lesson counts. Fixture entries do not
assert what any published lesson must contain. Full application persistence
tests combine this supplement with the bounded engine project; data-side
validator tests need only these small XML files.
