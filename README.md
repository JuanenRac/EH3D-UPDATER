<p align="center">
  <img src="images/EH3D_UPDATER_BANNER.svg" alt="EH3D-UPDATER banner" width="100%">
</p>

# 🛠️ EH3D-UPDATER

<p align="center">🇺🇸 <b>English</b> | <a href="README_spa.md">🇪🇸 Español</a> | <a href="README_fra.md">🇫🇷 Français</a> | <a href="README_ita.md">🇮🇹 Italiano</a> | <a href="README_deu.md">🇩🇪 Deutsch</a> | <a href="README_zho.md">🇨🇳 中文</a> | <a href="README_jpn.md">🇯🇵 日本語</a> | <a href="README_por.md">🇵🇹 Português</a></p>

### Detects, installs and updates the repositories of the EH3D Fabrication Suite on your PC: nothing happens by itself, and a live installation is only replaced after its replacement has been built and checked

<p align="center">
  <img src="https://img.shields.io/badge/License-GPL%203.0--or--later-blue.svg" alt="GPL 3.0 or later">
  <img src="https://img.shields.io/badge/Language-Python%203.10%2B-blue.svg" alt="Python">
  <img src="https://img.shields.io/badge/Languages-8-00E5FF.svg" alt="Languages">
  <img src="https://img.shields.io/badge/Version-0.0.1-0f6cbd.svg" alt="Version">
  <img src="https://img.shields.io/badge/Maturity-scaffolding-FFB020.svg" alt="Maturity">
</p>

---

**Honesty check - what actually runs today:** a command line and a Qt Quick window that find the EH3D repositories through their `eh3d.project.json` manifests, compare each local checkout with GitHub and install or update one at a time after a confirmation. The update is cloned, merged without force and built and checked in a staging clone first, and the previous installation is kept as a backup. It is the updater of the other ecosystems of the family with the names of EH3D, with 317 tests that run on a computer with a fake GitHub and local repositories. It has not been used for real work yet, and only EH3D-COMMON and EH3D-CORE-LIBS exist to be installed.

---

> **Safety and security status:** it replaces files on your machine and runs the build check of what it installs, so it only does so after an explicit confirmation, never over a checkout that has local changes, and it records every attempt in an evidence log that carries no secrets. It checks the signature of a commit only if you choose that policy; it is not a safety system and controls no machine.

## 📋 At a glance

| | |
|---|---|
| Version | `0.0.1` |
| Maturity | Scaffolding |
| Tests | 317 |
| Stack | Python 3.10+ / PySide6 / Qt Quick |
| On real hardware | Not applicable: it runs on the PC of the person using it |

## 🚦 Project status

Each line is one part of this repository and the light says how far it is today. It is written from what the repository can show (tests, builds, runs), not from what is planned.

🟢 Done and verified · 🟡 Works, with known limits · 🟠 Partly done or not verified yet · 🔴 Not done or not working

| Area | State | What it means here |
|---|---|---|
| Software | 🟡 | A command line and a Qt Quick window find the EH3D repositories by their manifests, compare them with GitHub and install or update one at a time, with a staging clone and a backup of the previous installation. |
| Tests | 🟢 | 317 tests pass, with a fake GitHub and local repositories (no network). |
| Real use | 🟠 | It has not been used for real work yet and has never installed or updated a project from the real GitHub; only a few EH3D repositories exist to be installed. |
| Interface | 🟡 | The window works in eight languages and its Python bridge is covered by tests; the command line needs only the standard library. |
| Security | 🟡 | Nothing changes without a confirmation or over a checkout with local changes, merges never force, and an evidence log shows edited or reordered lines; the signed-commit policy is optional and there has been no independent review. |
| Integration | 🟡 | ELECTRO-HOBBY-3D-UPDATER hands the EH3D projects over to it; that hand-over has not been run against a real checkout. |
| Real hardware | 🟢 | Not applicable: it runs on the PC of the person using it. |
| Documentation | 🟢 | README in eight languages, the command-line reference and the guide to the window. |

## 🎯 Overview

* **It finds the projects by their manifests:** every public repository with an `eh3d.project.json` of ecosystem `EH3D` is a project, so a new repository appears by having a manifest and nothing in this tool lists the projects.
* **It compares the machine with GitHub:** for each project it reads the version of the local checkout and the one on the default branch of GitHub, and says whether it is installed, up to date, outdated or has new commits.
* **It installs and updates one project at a time, after a confirmation:** the replacement is built and checked in a staging clone before the live installation is touched, and the previous one is kept as a backup that can be restored from the window.
* **Batches are confirmed too:** *Install all missing* and *Update all outdated* are separate, sequential actions through the same safety path. Nothing updates in the background.
* **An evidence log and an optional signed-commit policy:** every attempt is written to a log that can be checked later for edited, removed or reordered lines.
* **A window in eight languages and a command line** (`--cli`) that needs only the standard library, so it also works on a machine without a screen.

## 🧩 Role in EH3D

EH3D-UPDATER is the way to get the suite and keep it current. ELECTRO-HOBBY-3D-UPDATER, the tool above the four ecosystems, hands over to it for the EH3D projects.

## 📂 Repository Structure

```text
EH3D-UPDATER/
├── src/eh3d_updater/       the package: discovery, install, update, evidence, window
│   ├── main.py             the command line (--cli) and the start of the window
│   ├── github_client.py    the versions on GitHub, with no token
│   ├── detect.py           the local checkouts and their versions
│   ├── install.py          install, update (staging clone first), backup and restore
│   ├── project_manifest.py the contract of eh3d.project.json
│   ├── evidence.py         the log of every attempt
│   ├── qt_gui.py, qml/     the Qt Quick window
│   └── i18n.py             the eight languages
├── docs/
│   ├── CLI_REFERENCE.md    every command of the command line
│   └── QML_DESKTOP_GUI.md  the window
├── tests/                  the tests (no network, no board)
├── tools/ci_validate.py    the checks the CI runs
└── eh3d.project.json       the manifest of the project
```

## 🛠️ BUILD & RUN

You need Python 3.10 or newer; the window also needs PySide6 (`pip install ".[gui]"`).

```bash
PYTHONPATH=src python -m pytest tests -q
python -I tools/ci_validate.py
./run.sh --cli status        # run.bat --cli status on Windows
```

## 🔗 Related Projects

* [EH3D-COMMON](https://github.com/JuanenRac/EH3D-COMMON): the project container and the machine types; it can be installed with this tool
* [EH3D-CORE-LIBS](https://github.com/JuanenRac/EH3D-CORE-LIBS): the readers of Gerber, Excellon and G-code; it can be installed with this tool
* [ELECTRO-HOBBY-3D-UPDATER](https://github.com/JuanenRac/ELECTRO-HOBBY-3D-UPDATER): the updater above the four ecosystems, which dispatches to this one
* [URTC-UPDATER](https://github.com/JuanenRac/URTC-UPDATER): the updater of URTC, from which this tool takes its design

## 📚 Documentation & Community

* [Command line reference](docs/CLI_REFERENCE.md) and [the desktop window](docs/QML_DESKTOP_GUI.md).
* [Contributing](CONTRIBUTING.md), [Security policy](SECURITY.md), [Support](SUPPORT.md) and the [Code of Conduct](CODE_OF_CONDUCT.md).

## 👤 AUTHOR

**JuanenRac (Electro Hobby 3D)** · electrohobby3d@gmail.com

## 📜 LICENSE

Software: GPL-3.0-or-later. See [LICENSE](LICENSE).
