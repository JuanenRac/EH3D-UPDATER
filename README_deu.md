<p align="center">
  <img src="images/EH3D_UPDATER_BANNER.svg" alt="EH3D-UPDATER banner" width="100%">
</p>

# 🛠️ EH3D-UPDATER

<p align="center"><a href="README.md">🇺🇸 English</a> | <a href="README_spa.md">🇪🇸 Español</a> | <a href="README_fra.md">🇫🇷 Français</a> | <a href="README_ita.md">🇮🇹 Italiano</a> | 🇩🇪 <b>Deutsch</b> | <a href="README_zho.md">🇨🇳 中文</a> | <a href="README_jpn.md">🇯🇵 日本語</a> | <a href="README_por.md">🇵🇹 Português</a></p>

### Erkennt, installiert und aktualisiert die Repositories der EH3D Fabrication Suite auf Ihrem PC: nichts geschieht von selbst, und eine laufende Installation wird erst ersetzt, nachdem ihr Ersatz gebaut und geprüft wurde

<p align="center">
  <img src="https://img.shields.io/badge/License-GPL%203.0--or--later-blue.svg" alt="GPL 3.0 or later">
  <img src="https://img.shields.io/badge/Language-Python%203.10%2B-blue.svg" alt="Python">
  <img src="https://img.shields.io/badge/Languages-8-00E5FF.svg" alt="Languages">
  <img src="https://img.shields.io/badge/Version-0.0.1-0f6cbd.svg" alt="Version">
  <img src="https://img.shields.io/badge/Maturity-scaffolding-FFB020.svg" alt="Maturity">
</p>

---

**Ehrlichkeitsprüfung - was heute läuft:** eine Befehlszeile und ein Qt-Quick-Fenster, die die EH3D-Repositories über ihre `eh3d.project.json`-Manifeste finden, jede lokale Kopie mit GitHub vergleichen und nach einer Bestätigung jeweils ein Projekt installieren oder aktualisieren. Das Update wird geklont, ohne Zwang zusammengeführt und zuerst in einer Staging-Kopie gebaut und geprüft; die vorherige Installation bleibt als Sicherung erhalten. Es ist der Updater der anderen Ökosysteme der Familie mit den Namen von EH3D, mit 317 Tests, die auf einem Computer mit einem falschen GitHub und lokalen Repositories laufen. Er wurde noch nicht für echte Arbeit benutzt, und es gibt nur EH3D-COMMON und EH3D-CORE-LIBS zum Installieren.

---

> **Stand von Sicherheit (Safety) und IT-Sicherheit:** er ersetzt Dateien auf Ihrem Rechner und führt die Build-Prüfung dessen aus, was er installiert, und tut das daher nur nach ausdrücklicher Bestätigung, nie über eine Kopie mit lokalen Änderungen, und er hält jeden Versuch in einem Beweisprotokoll ohne Geheimnisse fest. Die Signatur eines Commits prüft er nur, wenn Sie diese Richtlinie wählen; er ist kein Sicherheitssystem und steuert keine Maschine.

## 📋 Auf einen Blick

| | |
|---|---|
| Version | `0.0.1` |
| Reifegrad | Gerüst |
| Tests | 317 |
| Technologie-Stack | Python 3.10+ / PySide6 / Qt Quick |
| Auf echter Hardware | Nicht zutreffend: läuft auf dem PC der Person, die ihn benutzt |

## 🚦 Projektstatus

Jede Zeile ist ein Teil dieses Repositorys, und die Ampel sagt, wie weit er heute ist. Sie beruht auf dem, was das Repository zeigen kann (Tests, Builds, Läufe), nicht auf dem, was geplant ist.

🟢 Fertig und überprüft · 🟡 Funktioniert, mit bekannten Grenzen · 🟠 Teilweise fertig oder noch nicht überprüft · 🔴 Nicht gemacht oder funktioniert nicht

| Bereich | Stand | Was das hier bedeutet |
|---|---|---|
| Software | 🟡 | Eine Kommandozeile und ein Qt-Quick-Fenster finden die EH3D-Repositorys über ihre Manifeste, vergleichen sie mit GitHub und installieren oder aktualisieren einzeln, mit einem Staging-Klon und einer Sicherung der vorherigen Installation. |
| Tests | 🟢 | 317 Tests bestehen, mit einem simulierten GitHub und lokalen Repositorys (ohne Netzwerk). |
| Echter Einsatz | 🟠 | Er wurde noch nicht für echte Arbeit benutzt und hat nie ein Projekt vom echten GitHub installiert oder aktualisiert; es gibt nur wenige EH3D-Repositorys zum Installieren. |
| Oberfläche | 🟡 | Das Fenster arbeitet in acht Sprachen und seine Python-Brücke ist durch Tests abgedeckt; die Kommandozeile braucht nur die Standardbibliothek. |
| Sicherheit | 🟡 | Nichts ändert sich ohne Bestätigung oder über einem Checkout mit lokalen Änderungen, Merges erzwingen nie etwas, und ein Nachweisprotokoll zeigt bearbeitete oder umgestellte Zeilen; die Richtlinie signierter Commits ist optional, eine unabhängige Prüfung gab es nicht. |
| Integration | 🟡 | ELECTRO-HOBBY-3D-UPDATER übergibt ihm die EH3D-Projekte; diese Übergabe wurde nicht an einem echten Checkout ausgeführt. |
| Echte Hardware | 🟢 | Nicht zutreffend: es läuft auf dem PC der Person, die es benutzt. |
| Dokumentation | 🟢 | README in acht Sprachen, die Referenz der Kommandozeile und die Anleitung zum Fenster. |

## 🎯 Überblick

* **Er findet die Projekte über ihre Manifeste:** jedes öffentliche Repository mit einer `eh3d.project.json` des Ökosystems `EH3D` ist ein Projekt; ein neues Repository erscheint also dadurch, dass es ein Manifest hat, und nichts in diesem Werkzeug listet die Projekte auf.
* **Er vergleicht den Rechner mit GitHub:** für jedes Projekt liest er die Version der lokalen Kopie und die des Standardzweigs auf GitHub und sagt, ob es installiert, aktuell, veraltet ist oder neue Commits hat.
* **Er installiert und aktualisiert ein Projekt nach dem anderen, nach einer Bestätigung:** der Ersatz wird in einer Staging-Kopie gebaut und geprüft, bevor die laufende Installation berührt wird, und die vorherige bleibt als Sicherung, die sich aus dem Fenster wiederherstellen lässt.
* **Auch Stapel werden bestätigt:** *Alles Fehlende installieren* und *Alles Veraltete aktualisieren* sind getrennte, sequenzielle Aktionen über denselben Sicherheitsweg. Nichts wird im Hintergrund aktualisiert.
* **Ein Beweisprotokoll und eine optionale Richtlinie für signierte Commits:** jeder Versuch wird in ein Protokoll geschrieben, das sich später auf bearbeitete, entfernte oder umgeordnete Zeilen prüfen lässt.
* **Ein Fenster in acht Sprachen und eine Befehlszeile** (`--cli`), die nur die Standardbibliothek braucht und daher auch auf einem Rechner ohne Bildschirm läuft.

## 🧩 Rolle in EH3D

EH3D-UPDATER ist der Weg, die Suite zu bekommen und aktuell zu halten. ELECTRO-HOBBY-3D-UPDATER, das Werkzeug über den vier Ökosystemen, übergibt die EH3D-Projekte an ihn.

## 📂 Repository-Struktur

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

## 🛠️ BAUEN & AUSFÜHREN

Sie brauchen Python 3.10 oder neuer; das Fenster braucht zusätzlich PySide6 (`pip install ".[gui]"`).

```bash
PYTHONPATH=src python -m pytest tests -q
python -I tools/ci_validate.py
./run.sh --cli status        # run.bat --cli status on Windows
```

## 🔗 Verwandte Projekte

* [EH3D-COMMON](https://github.com/JuanenRac/EH3D-COMMON): der Projektcontainer und die Maschinentypen; mit diesem Werkzeug installierbar
* [EH3D-CORE-LIBS](https://github.com/JuanenRac/EH3D-CORE-LIBS): die Leser für Gerber, Excellon und G-Code; mit diesem Werkzeug installierbar
* [ELECTRO-HOBBY-3D-UPDATER](https://github.com/JuanenRac/ELECTRO-HOBBY-3D-UPDATER): der Updater über den vier Ökosystemen, der an dieses delegiert
* [URTC-UPDATER](https://github.com/JuanenRac/URTC-UPDATER): der Updater von URTC, dessen Entwurf dieses Werkzeug übernimmt

## 📚 Dokumentation & Community

* [Referenz der Befehlszeile](docs/CLI_REFERENCE.md) und [das Desktop-Fenster](docs/QML_DESKTOP_GUI.md).
* [Mitwirken](CONTRIBUTING.md), [Sicherheitsrichtlinie](SECURITY.md), [Support](SUPPORT.md) und [Verhaltenskodex](CODE_OF_CONDUCT.md).

## 👤 AUTOR

**JuanenRac (Electro Hobby 3D)** · electrohobby3d@gmail.com

## 📜 LIZENZ

Software: GPL-3.0-or-later. Siehe [LICENSE](LICENSE).
