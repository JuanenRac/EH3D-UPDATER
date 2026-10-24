<p align="center">
  <img src="images/EH3D_UPDATER_BANNER.svg" alt="EH3D-UPDATER banner" width="100%">
</p>

# 🛠️ EH3D-UPDATER

<p align="center"><a href="README.md">🇺🇸 English</a> | <a href="README_spa.md">🇪🇸 Español</a> | 🇫🇷 <b>Français</b> | <a href="README_ita.md">🇮🇹 Italiano</a> | <a href="README_deu.md">🇩🇪 Deutsch</a> | <a href="README_zho.md">🇨🇳 中文</a> | <a href="README_jpn.md">🇯🇵 日本語</a> | <a href="README_por.md">🇵🇹 Português</a></p>

### Détecte, installe et met à jour sur votre PC les dépôts de l'EH3D Fabrication Suite : rien ne se fait tout seul, et une installation en service n'est remplacée qu'après la construction et la vérification de son remplaçant

<p align="center">
  <img src="https://img.shields.io/badge/License-GPL%203.0--or--later-blue.svg" alt="GPL 3.0 or later">
  <img src="https://img.shields.io/badge/Language-Python%203.10%2B-blue.svg" alt="Python">
  <img src="https://img.shields.io/badge/Languages-8-00E5FF.svg" alt="Languages">
  <img src="https://img.shields.io/badge/Version-0.0.1-0f6cbd.svg" alt="Version">
  <img src="https://img.shields.io/badge/Maturity-scaffolding-FFB020.svg" alt="Maturity">
</p>

---

**Vérification d'honnêteté - ce qui tourne aujourd'hui :** une ligne de commande et une fenêtre Qt Quick qui trouvent les dépôts EH3D par leurs manifestes `eh3d.project.json`, comparent chaque copie locale à GitHub et installent ou mettent à jour un projet à la fois après confirmation. La mise à jour est clonée, fusionnée sans forcer, puis construite et vérifiée dans une copie de préparation, et l'installation précédente est conservée comme sauvegarde. C'est l'outil de mise à jour des autres écosystèmes de la famille avec les noms d'EH3D, avec 317 tests exécutés sur un ordinateur avec un faux GitHub et des dépôts locaux. Il n'a pas encore servi pour un vrai travail, et seuls EH3D-COMMON et EH3D-CORE-LIBS existent à installer.

---

> **État de la sûreté et de la sécurité :** il remplace des fichiers de votre machine et lance la vérification de construction de ce qu'il installe ; il ne le fait donc qu'après une confirmation explicite, jamais sur une copie ayant des modifications locales, et il consigne chaque tentative dans un journal de preuves sans secrets. Il ne vérifie la signature d'un commit que si vous choisissez cette politique ; ce n'est pas un système de sûreté et il ne pilote aucune machine.

## 📋 En un coup d'œil

| | |
|---|---|
| Version | `0.0.1` |
| Maturité | Échafaudage |
| Tests | 317 |
| Pile technique | Python 3.10+ / PySide6 / Qt Quick |
| Sur matériel réel | Sans objet : il tourne sur le PC de la personne qui l'utilise |

## 🚦 État du projet

Chaque ligne est une partie de ce dépôt et le feu dit où elle en est aujourd'hui. Elle est écrite d'après ce que le dépôt peut montrer (tests, compilations, exécutions), pas d'après ce qui est prévu.

🟢 Fait et vérifié · 🟡 Fonctionne, avec des limites connues · 🟠 À moitié fait ou pas encore vérifié · 🔴 Pas fait ou ne fonctionne pas

| Domaine | État | Ce que cela veut dire ici |
|---|---|---|
| Logiciel | 🟡 | Une ligne de commande et une fenêtre Qt Quick trouvent les dépôts EH3D par leurs manifestes, les comparent à GitHub et installent ou mettent à jour un par un, avec un clone de préparation et une sauvegarde de l'installation précédente. |
| Tests | 🟢 | 317 tests réussissent, avec un faux GitHub et des dépôts locaux (sans réseau). |
| Usage réel | 🟠 | Il n'a pas encore servi à un vrai travail et n'a jamais installé ni mis à jour un projet depuis le vrai GitHub ; il n'existe que quelques dépôts EH3D à installer. |
| Interface | 🟡 | La fenêtre fonctionne en huit langues et son pont Python est couvert par des tests ; la ligne de commande n'a besoin que de la bibliothèque standard. |
| Sécurité | 🟡 | Rien ne change sans confirmation ni sur une copie avec des modifications locales, les fusions ne forcent jamais, et un journal de preuves révèle les lignes modifiées ou réordonnées ; la politique des commits signés est facultative et il n'y a pas eu de revue indépendante. |
| Intégration | 🟡 | ELECTRO-HOBBY-3D-UPDATER lui confie les projets EH3D ; cette délégation n'a pas été exécutée sur une vraie copie. |
| Matériel réel | 🟢 | Sans objet : il tourne sur le PC de la personne qui l'utilise. |
| Documentation | 🟢 | README en huit langues, la référence de la ligne de commande et le guide de la fenêtre. |

## 🎯 Vue d'ensemble

* **Il trouve les projets par leurs manifestes :** tout dépôt public avec un `eh3d.project.json` de l'écosystème `EH3D` est un projet ; un nouveau dépôt apparaît donc en ayant un manifeste, et rien dans cet outil ne liste les projets.
* **Il compare la machine à GitHub :** pour chaque projet il lit la version de la copie locale et celle de la branche par défaut sur GitHub, et dit s'il est installé, à jour, périmé ou avec de nouveaux commits.
* **Il installe et met à jour un projet à la fois, après confirmation :** le remplaçant est construit et vérifié dans une copie de préparation avant de toucher l'installation en service, et la précédente est gardée comme sauvegarde restaurable depuis la fenêtre.
* **Les lots sont aussi confirmés :** *Installer tout ce qui manque* et *Mettre à jour tout ce qui est périmé* sont des actions séparées et séquentielles par le même chemin de sécurité. Rien ne se met à jour en arrière-plan.
* **Un journal de preuves et une politique facultative de commits signés :** chaque tentative est écrite dans un journal qu'on peut vérifier plus tard pour des lignes modifiées, supprimées ou réordonnées.
* **Une fenêtre en huit langues et une ligne de commande** (`--cli`) qui n'exige que la bibliothèque standard, donc utilisable aussi sur une machine sans écran.

## 🧩 Rôle dans EH3D

EH3D-UPDATER est le moyen d'obtenir la suite et de la tenir à jour. ELECTRO-HOBBY-3D-UPDATER, l'outil au-dessus des quatre écosystèmes, lui confie les projets EH3D.

## 📂 Structure du dépôt

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

## 🛠️ COMPILER ET EXÉCUTER

Il faut Python 3.10 ou plus récent ; la fenêtre demande aussi PySide6 (`pip install ".[gui]"`).

```bash
PYTHONPATH=src python -m pytest tests -q
python -I tools/ci_validate.py
./run.sh --cli status        # run.bat --cli status on Windows
```

## 🔗 Projets liés

* [EH3D-COMMON](https://github.com/JuanenRac/EH3D-COMMON): le conteneur de projet et les types de machine ; installable avec cet outil
* [EH3D-CORE-LIBS](https://github.com/JuanenRac/EH3D-CORE-LIBS): les lecteurs de Gerber, Excellon et G-code ; installable avec cet outil
* [ELECTRO-HOBBY-3D-UPDATER](https://github.com/JuanenRac/ELECTRO-HOBBY-3D-UPDATER): l'outil de mise à jour au-dessus des quatre écosystèmes, qui délègue à celui-ci
* [URTC-UPDATER](https://github.com/JuanenRac/URTC-UPDATER): l'outil de mise à jour d'URTC, dont celui-ci reprend la conception

## 📚 Documentation et communauté

* [Référence de la ligne de commande](docs/CLI_REFERENCE.md) et [la fenêtre de bureau](docs/QML_DESKTOP_GUI.md).
* [Contribuer](CONTRIBUTING.md), [politique de sécurité](SECURITY.md), [support](SUPPORT.md) et [code de conduite](CODE_OF_CONDUCT.md).

## 👤 AUTEUR

**JuanenRac (Electro Hobby 3D)** · electrohobby3d@gmail.com

## 📜 LICENCE

Logiciel : GPL-3.0-or-later. Voir [LICENSE](LICENSE).
