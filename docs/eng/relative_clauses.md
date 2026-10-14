# Relative clauses in Content

Content revision 59 adds one `Zdania przydawkowe` pattern in category
`przydawki` in `patterns/sentence_maps.xml`. The `relative_clauses` definition
in `patterns/sentence_quizzes.xml` exposes a **Zdania przydawkowe** quiz
on Windows and Mobile through the existing grammar quiz package.
It requires an application containing Kotomi PR #208 and Polish grammar.
Downloading Content alone cannot add DSL support to an older application.

```xml
<sentence_pattern id="Zdania przydawkowe" category="przydawki"
                  forms="dictionary plain_negative past_plain past_negative_plain">
  <question>To jest {noun@item[case:nominative]}, {relative[agree:@item, government:@action].phrase} {verb@action[role:object, form].translation}.</question>
  <answer>これはわたしが{verb@action[role:object, form]}{noun@item}です。</answer>
</sentence_pattern>
```

`.phrase` preserves government prepositions: `nad którym zastanawiam się`,
`na który czekam`, `w który wierzę`. Without a preposition it behaves like
`.translation`: `którą czytam`, `której nie czytam`. The existing `object` role
binds the noun and verb; no additional argument declarations are needed.

| Form | Question for `book` and `yomu` | Answer |
|---|---|---|
| `dictionary` | To jest książka, którą czytam. | これはわたしがよむほんです。 |
| `plain_negative` | To jest książka, której nie czytam. | これはわたしがよまないほんです。 |
| `past_plain` | To jest książka, którą czytałem. | これはわたしがよんだほんです。 |
| `past_negative_plain` | To jest książka, której nie czytałem. | これはわたしがよまなかったほんです。 |

Select category `przydawki` in Studio. Preview and Simulator use the same
form restrictions as the quiz. Enable plain output in the quiz; polite verb
forms inside the relative clause are excluded. The final `です` stays fixed.
Use existing filters to practice selected vocabulary, for example
`verb.id=yomu;noun.id=book`. Without filters the existing dictionary categories
and explicit compatibility lists apply. They do not guarantee naturalness of
every semantic combination. Revision 59 corrects two demonstrated problems:
`sukuu` accepts people, animals and explicit `inochi` (life); `ireru` no longer
accepts all `abstract` nouns but explicitly retains `okane` (money).
This rejects rescuing a revision exercise and inserting time in every pattern.
The narrower `sukuu` scope also excludes abstract objects such as work and plans.
No exceptions or curated sentence dictionary were added to the engine.

The scope remains singular object relatives. `okane` has a plural agreement
class and is correctly rejected; `harau`, restricted to `okane`, therefore
has no results here. Do not invent forms to bypass this limitation.

Engine statistics distinguish vocabulary combinations, generated realizations
including context, and unique text. This pattern does not display context,
so different existing context options can produce identical text.
`generated_sentences` must not be read as the number of distinct visible sentences.

See the [Kotomi documentation](https://github.com/MaciejPotas/Kotomi/blob/main/docs/eng/relative_clauses.md)
for the complete DSL and `forms` contract. Publication advances only the Content
revision and rebuilds its manifest. Executable Quiz packages and the application
version remain unchanged.
