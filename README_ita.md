<p align="center">
  <img src="images/EH3D_UPDATER_BANNER.svg" alt="EH3D-UPDATER banner" width="100%">
</p>

# 🛠️ EH3D-UPDATER

<p align="center"><a href="README.md">🇺🇸 English</a> | <a href="README_spa.md">🇪🇸 Español</a> | <a href="README_fra.md">🇫🇷 Français</a> | 🇮🇹 <b>Italiano</b> | <a href="README_deu.md">🇩🇪 Deutsch</a> | <a href="README_zho.md">🇨🇳 中文</a> | <a href="README_jpn.md">🇯🇵 日本語</a> | <a href="README_por.md">🇵🇹 Português</a></p>

### Rileva, installa e aggiorna sul tuo PC i repository della EH3D Fabrication Suite: niente accade da solo, e un'installazione in uso viene sostituita solo dopo che la sostituta è stata costruita e verificata

<p align="center">
  <img src="https://img.shields.io/badge/License-GPL%203.0--or--later-blue.svg" alt="GPL 3.0 or later">
  <img src="https://img.shields.io/badge/Language-Python%203.10%2B-blue.svg" alt="Python">
  <img src="https://img.shields.io/badge/Languages-8-00E5FF.svg" alt="Languages">
  <img src="https://img.shields.io/badge/Version-0.0.1-0f6cbd.svg" alt="Version">
  <img src="https://img.shields.io/badge/Maturity-scaffolding-FFB020.svg" alt="Maturity">
</p>

---

**Controllo di onestà - cosa funziona oggi:** una riga di comando e una finestra Qt Quick che trovano i repository EH3D tramite i loro manifest `eh3d.project.json`, confrontano ogni copia locale con GitHub e installano o aggiornano un progetto alla volta dopo una conferma. L'aggiornamento viene clonato, unito senza forzare e costruito e verificato prima in una copia di preparazione, e l'installazione precedente viene conservata come backup. È l'aggiornatore degli altri ecosistemi della famiglia con i nomi di EH3D, con 317 test eseguiti su un computer con un GitHub finto e repository locali. Non è ancora stato usato per lavoro reale, e esistono da installare solo EH3D-COMMON e EH3D-CORE-LIBS.

---

> **Stato di sicurezza (safety) e di sicurezza informatica:** sostituisce file sulla tua macchina ed esegue il controllo di costruzione di ciò che installa, quindi lo fa solo dopo una conferma esplicita, mai su una copia con modifiche locali, e registra ogni tentativo in un registro di evidenze senza segreti. Controlla la firma di un commit solo se scegli quella politica; non è un sistema di sicurezza funzionale e non controlla alcuna macchina.

## 📋 In breve

| | |
|---|---|
| Versione | `0.0.1` |
| Maturità | Impalcatura |
| Test | 317 |
| Stack tecnologico | Python 3.10+ / PySide6 / Qt Quick |
| Su hardware reale | Non applicabile: gira sul PC di chi lo usa |

## 🎯 Panoramica

* **Trova i progetti tramite i loro manifest:** ogni repository pubblico con un `eh3d.project.json` dell'ecosistema `EH3D` è un progetto, quindi un nuovo repository compare avendo un manifest e nulla in questo strumento elenca i progetti.
* **Confronta la macchina con GitHub:** per ogni progetto legge la versione della copia locale e quella del ramo predefinito su GitHub, e dice se è installato, aggiornato, obsoleto o con nuovi commit.
* **Installa e aggiorna un progetto alla volta, dopo una conferma:** la sostituta viene costruita e verificata in una copia di preparazione prima di toccare l'installazione in uso, e la precedente viene conservata come backup ripristinabile dalla finestra.
* **Anche i lotti sono confermati:** *Installa tutto ciò che manca* e *Aggiorna tutto ciò che è obsoleto* sono azioni separate e sequenziali attraverso lo stesso percorso di sicurezza. Nulla si aggiorna in background.
* **Un registro di evidenze e una politica facoltativa di commit firmati:** ogni tentativo è scritto in un registro verificabile in seguito per righe modificate, rimosse o riordinate.
* **Una finestra in otto lingue e una riga di comando** (`--cli`) che richiede solo la libreria standard, quindi funziona anche su una macchina senza schermo.

## 🧩 Ruolo in EH3D

EH3D-UPDATER è il modo di ottenere la suite e tenerla aggiornata. ELECTRO-HOBBY-3D-UPDATER, lo strumento sopra i quattro ecosistemi, gli passa i progetti EH3D.

## 📂 Struttura del repository

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

## 🛠️ COMPILARE ED ESEGUIRE

Serve Python 3.10 o più recente; la finestra richiede anche PySide6 (`pip install ".[gui]"`).

```bash
PYTHONPATH=src python -m pytest tests -q
python -I tools/ci_validate.py
./run.sh --cli status        # run.bat --cli status on Windows
```

## 🔗 Progetti correlati

* [EH3D-COMMON](https://github.com/JuanenRac/EH3D-COMMON): il contenitore di progetto e i tipi di macchina; installabile con questo strumento
* [EH3D-CORE-LIBS](https://github.com/JuanenRac/EH3D-CORE-LIBS): i lettori di Gerber, Excellon e G-code; installabile con questo strumento
* [ELECTRO-HOBBY-3D-UPDATER](https://github.com/JuanenRac/ELECTRO-HOBBY-3D-UPDATER): l'aggiornatore sopra i quattro ecosistemi, che delega a questo
* [URTC-UPDATER](https://github.com/JuanenRac/URTC-UPDATER): l'aggiornatore di URTC, da cui questo strumento prende il progetto

## 📚 Documentazione e comunità

* [Riferimento della riga di comando](docs/CLI_REFERENCE.md) e [la finestra desktop](docs/QML_DESKTOP_GUI.md).
* [Contribuire](CONTRIBUTING.md), [politica di sicurezza](SECURITY.md), [supporto](SUPPORT.md) e [codice di condotta](CODE_OF_CONDUCT.md).

## 👤 AUTORE

**JuanenRac (Electro Hobby 3D)** · electrohobby3d@gmail.com

## 📜 LICENZA

Software: GPL-3.0-or-later. Vedi [LICENSE](LICENSE).
