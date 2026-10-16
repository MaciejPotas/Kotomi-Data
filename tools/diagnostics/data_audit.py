"""Read-only Content audit using Kotomi's parser, catalogs and validators."""
from __future__ import annotations

import argparse
from collections import Counter
import json
from pathlib import Path
import re
import sys


def fixed_form_requirements(project):
    """Only infer obligations for a fixed word and a fixed engine form selector.

    Open slots, dynamic quiz forms and inherited occurrence forms do not define
    a universal per-word completeness contract. Leave those to solver diagnostics.
    """
    if not getattr(project, 'patterns', {}):
        return {}
    from kotomi.core.generation.compatibility import satisfies_required_form_specs
    from kotomi.core.project.errors import ProjectError
    requirements = {}
    for pattern in getattr(project, 'patterns', {}).values():
        try:
            analysis = project.analyze_pattern(pattern)
        except ProjectError:
            continue  # The project validator reports invalid definitions.
        for slot, identifier in analysis.fixed_words.items():
            key = analysis.slots[slot].dictionary
            if project.dictionary_schemas.get(key) not in {'verb', 'adjective'}:
                continue
            word = project.words.get(key, {}).get(identifier)
            specs = analysis.required_form_specs.get(slot, ())
            if word is None or not specs or 'form' in specs:
                continue
            # Respect base-translation and other exemptions owned by the engine.
            satisfied = satisfies_required_form_specs(project, word, analysis, slot, '')
            for name in specs:
                if not satisfied or name in word.forms:
                    row = requirements.setdefault((key, identifier), {})
                    row.setdefault(name, set()).add(pattern.composite_id or pattern.id)
    return requirements


def form_inventory(word, catalog, generated, required):
    absent = set(catalog) - set(word.forms)
    missing_required = sorted(name for name in required if name not in word.forms)
    return dict(
        explicit_forms=sorted(word.forms),
        absent_catalog_forms=sorted(absent),  # Backward-compatible raw inventory.
        required_by_patterns={name: sorted(ids) for name, ids in sorted(required.items())},
        missing_required_forms=missing_required,
        generated_forms=sorted(absent & set(generated)),
        optional_forms_not_explicit=sorted(absent - set(required)),
        unsupported_by_generator=sorted(absent - set(generated)),
        requirements_status='PARTIAL: fixed-word fixed-form requirements only; no universal required/optional metadata',
        generation_scope='Authoring suggestions only; runtime uses stored forms. Generated translations and linguistic applicability are unverified.',
        selectable_catalog_forms=sorted(name for name, definition in catalog.items()
                                        if getattr(definition, 'is_selectable', False)),
    )


def known_conjugation_variant(word, actual, expected):
    # Only the copular contraction after the complete na-adjective stem.
    # Arbitrary differences (including a changed stem) still require review.
    if word.type != 'na_adjective':
        return False
    variants = (('ではありません', 'じゃありません'),
                ('ではなかった', 'じゃなかった'),
                ('ではありませんでした', 'じゃありませんでした'),
                ('ではない', 'じゃない'),
                ('ではありません', 'じゃないです'),
                ('ではありませんでした', 'じゃなかったです'))
    return any({actual, expected} == {word.kana + full, word.kana + short}
               for full, short in variants)


def audit_project(project, dictionary=None, *, word_validator=None):
    """Return deterministic findings without changing the supplied project."""
    findings = []
    inventories = {}
    requirements = fixed_form_requirements(project)
    selected = {key: words for key, words in project.words.items()
                if dictionary is None or key == dictionary}
    if dictionary is not None and dictionary not in project.words:
        raise ValueError(f"Unknown dictionary: {dictionary}")

    def add(level, key, word, message, *, affects_completeness=None):
        if level == 'WARNING' and (message == 'Redundant source-language form overrides will be removed on save.'
                                   or ' repeats common case(s): ' in message):
            level = 'INFO'
        path = project.dictionary_paths.get(key, project.manifest_path)
        if path and project.manifest_path:
            path = path.relative_to(project.manifest_path.parent)
        findings.append(dict(severity=level, dictionary=key, word=word,
                             file=str(path or ''), message=message,
                             affects_completeness=(level != 'INFO' if affects_completeness is None else affects_completeness)))

    # The engine owns grammar, references, counting, agreement and government.
    for issue in project.validate(include_pattern_renderability=False):
        level, _, message = issue.partition(': ')
        match = re.search(r"'([^'/]+)/([^'/]+)(?:/[^']*)?'", message)
        key, word = match.groups() if match and match.group(1) in project.words else ('', '')
        if not key or key in selected:
            add(level if level in {'ERROR', 'WARNING', 'INFO'} else 'WARNING', key, word, message)

    for key, words in sorted(selected.items()):
        schema = project.dictionary_schemas.get(key, '')
        catalog = project.form_definitions.get(schema, {})
        config = project.dictionary_configs.get(key)
        for identifier, word in sorted(words.items()):
            if word_validator:
                for issue in word_validator(word):
                    add(issue.severity, key, identifier, issue.message)
            for field in getattr(config, 'required_fields', ('translation', 'kana')):
                value = getattr(word, 'number_value' if field == 'value' else field, '')
                if value is None or isinstance(value, str) and not value.strip():
                    add('ERROR', key, identifier, f'Missing required field: {field}')
            for name, form in sorted(word.forms.items()):
                if not form.translation.strip() and not (form.target_translation or form.agreement_translations):
                    add('WARNING', key, identifier, f'Missing explicit form translation: {name}; no general or contextual translation is stored')
            generated = {}
            missing = sorted(set(catalog) - set(word.forms))
            # Catalog membership does not imply morphological productivity.
            # Absent optional/nonproductive forms are inventory, never errors.
            inventories[f'{key}/{identifier}'] = dict(
                schema=schema, explicit_forms=sorted(word.forms),
                absent_catalog_forms=missing,
                roles=sorted(word.usage),
                contextual_translations=sorted(name for name, form in word.forms.items()
                                                if form.target_translation or form.agreement_translations),
            )
            if schema == 'noun':
                for case in project.instruction_language.capabilities.cases:
                    if not word.cases.get(case, '').strip():
                        add('WARNING', key, identifier, f'Missing noun case: {case}')
                if not word.agreement_class:
                    add('WARNING', key, identifier, 'Missing noun agreement class')
            if schema in {'verb', 'adjective'}:
                from kotomi.core.dictionary.forms import generate_forms, FormGenerationError
                try:
                    generated = generate_forms(word.kana, word.type)
                except FormGenerationError as error:
                    add('WARNING', key, identifier, f'Conjugation cannot be checked: {error}', affects_completeness=False)
                else:
                    for name, form in sorted(word.forms.items()):
                        if name in generated and form.kana and form.kana != generated[name]:
                            known = known_conjugation_variant(word, form.kana, generated[name])
                            add('INFO' if known else 'WARNING', key, identifier,
                                f'Conjugation {"has a supported variant" if known else "needs review"}: {name}: {form.kana} (generator {generated[name]})',
                                affects_completeness=False)
            if schema == 'verb':
                for role, noun_ids in sorted(word.usage_nouns.items()):
                    if noun_ids:
                        add('INFO', key, identifier, f'Explicit noun exceptions for {role}: {", ".join(noun_ids)}; review whether a category suffices')

            required = requirements.get((key, identifier), {})
            inventory = inventories[f'{key}/{identifier}']
            inventory.update(form_inventory(word, catalog, generated, required))
            for name in inventory['missing_required_forms']:
                add('WARNING', key, identifier,
                    f'Missing required stored form: {name}; fixed word in patterns: {", ".join(sorted(required[name]))}. '
                    'Generator availability does not provide a runtime realization or translation.')
            if inventory['contextual_translations'] and any(
                    not word.forms[name].translation.strip() for name in inventory['contextual_translations']):
                add('INFO', key, identifier,
                    'Contextual translations are available; general translation coverage is unverified.')

    findings = sorted({tuple(item.items()) for item in findings})
    findings = sorted((dict(item) for item in findings),
                      key=lambda item: (item['dictionary'], item['word'], item['severity'], item['message']))
    counts = Counter(item['severity'] for item in findings)
    dictionaries = {}
    for key, words in sorted(selected.items()):
        incomplete = {item['word'] for item in findings if item['dictionary'] == key and item['word'] in words and item['affects_completeness']}
        dictionaries[key] = dict(total=len(words), complete=len(words)-len(incomplete), incomplete=len(incomplete),
                                 review_notes=sum(item['dictionary'] == key and not item['affects_completeness'] for item in findings))
    return dict(words_scanned=sum(len(words) for words in selected.values()),
                errors=counts['ERROR'], warnings=counts['WARNING'], info=counts['INFO'],
                dictionaries=dictionaries, findings=findings, inventory=inventories)


def render_report(report, verbose=False):
    lines = ['KOTOMI DATA AUDIT', f"Words scanned: {report['words_scanned']}",
             f"Errors: {report['errors']}  Warnings: {report['warnings']}  Info: {report['info']}",
             'Completeness covers checked contracts only; per-word form obligations remain partially unverified (see inventory).']
    for key, values in report['dictionaries'].items():
        lines.append(f"\n{key.upper()}: complete={values['complete']} incomplete={values['incomplete']} review_notes={values['review_notes']}")
    for issue in report['findings']:
        lines.append(f"[{issue['severity']}] {issue['dictionary']}/{issue['word']}: {issue['message']} ({issue['file']})")
    if verbose:
        for key, item in report['inventory'].items():
            lines.append(f"{key}: explicit={','.join(item['explicit_forms'])}; absent_catalog={','.join(item['absent_catalog_forms'])}; roles={','.join(item['roles'])}")
            for field in ('required_by_patterns', 'generated_forms', 'optional_forms_not_explicit',
                          'missing_required_forms', 'unsupported_by_generator', 'requirements_status', 'generation_scope'):
                lines.append(f"  {field}: {item[field]}")
    return '\n'.join(lines) + '\n'


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    root = Path(__file__).resolve().parents[2]
    parser.add_argument('--project', type=Path, default=root/'quiz_project.xml')
    parser.add_argument('--kotomi', type=Path, help='Kotomi checkout containing the engine')
    parser.add_argument('--dictionary')
    parser.add_argument('--verbose', action='store_true')
    parser.add_argument('--output', type=Path, default=root/'audit-results/data-audit.txt')
    parser.add_argument('--json', type=Path)
    args = parser.parse_args(argv)
    candidates = [args.kotomi] if args.kotomi else [root.parent, root.parent/'Kotomi']
    engine = next((p for p in candidates if p and (p/'kotomi/application/quiz_project.py').is_file()), None)
    if engine is None:
        parser.error('Engine checks require Kotomi. Use --kotomi PATH; no grammar registry is duplicated here.')
    sys.path.insert(0, str(engine.resolve()))
    from kotomi.application.quiz_project import QuizProject
    try:
        from kotomi.application.dictionary_service import DictionaryService
        project = QuizProject.load(args.project)
        service = DictionaryService(project.manifest_path, project=project)
        report = audit_project(project, args.dictionary, word_validator=service.validate_word)
    except (ValueError, OSError) as error:
        report = dict(words_scanned=0, errors=1, warnings=0, info=0, dictionaries={}, inventory={},
                      findings=[dict(severity='ERROR', affects_completeness=True, dictionary='', word='', file=str(args.project), message=f'Project could not be audited: {error}')])
    except Exception as error:
        from kotomi.core.project.errors import ProjectError
        if not isinstance(error, ProjectError):
            raise
        report = dict(words_scanned=0, errors=1, warnings=0, info=0, dictionaries={}, inventory={},
                      findings=[dict(severity='ERROR', affects_completeness=True, dictionary='', word='', file=str(args.project), message=f'Parser rejected Content: {error}. Fix this error and rerun; remaining words were not scanned.')])
    text = render_report(report, args.verbose)
    print(text)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(text, encoding='utf-8')
    if args.json:
        args.json.parent.mkdir(parents=True, exist_ok=True)
        args.json.write_text(json.dumps(report, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    return int(bool(report['errors']))


if __name__ == '__main__':
    raise SystemExit(main())
