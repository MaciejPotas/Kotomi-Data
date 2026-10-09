# Grammar contexts and shared selections

A selection alias chooses a word once. `noun@item` is one noun selection and
`adjective@quality` is one adjective selection, even when each occurs twice.
`OccurrenceId` addresses a token by template part and index. A grammar context
connects local noun, quantity, predicate and optional adjective realizations.
These are three different identities. Context names never create lexical slots.

## Addressing

Declare a source context with `occurrence:left` on its counted, governed noun.
Use `occurrence:left` on other members or qualify their edges, for example
`agree:@item#left`. A qualifier means the effective realization of that alias
in that context. It does not select another noun. All edges of a constituent
must address the same context. Unqualified `agree:@item` remains sufficient
when the noun has one context; with several contexts it is an error.

The source quantity also uses `case:@item#left`: its numeral case is the
construction case. The adjective omits `case`, because contextual `agree`
supplies its effective noun class and case together. For five books this is
plural genitive even though the affirmative construction is nominative.
Outside a counted construction, explicit agreement and case retain their
independent meanings. Ordinary verbs, questions and Japanese counters use the
same existing operations as before.

The planner recognizes constructions by declared dependencies and the
`existential` feature. There is one current semantics: the former
`semantics_version` field and XML attribute have been removed, without a
replacement mode. XML schema, app version and Content revision are independent.

## Working canonical pattern

```xml
<sentence_pattern id="Dwie policzone grupy opisanych rzeczowników" category="counting">
      <question>{verb@existence[role:subject, feature:existential, form, occurrence:left, agree:@left_count#left].translation} {number@left_count[set:one_to_ten, occurrence:left, agree:@item#left, case:@item#left].translation} {adjective@quality[form:attributive_nonpast, occurrence:left, agree:@item#left].translation} {noun@item[occurrence:left, quantity:@left_count#left, government:@existence#left]}, a obok {verb@existence[role:subject, feature:existential, form, occurrence:right, agree:@right_count#right].translation} {number@right_count[set:one_to_ten, occurrence:right, agree:@item#right, case:@item#right].translation} {adjective@quality[form:attributive_nonpast, occurrence:right, agree:@item#right].translation} {noun@item[occurrence:right, quantity:@right_count#right, government:@existence#right]}.</question>
      <answer>{adjective@quality[form:attributive_nonpast]}{noun@item}が{counter@unit[counts:@item, preferred, quantity:@left_count]}{verb@existence[role:subject, feature:existential, form]}。そのとなりに{adjective@quality[form:attributive_nonpast]}{noun@item}が{counter@unit[counts:@item, preferred, quantity:@right_count]}{verb@existence[role:subject, feature:existential, form]}。</answer>
    </sentence_pattern>
```

This pattern is included in the existing `counting` (Liczenie) quiz. The Japanese
answer uses two sentences with そのとなりに (next to it/that group); both clauses
retain adjective, noun, quantity and the ordinary ある/いる selection. No new
counter engine or lexical copies are needed.

With book, akai, left=1, right=5 and past_plain the engine produces:

> Była jedna czerwona książka, a obok było pięć czerwonych książek.
>
> あかいほんがいっさつあった。そのとなりにあかいほんがごさつあった。

The two choices are `number@left_count` and `number@right_count`; `noun@item`,
`adjective@quality`, `verb@existence` and `counter@unit` are shared selections.

## Planning and rendering

`RealizationPlan.constructions` contains independent grammatical bindings.
`occurrence_requests` addresses each required output by `OccurrenceId`. The
string-keyed request/replacement view is retained only for existing trace and
inspection consumers. Rendering assembles occurrence values with
`render_occurrences`, without parsing inserted text again. Braces in a selected
value are text. A rendered result is never cached by lexical slot alone.

A context with missing dependencies is Pending and cannot prune a valid partial
selection. A complete context without required lexical forms is Unsupported.
The existing MRV/backtracking solver checks ready requests; its terminal gate
requires all mandatory contexts. Preview, explanations, enumeration, statistics,
quiz generation and bound rendering use the same plan and language operation.
Per-search caches stay bounded. Generated numeric ranges stay lazy and intersect
the finite source-numeral catalog, rather than scanning every integer.

Pass a preview's words, entities, forms and context selection to bound rendering.
A dynamic predicate still needs explicit form overrides. Both clauses can share
tense and polarity. Statement-initial capitalization is a neutral structural
input: the first predicate is capitalized only when its token is preceded solely
by whitespace in the source template. Embedded predicates retain catalog case;
no whole-fragment lowercasing or output punctuation guessing is used.

Composite expansion scopes context names alongside the existing `embedded_*`
aliases, separately for each fragment occurrence. Shared selections stay shared
inside a fragment and separate between fragment instances. Invalid or ambiguous
addresses, duplicate contexts, missing members, conflicting bindings and typed
case cycles are rejected during analysis. Studio suggests context identifiers
and qualified references and uses the same analysis for diagnostics.

## Scope and release

Supported: feminine, neuter, masculine inanimate and masculine animate;
one optional adjective per context; present/past, affirmative/negative and
Japanese plain/polite forms. The source example uses stored Polish inflections.
Negative exercises concern the absence of the indicated groups, not general
logical negation scope. Masculine personal, collective numerals, pluralia tantum,
word chains and a general inflection generator remain outside this feature.
Indeclinable adjectives retain the documented strict-override limitation.

Named contexts currently address source counted existentials. Target counter
outputs use independent `quantity:@alias` links. Different governors for the
same shared noun selection remain rejected by existing lexical government
analysis; use the shared existential selection demonstrated above. A context
has one source realization per constituent; repeating a constituent requires a
separate named context. There is no new context editor or separate solver.

Content revision 52 requires Kotomi 1.5; the application version is 1.5.0.
Old applications reject the new Content requirement before installation.
Historical XML with the removed attribute is not supported. Merge the Data PR
first, then the application PR. Preserve the Data commit referenced by the
gitlink; after a squash merge update the pin and rerun validation before merging
the application. Both PRs require review and green CI; do not auto-merge.


Indeclinable adjectives have no persistent indeclinability declaration. Normalization removes overrides identical to common forms. Where feminine, neuter nominative or plural needs an explicit override, missing data yields Unsupported. Repeating common forms as overrides is not a supported workaround.
