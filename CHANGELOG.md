# Changelog

All notable changes to this project are documented here.

## [Unreleased]

- **README in the universal layout, in eight languages:** the README has the same sections in the same order as the other repositories of the family (status, overview, architecture, features, security, interfaces, configuration, quick start, testing, structure, roadmap and known limits), with figures taken from the code and from the tests that were run. The Architecture and Repository Structure pictures are drawn from `docs/architecture.json` and `docs/structure.json` by `tools/make_architecture.py` and `tools/make_structure.py`, and the CI checks that they match.
- **The build, build-test and test scripts show a live panel:** a banner with the name and version, one line per step with its time, the number of tests that passed and a summary at the end, with the whole output kept in a log file. `test.sh` and `test.bat` run only the tests and never change the version; without `tools/pretty_run.py` the scripts behave as they always did.
- **The layout of the README is checked in the CI:** the validator runs `tools/universal_readme_check.py` and lists, as a warning, what differs from the universal layout of the README.
- **The window no longer fills the console with `Cannot read property ... of null` when it closes:** the windows are deleted before the object their bindings read, instead of the other way round.

- **The build scripts work when the python first on the PATH makes a venv with no activate script** (for example the python that ESP-IDF installs): the venv is made with the `py` launcher when there is one and its own python, or its folder first on the PATH, is used instead of the activate script.

## [0.0.1] - The updater of the EH3D ecosystem

- **Finds the EH3D repositories** through their `eh3d.project.json` manifests (ecosystem `EH3D`) on GitHub, with no token, and the local checkouts that sit next to each other in the workspace.
- **Installs and updates one project at a time, after a confirmation:** the replacement is cloned, merged without force and built and checked in a staging clone first; the live installation is only touched when that succeeds, and the previous one is kept as a backup that can be restored from the window.
- **Install all missing / Update all outdated** are separate, confirmed, sequential batch actions through the same safety path; nothing updates by itself.
- **An evidence log** of every attempt, checkable later for edited, removed or reordered lines, and an optional policy on signed commits.
- **A Qt Quick window in eight languages** (English, Spanish, French, Italian, German, Chinese, Japanese and European Portuguese) and a command line (`--cli`) that needs nothing but the standard library.
- 317 tests, run on Linux and Windows in CI, and a repository check of the manifest, the versions, the changelog and the eight README files.
