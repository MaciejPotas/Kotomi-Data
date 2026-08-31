# Repository Tools

Tools in this directory maintain and validate the public Kotomi-Data repository itself.

`validate_repository.py` is the local and CI gate. It verifies the `learning/` hierarchy, required directory documentation, XML schema markers, `quiz_project.xml` references, Database revision and manifest integrity, public quiz package inventories, hashes, and Python source compatibility.

Run it from the repository root with:

```bash
python tools/validate_repository.py
```

Release-generation scripts live in the private Kotomi repository because they need the application source as their source of truth. This public tools directory should contain only utilities that can validate or maintain this repository without access to private source code.
