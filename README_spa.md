<p align="center">
  <img src="images/EH3D_UPDATER_BANNER.svg" alt="EH3D-UPDATER banner" width="100%">
</p>

# 🛠️ EH3D-UPDATER

<p align="center"><a href="README.md">🇺🇸 English</a> | 🇪🇸 <b>Español</b> | <a href="README_fra.md">🇫🇷 Français</a> | <a href="README_ita.md">🇮🇹 Italiano</a> | <a href="README_deu.md">🇩🇪 Deutsch</a> | <a href="README_zho.md">🇨🇳 中文</a> | <a href="README_jpn.md">🇯🇵 日本語</a> | <a href="README_por.md">🇵🇹 Português</a></p>

### Detecta, instala y actualiza en tu PC los repositorios de la EH3D Fabrication Suite: nada ocurre por sí solo, y una instalación en uso solo se reemplaza después de construir y comprobar su sustituta

<p align="center">
  <img src="https://img.shields.io/badge/License-GPL%203.0--or--later-blue.svg" alt="GPL 3.0 or later">
  <img src="https://img.shields.io/badge/Language-Python%203.10%2B-blue.svg" alt="Python">
  <img src="https://img.shields.io/badge/Languages-8-00E5FF.svg" alt="Languages">
  <img src="https://img.shields.io/badge/Version-0.0.1-0f6cbd.svg" alt="Version">
  <img src="https://img.shields.io/badge/Maturity-scaffolding-FFB020.svg" alt="Maturity">
</p>

---

**Comprobación de honestidad - lo que se ejecuta hoy:** una línea de órdenes y una ventana Qt Quick que encuentran los repositorios EH3D por sus manifiestos `eh3d.project.json`, comparan cada copia local con GitHub e instalan o actualizan de uno en uno tras una confirmación. La actualización se clona, se fusiona sin forzar y se construye y comprueba antes en una copia de preparación, y la instalación anterior se conserva como copia de seguridad. Es el actualizador de los otros ecosistemas de la familia con los nombres de EH3D, con 317 tests que se ejecutan en un ordenador con un GitHub falso y repositorios locales. Aún no se ha usado para trabajo real, y solo EH3D-COMMON y EH3D-CORE-LIBS existen para instalar.

---

> **Estado de seguridad (safety) y de seguridad informática:** reemplaza ficheros de tu máquina y ejecuta la comprobación de construcción de lo que instala, así que solo lo hace tras una confirmación explícita, nunca sobre una copia con cambios locales, y anota cada intento en un registro de evidencias sin secretos. Comprueba la firma de un commit solo si eliges esa política; no es un sistema de seguridad funcional y no controla ninguna máquina.

## 📋 De un vistazo

| | |
|---|---|
| Versión | `0.0.1` |
| Madurez | Andamiaje |
| Pruebas | 317 |
| Pila tecnológica | Python 3.10+ / PySide6 / Qt Quick |
| En hardware real | No aplica: se ejecuta en el PC de quien lo usa |

## 🎯 Descripción general

* **Encuentra los proyectos por sus manifiestos:** todo repositorio público con un `eh3d.project.json` del ecosistema `EH3D` es un proyecto, así que un repositorio nuevo aparece por tener un manifiesto y nada en esta herramienta enumera los proyectos.
* **Compara la máquina con GitHub:** de cada proyecto lee la versión de la copia local y la de la rama por defecto de GitHub, y dice si está instalado, al día, desactualizado o con commits nuevos.
* **Instala y actualiza de uno en uno, tras una confirmación:** la sustituta se construye y comprueba en una copia de preparación antes de tocar la instalación en uso, y la anterior se conserva como copia de seguridad que se puede restaurar desde la ventana.
* **Los lotes también se confirman:** *Instalar todo lo que falta* y *Actualizar todo lo desactualizado* son acciones aparte y secuenciales por el mismo camino de seguridad. Nada se actualiza en segundo plano.
* **Un registro de evidencias y una política opcional de commits firmados:** cada intento se escribe en un registro que se puede comprobar después por líneas editadas, borradas o reordenadas.
* **Una ventana en ocho idiomas y una línea de órdenes** (`--cli`) que solo necesita la biblioteca estándar, así que también funciona en una máquina sin pantalla.

## 🧩 Papel en EH3D

EH3D-UPDATER es la forma de obtener la suite y mantenerla al día. ELECTRO-HOBBY-3D-UPDATER, la herramienta por encima de los cuatro ecosistemas, le cede los proyectos EH3D.

## 📂 Estructura del repositorio

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

## 🛠️ COMPILAR Y EJECUTAR

Necesitas Python 3.10 o más reciente; la ventana también necesita PySide6 (`pip install ".[gui]"`).

```bash
PYTHONPATH=src python -m pytest tests -q
python -I tools/ci_validate.py
./run.sh --cli status        # run.bat --cli status on Windows
```

## 🔗 Proyectos relacionados

* [EH3D-COMMON](https://github.com/JuanenRac/EH3D-COMMON): el contenedor de proyecto y los tipos de máquina; se puede instalar con esta herramienta
* [EH3D-CORE-LIBS](https://github.com/JuanenRac/EH3D-CORE-LIBS): los lectores de Gerber, Excellon y G-code; se puede instalar con esta herramienta
* [ELECTRO-HOBBY-3D-UPDATER](https://github.com/JuanenRac/ELECTRO-HOBBY-3D-UPDATER): el actualizador por encima de los cuatro ecosistemas, que delega en este
* [URTC-UPDATER](https://github.com/JuanenRac/URTC-UPDATER): el actualizador de URTC, del que esta herramienta toma su diseño

## 📚 Documentación y comunidad

* [Referencia de la línea de órdenes](docs/CLI_REFERENCE.md) y [la ventana de escritorio](docs/QML_DESKTOP_GUI.md).
* [Cómo contribuir](CONTRIBUTING.md), [política de seguridad](SECURITY.md), [soporte](SUPPORT.md) y [código de conducta](CODE_OF_CONDUCT.md).

## 👤 AUTOR

**JuanenRac (Electro Hobby 3D)** · electrohobby3d@gmail.com

## 📜 LICENCIA

Software: GPL-3.0-or-later. Véase [LICENSE](LICENSE).
