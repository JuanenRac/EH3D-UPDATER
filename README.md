<p align="center">
  <img src="images/EH3D_UPDATER_BANNER.svg" alt="EH3D-UPDATER banner" width="100%">
</p>

# 🛠️ EH3D-UPDATER

<p align="center">🇺🇸 <b>English</b> | <a href="README_spa.md">🇪🇸 Español</a> | <a href="README_fra.md">🇫🇷 Français</a> | <a href="README_ita.md">🇮🇹 Italiano</a> | <a href="README_deu.md">🇩🇪 Deutsch</a> | <a href="README_zho.md">🇨🇳 中文</a> | <a href="README_jpn.md">🇯🇵 日本語</a> | <a href="README_por.md">🇵🇹 Português</a></p>

### Detects, installs and updates the repositories of the EH3D Fabrication Suite on your PC: nothing happens by itself, and a live installation is only replaced after its replacement has been built and checked

<p align="center">
  <img src="https://img.shields.io/badge/License-GPL%203.0--or--later-blue.svg" alt="GPL 3.0 or later">
  <img src="https://img.shields.io/badge/Stack-Python%203.10%2B-3776AB.svg" alt="Python">
  <img src="https://img.shields.io/badge/Languages-8-00E5FF.svg" alt="Languages">
  <img src="https://img.shields.io/badge/Version-0.0.2-0f6cbd.svg" alt="Version">
  <img src="https://img.shields.io/badge/Maturity-scaffolding-FFB020.svg" alt="Maturity">
</p>

---

**Honesty check - what actually runs today:** a command line and a Qt Quick window that find the EH3D repositories through their `eh3d.project.json` manifests, compare each local checkout with GitHub and install or update one at a time after a confirmation. The update is cloned, merged without force and built and checked in a staging clone first, and the previous installation is kept as a backup. It is the updater of the other ecosystems of the family with the names of EH3D, with 322 tests that run on a computer with a fake GitHub and local repositories. It has not been used for real work yet and has never installed or updated a project from the real GitHub.

---

> **Safety and security status:** it replaces files on your machine and runs the build check of what it installs, so it only does so after an explicit confirmation, never over a checkout that has local changes, and it records every attempt in an evidence log that carries no secrets. It checks the signature of a commit only if you choose that policy; it is not a safety system and controls no machine.

## 📋 At a glance

| | |
|---|---|
| Version | `0.0.2` |
| Maturity | Scaffolding |
| Tests | 322 |
| Stack | Python 3.10+ / PySide6 / Qt Quick |
| On real hardware | Not applicable: it runs on the PC of the person using it |

**Jump to:** [Overview](#-overview) · [Architecture](#-architecture) · [Quick start](#-quick-start) · [Testing](#-testing) · [Structure](#-repository-structure) · [Related](#-related-projects)

## 🚦 Project status

Each line is one part of this repository and the light says how far it is today. It is written from what the repository can show (tests, builds, runs), not from what is planned.

🟢 Done and verified · 🟡 Works, with known limits · 🟠 Partly done or not verified yet · 🔴 Not done or not working

| Area | State | What it means here |
|---|---|---|
| Software | 🟡 | A command line and a Qt Quick window find the EH3D repositories by their manifests, compare them with GitHub and install or update one at a time, with a staging clone and a backup of the previous installation. |
| Tests | 🟢 | 322 tests pass (`pytest`), with a fake GitHub and local repositories (no network); one more is skipped when a sibling checkout it needs is missing. |
| Discovery | 🟡 | Public repositories are only candidates: a project joins the ecosystem when its root `eh3d.project.json` validates and says `EH3D`; tested against a fake listing, not run against the real GitHub. |
| Real use | 🟠 | It has not been used for real work yet and has never installed or updated a project from the real GitHub; only a few EH3D repositories exist to be installed. |
| Interface | 🟡 | The window works in eight languages and its Python bridge is covered by tests; the command line needs only the standard library. |
| Security | 🟡 | Nothing changes without a confirmation or over a checkout with local changes, merges never force, and an evidence log shows edited or reordered lines; the signed-commit policy is optional and there has been no independent review. |
| Integration | 🟡 | ELECTRO-HOBBY-3D-UPDATER hands the EH3D projects over to it; that hand-over has not been run against a real checkout. |
| Real hardware | 🟢 | Not applicable: it runs on the PC of the person using it. |
| Documentation | 🟢 | README in eight languages, the command-line reference and the guide to the window. |

## 🎯 Overview

* **It finds the projects by their manifests:** the public repositories of the owner on GitHub are only a list of candidates; one is a project when its root `eh3d.project.json` validates and declares the ecosystem `EH3D`, so a new repository appears by having a manifest and nothing in this tool lists the projects. Locally, a folder name alone is never enough to join the ecosystem.
* **It compares the machine with GitHub:** for each project it reads the version of the local checkout and the one on the default branch of GitHub, and says whether it is installed, up to date, outdated or has new commits (an equal version with new commits is noticed with one `git ls-remote`).
* **It installs and updates one project at a time, after a confirmation:** the replacement is built and checked in a staging clone before the live installation is touched, and the previous one is kept as a backup that can be restored from the window or with `restore-backup`.
* **Batches are confirmed too:** *Install all missing* and *Update all outdated* are separate, sequential actions through the same safety path. Nothing updates in the background.
* **An evidence log and an optional signed-commit policy:** every attempt is written to a log that can be checked later for edited, removed or reordered lines.
* **Station profiles:** a named profile lists the projects a machine works with, and the window and the commands follow it.
* **A window in eight languages and a command line** (`--cli`) that needs only the standard library, so it also works on a machine without a screen.

## 🧩 Role in EH3D

EH3D-UPDATER is the way to get the suite and keep it current. ELECTRO-HOBBY-3D-UPDATER, the tool above the four ecosystems, hands over to it for the EH3D projects. A new EH3D repository needs nothing here: it appears as soon as it is public and carries a valid manifest.

## 🏛️ Architecture

<p align="center">
  <img src="images/architecture.svg" alt="EH3D-UPDATER architecture: who uses it, what it holds and what it depends on" width="100%">
</p>

How the parts of this repository fit together: who uses it, what it holds and what it depends on. The picture is drawn from `docs/architecture.json` and checked against the code.

## ✨ Features

* **The manifest decides:** discovery, the name, the version, the build command and the notes all come from the repository's own `eh3d.project.json`; a candidate whose manifest is invalid, or whose version is lower than the installed one, is refused before anything is touched.
* **A healthy checkout is never replaced:** a real local edit or a diverged branch makes the update fail loudly, never a silent reset (`--ff-only` with `--no-build`).
* **Preview before updating:** `update --preview` shows the candidate commit, its author, its signature state and the build and tool files it changes, then stops.
* **Notify only:** `check` lists what could be updated, changes nothing and exits with 10 when something can (a desktop notification is optional).
* **Backups with a limit:** the previous installation is kept as `<name>.backup-<8 hex digits>`; the newest 2 are kept by default and `clean-backups` prunes the rest.
* **Kind to the network:** requests retry with backoff, a short `Retry-After` is waited out, the repository listing is cached with `If-None-Match` (a `304` costs no quota) and an unreachable GitHub falls back to the local state with a warning.

## 🔒 Security & Safety

| Threat | Defense |
|---|---|
| An unwanted or surprise update | nothing runs in the background: `install` and `update` take one project name and a confirmation, and the batch buttons of the window are separate, sequential and confirmed |
| A broken candidate replacing a working installation | the candidate is cloned, merged without force, built and checked in a staging clone; the live folder is swapped with two renames only afterwards, and the previous one is kept as a backup you can restore |
| Losing local work | a checkout with local changes or a diverged branch is never replaced: the update fails loudly |
| A repository that pretends to be part of the suite | a repository joins only when its root manifest validates and declares `EH3D`; a candidate with a lower version than the installed one is refused |
| A commit of unknown origin | optional policy: with `EH3D_UPDATER_REQUIRE_SIGNED=1` (or the setting) and an allowed-signers file a commit must be signed; by default an unsigned one is installed with a warning, and `update --preview` shows the signature state first |
| Tampering with the record of what happened | every install or update attempt is one line of an evidence log that carries the hash of the line before it; `evidence` verifies the chain and exits 1 when a line was edited, removed or reordered |
| Leaking secrets | the evidence log carries no secrets; GitHub is read with no token (an optional `GITHUB_TOKEN` only raises the rate limit); the tool never prints it |
| A validation script that cannot run here | an install that cannot be validated because a tool is missing is refused unless you accept it (the setting `validation_unavailable` or `EH3D_UPDATER_ACCEPT_UNAVAILABLE_VALIDATION=1`) |
| Two copies at once | an instance that finds another one working on the workspace refuses to clean or restore backups |

**What is not defended:** the build script of an installed project is that project's own code and runs with your rights, so install only what you trust; unsigned commits are accepted by default; and the tool has had no independent review. Report a vulnerability privately (see [SECURITY.md](SECURITY.md)).

## 🔌 Interfaces

| Interface | What it is | Where |
|---|---|---|
| Window | a Qt Quick window in eight languages (the default; needs the optional `PySide6` extra) | `qt_gui.py`, `qml/Main.qml`, [docs/QML_DESKTOP_GUI.md](docs/QML_DESKTOP_GUI.md) |
| Command line | `eh3d-updater --cli` with `status`, `install`, `update`, `check`, `clean-backups`, `restore-backup` and `evidence`; exit codes 0, 1 and 10 (something can be updated) | [docs/CLI_REFERENCE.md](docs/CLI_REFERENCE.md) |
| GitHub | `GET /users/<owner>/repos` (cached with `If-None-Match`) and the raw manifest of each candidate; no token needed | `github_client.py` |
| The workspace | the folders next to the tool, `<name>.backup-xxxxxxxx` for the previous installations and `.eh3d-updater/evidence.jsonl` for the evidence log | `install.py`, `evidence.py` |
| Settings | `~/.eh3d_updater_settings.json` (language, workspace, profile, backups kept, signature policy) | `settings.py` |

## ⚙️ Configuration

Nothing has to be configured to start. The choices that are remembered live in `~/.eh3d_updater_settings.json`, and a few can also be given as options or environment variables.

| Setting | Default | Range | What it does |
|---|---|---|---|
| `workspace_root` / `--workspace` | the parent folder of the tool | a folder | where the checkouts, the backups and the evidence log live |
| `lang` | the system language | en, es, de, fr, it, ja, zh, pt | the language of the window |
| `profile` / `--profile` | none (all projects) | a defined profile name; an undefined one is an error | restricts `status`, `check`, `install` and `update` to the projects of a station profile |
| `backups_to_keep` / `clean-backups --keep` | 2 | a whole number of 0 or more | how many previous installations are kept per project |
| `require_signed_commits`, `allowed_signers_file` / `EH3D_UPDATER_REQUIRE_SIGNED=1`, `EH3D_UPDATER_ALLOWED_SIGNERS` | off | on or off | refuse commits that are not signed by an allowed signer |
| `validation_unavailable` / `EH3D_UPDATER_ACCEPT_UNAVAILABLE_VALIDATION=1` | refuse | refuse or accept | what to do when a project's validation cannot run because a tool is missing |
| `GITHUB_TOKEN` | none | a GitHub token | only raises the rate limit of the listing; never required |
| `--no-build` (install, update) | off | on or off | clone or pull only, without the project's own build check (a plain fast-forward) |

The network values are constants: 10 s per request, up to 8 requests at a time, 3 attempts with backoff and a `Retry-After` of at most 60 s.

## 🚀 Quick start

You need Python 3.10 or newer; the window also needs PySide6 (`pip install ".[gui]"`).

```bash
./run.sh --cli status          # run.bat --cli status on Windows
./run.sh --cli status --offline --json
./run.sh --cli check           # exit code 10 when something can be updated
./run.sh --cli update EH3D-COMMON --preview
./run.sh --cli install EH3D-CORE-LIBS
```

`run.sh` / `run.bat` without `--cli` open the window. `install` and `update` ask for a confirmation before they touch anything, and always take one project name.

## 🧪 Testing

The suite has 322 tests that pass (`pytest tests`), and one more that is skipped when a sibling checkout it needs is not next to this one. They run with a fake GitHub and local repositories, with no network, and cover the manifest contract, the discovery, the version and commit comparison, install and update with the staging clone and the refusals (local changes, a diverged branch, a lower version, an invalid manifest, a failing build), backups and restore, the evidence chain, the signature policy, the settings and profiles, the messages and the eight languages of the window, and the Python bridge of the window (offscreen). A test also checks that the file tree of every README lists each versioned first-level entry. The CI runs them on Linux and on Windows, plus `python tools/ci_validate.py` and a syntax check of every Python file.

## 🏗️ Build & Release

The version lives in `pyproject.toml`, in `eh3d.project.json` and in the package, and each version has its entry in [CHANGELOG.md](CHANGELOG.md). `build.sh` / `build.bat` install the package and check it, `build-test.sh` / `build-test.bat` also run the tests and `test.sh` / `test.bat` run only the tests, each in a live panel; the version does not change. Releases are published on GitHub; the tool is installed from this repository with pip and is not on PyPI.

## 📂 Repository Structure

<p align="center">
  <img src="images/repository-structure.svg" alt="Repository structure of EH3D-UPDATER" width="100%">
</p>

<details>
<summary>Text version of the tree</summary>

```text
EH3D-UPDATER/
├── src/eh3d_updater/
│   ├── main.py                                  the command line and the start of the window
│   ├── github_client.py detect.py               the versions on GitHub and the local checkouts
│   ├── project_manifest.py registry.py          the manifest contract and its runtime form
│   ├── install.py commits.py                    install, update, backup, restore; commit comparison
│   ├── evidence.py signature.py                 the evidence log and the signed-commit policy
│   ├── qt_gui.py qml/                           the Qt Quick window and its QML
│   ├── i18n.py messages.py                      the eight languages and the messages as codes
│   └── settings.py profiles.py                  what is remembered and the station profiles
├── tests/                                       no network: a fake GitHub and local repositories
├── docs/                                        the command line reference, the guide to the window and the data of the two pictures
├── tools/                                       CI check, build check, README check, icon and picture tools
├── images/                                      banner and the Architecture and Repository Structure pictures
├── .github/                                     CI and release workflows, issue and pull-request templates
├── build.sh build.bat                           install and check the package in a live panel
├── build-test.sh build-test.bat                 the same, then the tests
├── run.sh run.bat                               start the window, or the command line with --cli
├── bump*.py                                     the scripts that raise the version
├── eh3d.project.json                            manifest: version, role, maturity and build command
├── run-gui.vbs                                  start the window without a console on Windows
├── pyproject.toml                               the Python package and its extras
├── CHANGELOG.md                                 what changed in each version
├── SECURITY.md SUPPORT.md                       how to report a vulnerability and where to ask
├── CONTRIBUTING.md CODE_OF_CONDUCT.md LICENSE   how to contribute, the code of conduct and the licence
└── LICENSE.md                                   the licence text in Markdown
```

</details>

## 🗺️ Roadmap & Known limits

**Known limits today**

* It has never installed or updated a project from the real GitHub: everything is tested with a fake GitHub and local repositories, and only a few EH3D repositories exist to be installed.
* The hand-over from ELECTRO-HOBBY-3D-UPDATER has not been run against a real checkout.
* Commits are not required to be signed by default; the policy is optional.
* The build script of an installed project runs with your rights.
* The tool has had no independent review, and it is not on PyPI.

**Next**

* Install and update a real project end to end with the real GitHub and record what shows up.
* Run the hand-over from ELECTRO-HOBBY-3D-UPDATER on a real checkout.
* Decide whether signed commits become the default for the suite.

## 🌍 Languages

README and texts exist in English, Spanish, French, Italian, German, Chinese, Japanese and European Portuguese.

## 🔗 Related Projects

* [EH3D-COMMON](https://github.com/JuanenRac/EH3D-COMMON): the project container and the machine types; it can be installed with this tool
* [EH3D-CORE-LIBS](https://github.com/JuanenRac/EH3D-CORE-LIBS): the readers of Gerber, Excellon and G-code; it can be installed with this tool
* [ELECTRO-HOBBY-3D-UPDATER](https://github.com/JuanenRac/ELECTRO-HOBBY-3D-UPDATER): the updater above the four ecosystems, which dispatches to this one
* [URTC-UPDATER](https://github.com/JuanenRac/URTC-UPDATER): the updater of URTC, from which this tool takes its design

## 📚 Documentation

* [Command line reference](docs/CLI_REFERENCE.md): every command, option and exit code.
* [The desktop window](docs/QML_DESKTOP_GUI.md): how the Qt Quick window sits on the same services as the command line.
* [Changelog](CHANGELOG.md)

## 🤝 Contributing & Community

* Before a pull request run `PYTHONPATH=src python -m pytest tests -q` and `python -I tools/ci_validate.py`: all must pass. See [CONTRIBUTING.md](CONTRIBUTING.md) and the [code of conduct](CODE_OF_CONDUCT.md).
* The README exists in eight languages: a change to the text is made in all eight files, and the two pictures are drawn from `docs/architecture.json` and `docs/structure.json` by `tools/make_architecture.py` and `tools/make_structure.py`.
* A change to a user-facing text goes into the eight languages of `i18n.py`; a safety decision is made in the Python services, never in the QML.
* Report a vulnerability privately: [SECURITY.md](SECURITY.md). Questions, ideas and reports: electrohobby3d@gmail.com ([SUPPORT.md](SUPPORT.md)).

## 👤 AUTHOR

**JuanenRac (Electro Hobby 3D)** · electrohobby3d@gmail.com

## 📜 LICENSE

Software: GPL-3.0-or-later. See [LICENSE](LICENSE). Hardware designs of the suite use CERN OHL-S.
