# Changelog

All notable changes to this project are documented here.

## [Unreleased]
- **The manifest contract is checked like in the other updaters:** `tests/test_manifest_contract.py` checks that this updater reads the fields every manifest carries and the optional ones none may refuse (`min_common` among them), compares its reader with the readers of the other updaters when they are next to this repository (skipped when they are not), and checks that `min_common` is read when it is a version, ignored when it is not and that a misspelled field is still refused.
- **A project that asks for a newer EH3D-COMMON than the installed one is told:** the `min_common` of a manifest is read into the project entry and `status` writes a warning on the error stream for every project whose minimum is above the installed EH3D-COMMON (or says that the installed version is not known). It only warns and never holds an update back; the setting `min_common_check` (or `EH3D_UPDATER_MIN_COMMON`) is `warn` by default and `off` turns it off. The reader is the same file as in the other updaters (`common_gate.py`), pinned by a digest test.
- **The test count of the README files is the one of the CI:** 422 tests pass and four more are skipped when a sibling checkout is missing.
- **A picture mode for the window:** `--shot FILE.png` (the window needs the `gui` extra) opens the window at the size of `--size WxH` (320 to 8192, 1500x900 by default) in the language of `--lang CODE`, waits `--wait MS` milliseconds (0 to 60000, 1500 by default), saves what it drew as a PNG file and closes by itself. An existing file is never replaced unless `--replace` is given, the window shows an empty workspace (or the folder of `--workspace DIR`), asks nothing of GitHub, reads no saved preference or profile and writes no settings and no log in this mode, the exit code is 0 when the file was written, 1 when it was not (also when the picture does not come back within 30 seconds) and 2 for wrong arguments. The arguments are read by plain Python with its tests, so the command line refuses them on a machine without a screen.
- **The manifest may carry `min_common`:** the oldest version of the shared contracts repository the project works with. The field is read when it is a version and ignored when it is not, never refused, and a misspelled name is still refused; nothing is decided by it yet (the same rule as the other updaters of the family).

## [0.0.8] - Trusted signatures bound to a key, former project names in manifests and the new icon

- **The test count of the README files is the one of the CI:** 422 tests pass and four more are skipped when a sibling checkout is missing.
- **A manifest may name the previous name of a renamed project:** the optional field `former_name` is accepted, so a renamed repository no longer fails the check of the manifests.
- **The window carries the new icon:** the icon files inside the package are the icon of the program, so the title bar and the task bar show it.
- **A signature must be trusted, and may be bound to one key:** a good signature by a key whose trust is unknown is refused unless `signature_accept_unknown_trust` is set, and `signature_expected_fingerprint` (or `EH3D_UPDATER_EXPECTED_FINGERPRINT`) requires the signing key to be a given one.
- **A checkout of another repository is not updated:** when the `origin` of a checkout is not the official repository of the project the update and the preview refuse with a clear message (`allow_foreign_origin` overrides it).
- **A failed health check undoes the update by itself:** the previous installation is put back, the failed one is kept as `<name>.failed-xxxxxxxx`, and an update always keeps at least one previous installation whatever `backups_to_keep` says.
- **The evidence log is described as what it is:** it detects accidents, not attacks, in the README in eight languages and in the command reference.
- **Brand:** Add the application icon and the logos of the program.
- **Shared checks updated:** the validator also compares the badge and the Version row of the README with the manifest, fails when one of its checks cannot run, and the CHANGELOG step of the workflow reads the base branch from the environment.
- **Answers from GitHub have a size limit:** an answer bigger than 8 MB is refused instead of filling the memory.
- **A manifest pattern that can backtrack for ever is refused:** a version pattern longer than 300 characters or with a repeat inside a repeat is rejected when the manifest is read, and a pattern already stored is read as an unknown version.
- **The CHANGELOG step of the workflow no longer expands the base branch inside the script:** the name goes through an environment variable.

## [0.0.7] - Closed signature policy, dependencies from the windows and a harder evidence log
- **A mistyped signature policy fails closed:** a value that is not recognised (`"required"`, `"on"`, a text instead of `true`, an unknown `EH3D_UPDATER_REQUIRE_SIGNED`) is treated as `require` and the install warns, in the eight languages, naming the value.
- **The windows install the sibling repositories a project needs:** a project with `depends_on` gets its missing siblings first, in order, from both windows and from "install all missing", as the command line already did.
- **A local file the new version starts to track no longer blocks the update:** the staging merge runs before the local data is carried over, the shipped file wins, and nested build folders and links are no longer copied.
- **A damaged evidence log never breaks an update:** a last line that is not an object or a byte that is not UTF-8 is tolerated when recording and reported by the chain check.
- **The windows leave the busy state when a background task fails:** the GitHub check, the preview and the restore report the error instead of freezing the window.
- **Files in a legacy codepage and bad version patterns are handled:** settings, manifests and the restore check tolerate non-UTF-8 bytes, a manifest with an invalid version regex is refused, and a pattern that cannot be applied reads as an unknown version.
- **The workflows are hardened:** every action is pinned by its commit with its version in a comment, and the checkouts keep no credentials.

## [0.0.6] - CI hardening and monthly dependency updates

- **Monthly dependency updates:** Dependabot opens one grouped pull request a month for the GitHub Actions and the Python dependencies.
- **A line for every change:** a pull request that changes code must add a line under `[Unreleased]` of this file (`tools/changelog_pr_check.py`; the label `no-changelog` skips it).
- **Shared checks updated:** the validator of the suite checks the text of the banner against the manifest and reads the files that git tracks.

## [0.0.5] - Full log on failures, oldest Python tested and evidence none accepted

- **A manifest that says `evidence: none` is accepted:** a project with no code yet declares that nothing has been shown to work, and the manifest parser takes that level as the shared status tool and the dashboard do, instead of refusing the repository. With a test.
- **A failed command names its log:** a `--cli` run that ends with a code other than 0 or 10, or with an unexpected error, finishes with `Full log: <path>` on the error output; the traceback of an unexpected error is in the log.
- **Tested on the oldest and the newest Python it promises:** the CI runs the tests without the window on Python 3.10 and 3.13, and `tools/test_python_minimum.py` reads every source with the grammar of the oldest version named in `pyproject.toml`.
- **The maturity is functional:** the manifest, the badge and the table of the eight README files say it, since it is used and tried with real files; the evidence stays as host tests.
## [0.0.4] - The folders that are left out are told, an install can be previewed, the command line keeps a log and a manifest may name its binary

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
