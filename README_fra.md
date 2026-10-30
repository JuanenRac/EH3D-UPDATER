<p align="center">
  <img src="images/EH3D_UPDATER_BANNER.svg" alt="EH3D-UPDATER banner" width="100%">
</p>

# 🛠️ EH3D-UPDATER

<p align="center"><a href="README.md">🇺🇸 English</a> | <a href="README_spa.md">🇪🇸 Español</a> | 🇫🇷 <b>Français</b> | <a href="README_ita.md">🇮🇹 Italiano</a> | <a href="README_deu.md">🇩🇪 Deutsch</a> | <a href="README_zho.md">🇨🇳 中文</a> | <a href="README_jpn.md">🇯🇵 日本語</a> | <a href="README_por.md">🇵🇹 Português</a></p>

### Détecte, installe et met à jour sur ton PC les dépôts de l'EH3D Fabrication Suite : rien ne se passe tout seul, et une installation en service n'est remplacée qu'après que son remplaçant a été construit et vérifié

<p align="center">
  <img src="https://img.shields.io/badge/License-GPL%203.0--or--later-blue.svg" alt="GPL 3.0 or later">
  <img src="https://img.shields.io/badge/Stack-Python%203.10%2B-3776AB.svg" alt="Python">
  <img src="https://img.shields.io/badge/Languages-8-00E5FF.svg" alt="Languages">
  <img src="https://img.shields.io/badge/Version-0.0.2-0f6cbd.svg" alt="Version">
  <img src="https://img.shields.io/badge/Maturity-scaffolding-FFB020.svg" alt="Maturity">
</p>

---

**Vérification d'honnêteté - ce qui tourne aujourd'hui :** une ligne de commande et une fenêtre Qt Quick qui trouvent les dépôts EH3D par leurs manifestes `eh3d.project.json`, comparent chaque copie locale à GitHub et installent ou mettent à jour un projet à la fois après une confirmation. La mise à jour est clonée, fusionnée sans forcer, puis construite et vérifiée d'abord dans un clone de préparation, et l'installation précédente est gardée en sauvegarde. C'est l'outil de mise à jour des autres écosystèmes de la famille avec les noms d'EH3D, avec 322 tests qui tournent sur un ordinateur avec un faux GitHub et des dépôts locaux. Il n'a pas encore servi à un travail réel et n'a jamais installé ni mis à jour un projet depuis le vrai GitHub.

---

> **État de la sûreté et de la sécurité :** il remplace des fichiers sur ta machine et lance le contrôle de construction de ce qu'il installe, donc il ne le fait qu'après une confirmation explicite, jamais sur une copie ayant des modifications locales, et il consigne chaque tentative dans un journal de preuves qui ne contient aucun secret. Il ne vérifie la signature d'un commit que si tu choisis cette politique ; ce n'est pas un système de sûreté et il ne pilote aucune machine.

## 📋 En un coup d'œil

| | |
|---|---|
| Version | `0.0.2` |
| Maturité | Échafaudage |
| Tests | 322 |
| Pile technique | Python 3.10+ / PySide6 / Qt Quick |
| Sur du matériel réel | Sans objet : il tourne sur le PC de la personne qui l'utilise |

**Aller à  :** [Présentation](#-présentation) · [Architecture](#-architecture) · [Démarrage rapide](#-démarrage-rapide) · [Tests](#-tests) · [Structure](#-structure-du-dépôt) · [Liés](#-projets-liés)

## 🚦 État du projet

Chaque ligne est une partie de ce dépôt et le feu dit où elle en est aujourd'hui. Elle est écrite d'après ce que le dépôt peut montrer (tests, compilations, exécutions), pas d'après ce qui est prévu.

🟢 Fait et vérifié · 🟡 Fonctionne, avec des limites connues · 🟠 À moitié fait ou pas encore vérifié · 🔴 Pas fait ou ne fonctionne pas

| Domaine | État | Ce que cela veut dire ici |
|---|---|---|
| Logiciel | 🟡 | Une ligne de commande et une fenêtre Qt Quick trouvent les dépôts EH3D par leurs manifestes, les comparent à GitHub et installent ou mettent à jour un projet à la fois, avec un clone de préparation et une sauvegarde de l'installation précédente. |
| Tests | 🟡 | 322 tests réussissent (`pytest`), avec un faux GitHub et des dépôts locaux (sans réseau) ; un autre est ignoré quand une copie voisine dont il a besoin manque. |
| Découverte | 🟡 | Les dépôts publics ne sont que des candidats : un projet entre dans l'écosystème quand son `eh3d.project.json` à la racine est valide et dit `EH3D` ; testé contre une fausse liste, pas contre le vrai GitHub. |
| Usage réel | 🟠 | Il n'a pas encore servi à un travail réel et n'a jamais installé ni mis à jour un projet depuis le vrai GitHub ; seuls quelques dépôts EH3D existent à installer. |
| Interface | 🟡 | La fenêtre fonctionne en huit langues et son pont Python est couvert par des tests ; la ligne de commande n'a besoin que de la bibliothèque standard. |
| Sécurité | 🟡 | Rien ne change sans confirmation ni sur une copie ayant des modifications locales, les fusions ne forcent jamais et un journal de preuves montre les lignes modifiées ou réordonnées ; la politique de commits signés est facultative et il n'y a pas eu de revue indépendante. |
| Intégration | 🟡 | ELECTRO-HOBBY-3D-UPDATER lui passe les projets EH3D ; ce passage n'a pas été exécuté sur une vraie copie. |
| Matériel réel | 🟡 | Sans objet : il tourne sur le PC de la personne qui l'utilise. |
| Documentation | 🟡 | README en huit langues, la référence de la ligne de commande et le guide de la fenêtre. |

## 🎯 Présentation

* **Il trouve les projets par leurs manifestes :** les dépôts publics du propriétaire sur GitHub ne sont qu'une liste de candidats ; l'un est un projet quand son `eh3d.project.json` à la racine est valide et déclare l'écosystème `EH3D`, donc un nouveau dépôt apparaît en ayant un manifeste et rien dans cet outil ne liste les projets. En local, un nom de dossier ne suffit jamais pour entrer dans l'écosystème.
* **Il compare la machine à GitHub :** pour chaque projet, il lit la version de la copie locale et celle de la branche par défaut de GitHub, et dit s'il est installé, à jour, périmé ou a de nouveaux commits (une version égale avec de nouveaux commits est repérée par un `git ls-remote`).
* **Il installe et met à jour un projet à la fois, après une confirmation :** le remplaçant est construit et vérifié dans un clone de préparation avant de toucher l'installation en service, et la précédente est gardée en sauvegarde, restaurable depuis la fenêtre ou avec `restore-backup`.
* **Les lots sont aussi confirmés :** *Installer tout ce qui manque* et *Mettre à jour tout ce qui est périmé* sont des actions séparées et séquentielles par le même chemin de sécurité. Rien ne se met à jour en arrière-plan.
* **Un journal de preuves et une politique facultative de commits signés :** chaque tentative est écrite dans un journal qu'on peut vérifier plus tard pour y trouver des lignes modifiées, retirées ou réordonnées.
* **Profils de poste :** un profil nommé liste les projets avec lesquels une machine travaille, et la fenêtre et les commandes le suivent.
* **Une fenêtre en huit langues et une ligne de commande** (`--cli`) qui n'a besoin que de la bibliothèque standard, donc elle marche aussi sur une machine sans écran.

## 🧩 Rôle dans EH3D

EH3D-UPDATER est le moyen d'obtenir la suite et de la garder à jour. ELECTRO-HOBBY-3D-UPDATER, l'outil au-dessus des quatre écosystèmes, lui passe la main pour les projets EH3D. Un nouveau dépôt EH3D n'exige rien ici : il apparaît dès qu'il est public et porte un manifeste valide.

## 🏛️ Architecture

<p align="center">
  <img src="images/architecture.svg" alt="Architecture de EH3D-UPDATER : qui l'utilise, ce qu'il contient et de quoi il dépend" width="100%">
</p>

Comment les parties de ce dépôt s'articulent : qui l'utilise, ce qu'il contient et de quoi il dépend. L'image est dessinée à partir de `docs/architecture.json` et vérifiée par rapport au code.

## ✨ Fonctionnalités

* **Le manifeste décide :** la découverte, le nom, la version, la commande de compilation et les notes viennent du `eh3d.project.json` propre au dépôt ; un candidat dont le manifeste est invalide, ou dont la version est inférieure à celle installée, est refusé avant que rien ne soit touché.
* **Une copie saine n'est jamais remplacée :** une vraie modification locale ou une branche divergente fait échouer la mise à jour bruyamment, jamais une réinitialisation silencieuse (`--ff-only` avec `--no-build`).
* **Aperçu avant la mise à jour :** `update --preview` montre le commit candidat, son auteur, l'état de sa signature et les fichiers de build et d'outils qu'il change, puis s'arrête.
* **Notifier seulement :** `check` liste ce qui pourrait être mis à jour, ne change rien et sort avec 10 quand quelque chose peut l'être (une notification de bureau est facultative).
* **Sauvegardes limitées :** l'installation précédente est gardée sous `<nom>.backup-<8 chiffres hex>` ; les 2 plus récentes sont conservées par défaut et `clean-backups` élague le reste.
* **Poli avec le réseau :** les requêtes sont retentées avec attente, un `Retry-After` court est attendu, la liste des dépôts est mise en cache avec `If-None-Match` (un `304` ne coûte aucun quota) et un GitHub injoignable replie sur l'état local avec un avertissement.

## 🔒 Sécurité et protection

| Menace | Défense |
|---|---|
| Une mise à jour non désirée ou par surprise | rien ne tourne en arrière-plan : `install` et `update` prennent un nom de projet et une confirmation, et les boutons de lot de la fenêtre sont séparés, séquentiels et confirmés |
| Un candidat cassé qui remplace une installation qui marchait | le candidat est cloné, fusionné sans forcer, construit et vérifié dans un clone de préparation ; le dossier en service n'est échangé par deux renommages qu'ensuite, et le précédent est gardé en sauvegarde restaurable |
| Perdre du travail local | une copie avec des modifications locales ou une branche divergente n'est jamais remplacée : la mise à jour échoue bruyamment |
| Un dépôt qui fait semblant de faire partie de la suite | un dépôt n'entre que si son manifeste à la racine est valide et déclare `EH3D` ; un candidat de version inférieure à celle installée est refusé |
| Un commit d'origine inconnue | politique facultative : avec `EH3D_UPDATER_REQUIRE_SIGNED=1` (ou le réglage) et un fichier de signataires autorisés, un commit doit être signé ; par défaut un commit non signé est installé avec un avertissement, et `update --preview` montre d'abord l'état de la signature |
| Altérer le journal de ce qui s'est passé | chaque tentative d'installation ou de mise à jour est une ligne d'un journal de preuves qui porte le hachage de la ligne précédente ; `evidence` vérifie la chaîne et sort avec 1 quand une ligne a été modifiée, retirée ou réordonnée |
| Fuite de secrets | le journal de preuves ne contient aucun secret ; GitHub est lu sans jeton (un `GITHUB_TOKEN` facultatif ne fait que relever la limite de requêtes) ; l'outil ne l'affiche jamais |
| Un script de validation qui ne peut pas tourner ici | une installation qu'on ne peut pas valider faute d'outil est refusée sauf si tu l'acceptes (le réglage `validation_unavailable` ou `EH3D_UPDATER_ACCEPT_UNAVAILABLE_VALIDATION=1`) |
| Deux instances à la fois | une instance qui en trouve une autre au travail sur l'espace de travail refuse de nettoyer ou de restaurer des sauvegardes |

**Ce qui n'est pas défendu :** le script de construction d'un projet installé est le code de ce projet et s'exécute avec tes droits, n'installe donc que ce à quoi tu fais confiance ; les commits non signés sont acceptés par défaut ; et l'outil n'a pas eu de revue indépendante. Signale une vulnérabilité en privé (voir [SECURITY.md](SECURITY.md)).

## 🔌 Interfaces

| Interface | Ce que c'est | Où |
|---|---|---|
| Fenêtre | une fenêtre Qt Quick en huit langues (le mode par défaut ; demande l'extra facultatif `PySide6`) | `qt_gui.py`, `qml/Main.qml`, [docs/QML_DESKTOP_GUI.md](docs/QML_DESKTOP_GUI.md) |
| Ligne de commande | `eh3d-updater --cli` avec `status`, `install`, `update`, `check`, `clean-backups`, `restore-backup` et `evidence` ; codes de sortie 0, 1 et 10 (quelque chose peut être mis à jour) | [docs/CLI_REFERENCE.md](docs/CLI_REFERENCE.md) |
| GitHub | `GET /users/<propriétaire>/repos` (mis en cache avec `If-None-Match`) et le manifeste brut de chaque candidat ; aucun jeton nécessaire | `github_client.py` |
| L'espace de travail | les dossiers à côté de l'outil, `<nom>.backup-xxxxxxxx` pour les installations précédentes et `.eh3d-updater/evidence.jsonl` pour le journal de preuves | `install.py`, `evidence.py` |
| Réglages | `~/.eh3d_updater_settings.json` (langue, espace de travail, profil, sauvegardes gardées, politique de signature) | `settings.py` |

## ⚙️ Configuration

Rien n'est à configurer pour démarrer. Les choix mémorisés vivent dans `~/.eh3d_updater_settings.json`, et certains peuvent aussi être donnés en options ou en variables d'environnement.

| Réglage | Défaut | Plage | Ce qu'il fait |
|---|---|---|---|
| `workspace_root` / `--workspace` | le dossier parent de l'outil | un dossier | où vivent les copies, les sauvegardes et le journal de preuves |
| `lang` | la langue du système | en, es, de, fr, it, ja, zh, pt | la langue de la fenêtre |
| `profile` / `--profile` | aucun (tous les projets) | un nom de profil défini ; un nom non défini est une erreur | limite `status`, `check`, `install` et `update` aux projets d'un profil de poste |
| `backups_to_keep` / `clean-backups --keep` | 2 | un nombre entier de 0 ou plus | combien d'installations précédentes sont gardées par projet |
| `require_signed_commits`, `allowed_signers_file` / `EH3D_UPDATER_REQUIRE_SIGNED=1`, `EH3D_UPDATER_ALLOWED_SIGNERS` | désactivé | activé ou désactivé | refuser les commits non signés par un signataire autorisé |
| `validation_unavailable` / `EH3D_UPDATER_ACCEPT_UNAVAILABLE_VALIDATION=1` | refuser | refuser ou accepter | que faire quand la validation d'un projet ne peut pas tourner faute d'outil |
| `GITHUB_TOKEN` | aucun | un jeton GitHub | ne fait que relever la limite de requêtes de la liste ; jamais obligatoire |
| `--no-build` (install, update) | désactivé | activé ou désactivé | cloner ou récupérer seulement, sans le contrôle de construction du projet (une simple avance rapide) |

Les valeurs réseau sont des constantes : 10 s par requête, jusqu'à 8 requêtes à la fois, 3 essais avec attente et un `Retry-After` d'au plus 60 s.

## 🚀 Démarrage rapide

Il faut Python 3.10 ou plus récent ; la fenêtre demande aussi PySide6 (`pip install ".[gui]"`).

```bash
./run.sh --cli status          # run.bat --cli status on Windows
./run.sh --cli status --offline --json
./run.sh --cli check           # exit code 10 when something can be updated
./run.sh --cli update EH3D-COMMON --preview
./run.sh --cli install EH3D-CORE-LIBS
```

`run.sh` / `run.bat` sans `--cli` ouvrent la fenêtre. `install` et `update` demandent une confirmation avant de toucher à quoi que ce soit, et prennent toujours un nom de projet.

## 🧪 Tests

La suite compte 322 tests qui réussissent (`pytest tests`), et un autre qui est ignoré quand une copie voisine dont il a besoin n'est pas à côté de celle-ci. Ils tournent avec un faux GitHub et des dépôts locaux, sans réseau, et couvrent le contrat du manifeste, la découverte, la comparaison des versions et des commits, l'installation et la mise à jour avec le clone de préparation et les refus (modifications locales, branche divergente, version inférieure, manifeste invalide, construction qui échoue), les sauvegardes et la restauration, la chaîne de preuves, la politique de signature, les réglages et profils, les messages et les huit langues de la fenêtre, et le pont Python de la fenêtre (hors écran). Un test vérifie aussi que l'arborescence de chaque README liste chaque entrée versionnée de premier niveau. La CI les exécute sous Linux et sous Windows, plus `python tools/ci_validate.py` et un contrôle de syntaxe de chaque fichier Python.

## 🏗️ Compilation et publication

La version se trouve dans `pyproject.toml`, dans `eh3d.project.json` et dans le paquet, et chaque version a son entrée dans [CHANGELOG.md](CHANGELOG.md). `build.sh` / `build.bat` installent le paquet et le vérifient, `build-test.sh` / `build-test.bat` exécutent en plus les tests et `test.sh` / `test.bat` n'exécutent que les tests, chacun dans un panneau en direct ; la version ne change pas. Les versions sont publiées sur GitHub ; l'outil s'installe depuis ce dépôt avec pip et n'est pas sur PyPI.

## 📂 Structure du dépôt

<p align="center">
  <img src="images/repository-structure.svg" alt="Structure du dépôt EH3D-UPDATER" width="100%">
</p>

<details>
<summary>Version texte de l'arborescence</summary>

```text
EH3D-UPDATER/
├── src/eh3d_updater/
│   ├── main.py                                  la ligne de commande et le démarrage de la fenêtre
│   ├── github_client.py detect.py               les versions sur GitHub et les copies locales
│   ├── project_manifest.py registry.py          le contrat du manifeste et sa forme d'exécution
│   ├── install.py commits.py                    installer, mettre à jour, sauvegarder ; comparer les commits
│   ├── evidence.py signature.py                 le journal de preuves et la politique de signature
│   ├── qt_gui.py qml/                           la fenêtre Qt Quick et son QML
│   ├── i18n.py messages.py                      les huit langues et les messages en codes
│   └── settings.py profiles.py                  ce qui est mémorisé et les profils de poste
├── tests/                                       sans réseau : un faux GitHub et des dépôts locaux
├── docs/                                        la référence de la ligne de commande, le guide de la fenêtre et les données des deux images
├── tools/                                       CI, construction, README, icône et images
├── images/                                      bannière et images d'Architecture et de Structure du dépôt
├── .github/                                     workflows de CI et de publication, modèles d'issues et de pull requests
├── build.sh build.bat                           installe et vérifie le paquet dans un panneau en direct
├── build-test.sh build-test.bat                 pareil, puis les tests
├── run.sh run.bat                               ouvre la fenêtre, ou la ligne de commande avec --cli
├── bump*.py                                     les scripts qui montent la version
├── eh3d.project.json                            manifeste : version, rôle, maturité et commande de compilation
├── run-gui.vbs                                  ouvre la fenêtre sans console sous Windows
├── pyproject.toml                               le paquet Python et ses extras
├── CHANGELOG.md                                 ce qui a changé dans chaque version
├── SECURITY.md SUPPORT.md                       signaler une vulnérabilité et poser des questions
├── CONTRIBUTING.md CODE_OF_CONDUCT.md LICENSE   contribuer, code de conduite et licence
└── LICENSE.md                                   le texte de la licence en Markdown
```

</details>

## 🗺️ Feuille de route et limites connues

**Limites connues aujourd'hui**

* Il n'a jamais installé ni mis à jour un projet depuis le vrai GitHub : tout est testé avec un faux GitHub et des dépôts locaux, et seuls quelques dépôts EH3D existent à installer.
* Le passage depuis ELECTRO-HOBBY-3D-UPDATER n'a pas été exécuté sur une vraie copie.
* Les commits ne sont pas obligatoirement signés par défaut ; la politique est facultative.
* Le script de construction d'un projet installé s'exécute avec tes droits.
* L'outil n'a pas eu de revue indépendante et n'est pas sur PyPI.

**Ensuite**

* Installer et mettre à jour un vrai projet de bout en bout avec le vrai GitHub et noter ce qui apparaît.
* Exécuter le passage depuis ELECTRO-HOBBY-3D-UPDATER sur une vraie copie.
* Décider si les commits signés deviennent la valeur par défaut de la suite.

## 🌍 Langues

Le README et les textes existent en anglais, espagnol, français, italien, allemand, chinois, japonais et portugais européen.

## 🔗 Projets liés

* [EH3D-COMMON](https://github.com/JuanenRac/EH3D-COMMON) : le conteneur de projet et les types de machine ; s'installe avec cet outil
* [EH3D-CORE-LIBS](https://github.com/JuanenRac/EH3D-CORE-LIBS) : les lecteurs de Gerber, Excellon et G-code ; s'installe avec cet outil
* [ELECTRO-HOBBY-3D-UPDATER](https://github.com/JuanenRac/ELECTRO-HOBBY-3D-UPDATER) : l'outil de mise à jour au-dessus des quatre écosystèmes, qui passe la main à celui-ci
* [URTC-UPDATER](https://github.com/JuanenRac/URTC-UPDATER) : l'outil de mise à jour d'URTC, dont celui-ci reprend la conception

## 📚 Documentation

* [Référence de la ligne de commande](docs/CLI_REFERENCE.md) : chaque commande, option et code de sortie.
* [La fenêtre de bureau](docs/QML_DESKTOP_GUI.md) : comment la fenêtre Qt Quick repose sur les mêmes services que la ligne de commande.
* [Journal des modifications](CHANGELOG.md)

## 🤝 Contribuer et communauté

* Avant une pull request, exécute `PYTHONPATH=src python -m pytest tests -q` et `python -I tools/ci_validate.py` : tout doit réussir. Voir [CONTRIBUTING.md](CONTRIBUTING.md) et le [code de conduite](CODE_OF_CONDUCT.md).
* Le README existe en huit langues : une modification du texte se fait dans les huit fichiers, et les deux images sont dessinées à partir de `docs/architecture.json` et `docs/structure.json` par `tools/make_architecture.py` et `tools/make_structure.py`.
* Un changement d'un texte visible par l'utilisateur va dans les huit langues de `i18n.py` ; une décision de sécurité se prend dans les services Python, jamais dans le QML.
* Signalez une vulnérabilité en privé : [SECURITY.md](SECURITY.md). Questions, idées et rapports : electrohobby3d@gmail.com ([SUPPORT.md](SUPPORT.md)).

## 👤 AUTEUR

**JuanenRac (Electro Hobby 3D)** · electrohobby3d@gmail.com

## 📜 LICENCE

Logiciel : GPL-3.0-or-later. Voir [LICENSE](LICENSE). Les conceptions matérielles de la suite utilisent la CERN OHL-S.
