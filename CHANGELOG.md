# Changelog

All notable changes to this project are documented here.

## [Unreleased]

- **The optional `binary` field of the manifest:** the file name of the executable a repository builds (letters, digits, dot, dash and underscore, no folder) is accepted by the parser in schema 1.0 and 1.1 and kept in `ProjectManifest.binary`; any other value is rejected.
- **`install --preview`:** shows what an installation would do (what is cloned from where, the siblings that are installed first, the signature policy and the build check) and changes nothing, like `update --preview`.
- **A log file for the command line:** every `--cli` run writes `cli_<time>.log` in the folder of the window's logs (command, every printed line, exit code); `--log-file FILE` chooses the file, `--no-log` writes none, `EH3D_UPDATER_LOG_DIR` moves the folder, and the oldest command-line logs are removed beyond twenty.

- **A program that is on the disk but is left out says so:** `status` and `check` print `IGNORED <folder>: <reason>` on the error output for each folder whose manifest is rejected, `status --json` gives them as `ignored` (`folder`, `reason`) and the summary line counts them, so a program no longer disappears from the table without a word.

## [0.0.3] - Weekly manifest checks, dependencies between repositories and a safer installation

- **The manifests of the whole suite are checked every week:** a CI job (on every push and once a week) reads the manifest of every repository with the parser of this tool and fails, listing them, when one is rejected or has no readable version.
- The README says what this tool is for: the computers of the people who develop the suite, by git. The CM5 of the workshop is updated by releases (`deploy/eh3d-update.py` of EH3D-SERVER).

- **`depends_on` (schema 1.1):** a manifest lists the sibling repositories its Cargo.toml reaches by path; `install` installs the missing ones first, in dependency order (a missing sibling or a cycle is an error). The CI of the repositories checks the list against their Cargo.toml.

- **The manifests of the suite are accepted:** `hardware_bound` (true or false), the roles `node` and `docs`, and the `mcu` target in a 1.0 manifest are valid, and a test reads every manifest of the repositories next to this one.
- **A repository without `build-test` is checked with its `test` script** (which never changes a version), so the programs of the suite can be installed and updated with the build check on.
- **A new installation whose check fails is removed** instead of staying as installed, and a version pattern with a single group that holds the whole `MAJOR.MINOR.PATCH` is read.

- **A test that does not depend on the machine:** the check of the update journal without the SDK sets its own state instead of relying on a sibling checkout being absent, so the 334 tests give the same result on any computer.

## [0.0.2] - The universal README, the live panel of the scripts and the layout checks of the repository

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
