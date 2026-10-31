<p align="center">
  <img src="images/EH3D_UPDATER_BANNER.svg" alt="EH3D-UPDATER banner" width="100%">
</p>

# 🛠️ EH3D-UPDATER

<p align="center"><a href="README.md">🇺🇸 English</a> | 🇪🇸 <b>Español</b> | <a href="README_fra.md">🇫🇷 Français</a> | <a href="README_ita.md">🇮🇹 Italiano</a> | <a href="README_deu.md">🇩🇪 Deutsch</a> | <a href="README_zho.md">🇨🇳 中文</a> | <a href="README_jpn.md">🇯🇵 日本語</a> | <a href="README_por.md">🇵🇹 Português</a></p>

### Detecta, instala y actualiza en tu PC los repositorios de la EH3D Fabrication Suite: nada ocurre por sí solo, y una instalación en uso solo se reemplaza después de construir y comprobar su sustituto

<p align="center">
  <img src="https://img.shields.io/badge/License-GPL%203.0--or--later-blue.svg" alt="GPL 3.0 or later">
  <img src="https://img.shields.io/badge/Stack-Python%203.10%2B-3776AB.svg" alt="Python">
  <img src="https://img.shields.io/badge/Languages-8-00E5FF.svg" alt="Languages">
  <img src="https://img.shields.io/badge/Version-0.0.2-0f6cbd.svg" alt="Version">
  <img src="https://img.shields.io/badge/Maturity-scaffolding-FFB020.svg" alt="Maturity">
</p>

---

**Comprobación de honestidad - lo que se ejecuta hoy:** una línea de comandos y una ventana Qt Quick que encuentran los repositorios EH3D por sus manifiestos `eh3d.project.json`, comparan cada copia local con GitHub e instalan o actualizan de uno en uno tras una confirmación. La actualización se clona, se fusiona sin forzar y se construye y comprueba antes en un clon de preparación, y la instalación anterior se guarda como copia de seguridad. Es el actualizador de los otros ecosistemas de la familia con los nombres de EH3D, con 334 pruebas que se ejecutan en un ordenador con un GitHub simulado y repositorios locales. Todavía no se ha usado para trabajo real y nunca ha instalado ni actualizado un proyecto desde el GitHub real.

---

> **Estado de seguridad (safety) y de seguridad informática:** reemplaza ficheros en tu máquina y ejecuta la comprobación de construcción de lo que instala, así que solo lo hace tras una confirmación explícita, nunca sobre una copia con cambios locales, y registra cada intento en un registro de evidencias que no lleva secretos. Comprueba la firma de un commit solo si eliges esa política; no es un sistema de seguridad (safety) y no controla ninguna máquina.

## 📋 De un vistazo

| | |
|---|---|
| Versión | `0.0.2` |
| Madurez | Andamiaje |
| Pruebas | 334 |
| Pila tecnológica | Python 3.10+ / PySide6 / Qt Quick |
| En hardware real | No aplica: se ejecuta en el PC de la persona que lo usa |

**Ir a:** [Resumen](#-resumen) · [Arquitectura](#-arquitectura) · [Inicio rápido](#-inicio-rápido) · [Pruebas](#-pruebas) · [Estructura](#-estructura-del-repositorio) · [Relacionados](#-proyectos-relacionados)

## 🚦 Estado del proyecto

Cada línea es una parte de este repositorio y la luz dice hasta dónde llega hoy. Se escribe con lo que el repositorio puede demostrar (pruebas, compilaciones, ejecuciones), no con lo previsto.

🟢 Hecho y verificado · 🟡 Funciona, con límites conocidos · 🟠 Hecho a medias o sin verificar · 🔴 Sin hacer o sin funcionar

| Área | Estado | Qué significa aquí |
|---|---|---|
| Software | 🟡 | Una línea de comandos y una ventana Qt Quick encuentran los repositorios EH3D por sus manifiestos, los comparan con GitHub e instalan o actualizan de uno en uno, con un clon de preparación y una copia de la instalación anterior. |
| Pruebas | 🟡 | Pasan 334 pruebas (`pytest`), con un GitHub simulado y repositorios locales (sin red); otra se omite cuando falta una copia hermana que necesita. |
| Descubrimiento | 🟡 | Los repositorios públicos son solo candidatos: un proyecto entra en el ecosistema cuando su `eh3d.project.json` de la raíz valida y dice `EH3D`; probado con un listado simulado, no ejecutado contra el GitHub real. |
| Uso real | 🟠 | Todavía no se ha usado para trabajo real y nunca ha instalado ni actualizado un proyecto desde el GitHub real; solo existen unos pocos repositorios EH3D para instalar. |
| Interfaz | 🟡 | La ventana funciona en ocho idiomas y su puente de Python está cubierto por pruebas; la línea de comandos solo necesita la biblioteca estándar. |
| Seguridad | 🟡 | Nada cambia sin una confirmación ni sobre una copia con cambios locales, las fusiones nunca fuerzan y un registro de evidencias muestra las líneas editadas o reordenadas; la política de commits firmados es opcional y no ha habido revisión independiente. |
| Integración | 🟡 | ELECTRO-HOBBY-3D-UPDATER le pasa los proyectos EH3D; ese traspaso no se ha ejecutado contra una copia real. |
| Hardware real | 🟡 | No aplica: se ejecuta en el PC de la persona que lo usa. |
| Documentación | 🟡 | README en ocho idiomas, la referencia de la línea de comandos y la guía de la ventana. |

## 🎯 Resumen

* **Encuentra los proyectos por sus manifiestos:** los repositorios públicos del propietario en GitHub son solo una lista de candidatos; uno es un proyecto cuando su `eh3d.project.json` de la raíz valida y declara el ecosistema `EH3D`, así que un repositorio nuevo aparece por tener un manifiesto y nada en esta herramienta enumera los proyectos. En local, el nombre de una carpeta nunca basta para entrar en el ecosistema.
* **Compara la máquina con GitHub:** de cada proyecto lee la versión de la copia local y la de la rama por defecto de GitHub, y dice si está instalado, al día, desactualizado o con commits nuevos (una versión igual con commits nuevos se detecta con un `git ls-remote`).
* **Instala y actualiza un proyecto cada vez, tras una confirmación:** el sustituto se construye y se comprueba en un clon de preparación antes de tocar la instalación en uso, y la anterior se guarda como copia que se puede restaurar desde la ventana o con `restore-backup`.
* **Los lotes también se confirman:** *Instalar todo lo que falta* y *Actualizar todo lo desactualizado* son acciones separadas y secuenciales por el mismo camino de seguridad. Nada se actualiza en segundo plano.
* **Un registro de evidencias y una política opcional de commits firmados:** cada intento se escribe en un registro que luego se puede comprobar en busca de líneas editadas, borradas o reordenadas.
* **Perfiles de estación:** un perfil con nombre lista los proyectos con los que trabaja una máquina, y la ventana y los comandos lo siguen.
* **Una ventana en ocho idiomas y una línea de comandos** (`--cli`) que solo necesita la biblioteca estándar, así que también funciona en una máquina sin pantalla.

## 🧩 Papel en EH3D

EH3D-UPDATER es la forma de conseguir la suite y mantenerla al día. ELECTRO-HOBBY-3D-UPDATER, la herramienta por encima de los cuatro ecosistemas, le pasa los proyectos EH3D. Un repositorio EH3D nuevo no necesita nada aquí: aparece en cuanto es público y lleva un manifiesto válido.

## 🏛️ Arquitectura

<p align="center">
  <img src="images/architecture.svg" alt="Arquitectura de EH3D-UPDATER: quién lo usa, qué contiene y de qué depende" width="100%">
</p>

Cómo encajan las partes de este repositorio: quién lo usa, qué contiene y de qué depende. La imagen se dibuja desde `docs/architecture.json` y se comprueba contra el código.

## ✨ Funciones

* **El manifiesto decide:** el descubrimiento, el nombre, la versión, el comando de compilación y las notas salen del propio `eh3d.project.json` del repositorio; un candidato con manifiesto no válido, o con una versión menor que la instalada, se rechaza antes de tocar nada.
* **Una copia sana nunca se reemplaza:** una edición local real o una rama divergente hacen fallar la actualización en voz alta, nunca un reinicio silencioso (`--ff-only` con `--no-build`).
* **Vista previa antes de actualizar:** `update --preview` muestra el commit candidato, su autor, el estado de su firma y los ficheros de compilación y herramientas que cambia, y se detiene.
* **Solo avisar:** `check` lista lo que se podría actualizar, no cambia nada y termina con 10 cuando hay algo (una notificación de escritorio es opcional).
* **Copias de seguridad con límite:** la instalación anterior se guarda como `<nombre>.backup-<8 dígitos hex>`; por defecto se conservan las 2 más recientes y `clean-backups` poda el resto.
* **Amable con la red:** las peticiones se reintentan con espera, un `Retry-After` corto se espera, el listado de repositorios se cachea con `If-None-Match` (un `304` no gasta cuota) y un GitHub inalcanzable vuelve al estado local con un aviso.

## 🔒 Seguridad y protección

| Amenaza | Defensa |
|---|---|
| Una actualización no deseada o por sorpresa | nada se ejecuta en segundo plano: `install` y `update` reciben un nombre de proyecto y una confirmación, y los botones de lote de la ventana son separados, secuenciales y confirmados |
| Un candidato roto que reemplaza una instalación que funcionaba | el candidato se clona, se fusiona sin forzar y se construye y comprueba en un clon de preparación; la carpeta en uso se cambia con dos renombrados solo después, y la anterior se guarda como copia que se puede restaurar |
| Perder trabajo local | una copia con cambios locales o una rama divergente nunca se reemplaza: la actualización falla en voz alta |
| Un repositorio que finge ser parte de la suite | un repositorio entra solo cuando su manifiesto de la raíz valida y declara `EH3D`; se rechaza un candidato con versión menor que la instalada |
| Un commit de origen desconocido | política opcional: con `EH3D_UPDATER_REQUIRE_SIGNED=1` (o el ajuste) y un fichero de firmantes permitidos un commit debe estar firmado; por defecto uno sin firmar se instala con un aviso, y `update --preview` muestra antes el estado de la firma |
| Manipular el registro de lo ocurrido | cada intento de instalación o actualización es una línea de un registro de evidencias que lleva el hash de la línea anterior; `evidence` verifica la cadena y sale con 1 cuando una línea se editó, se borró o se reordenó |
| Filtrar secretos | el registro de evidencias no lleva secretos; GitHub se lee sin token (un `GITHUB_TOKEN` opcional solo sube el límite de peticiones); la herramienta nunca lo imprime |
| Un script de validación que no puede ejecutarse aquí | una instalación que no se puede validar porque falta una herramienta se rechaza salvo que la aceptes (el ajuste `validation_unavailable` o `EH3D_UPDATER_ACCEPT_UNAVAILABLE_VALIDATION=1`) |
| Dos copias a la vez | una instancia que encuentra otra trabajando en el espacio de trabajo se niega a limpiar o restaurar copias de seguridad |

**Lo que no se defiende:** el script de compilación de un proyecto instalado es código de ese proyecto y se ejecuta con tus derechos, así que instala solo lo que te fíes; los commits sin firmar se aceptan por defecto; y la herramienta no ha tenido revisión independiente. Informa de una vulnerabilidad en privado (véase [SECURITY.md](SECURITY.md)).

## 🔌 Interfaces

| Interfaz | Qué es | Dónde |
|---|---|---|
| Ventana | una ventana Qt Quick en ocho idiomas (la opción por defecto; necesita el extra opcional `PySide6`) | `qt_gui.py`, `qml/Main.qml`, [docs/QML_DESKTOP_GUI.md](docs/QML_DESKTOP_GUI.md) |
| Línea de comandos | `eh3d-updater --cli` con `status`, `install`, `update`, `check`, `clean-backups`, `restore-backup` y `evidence`; códigos de salida 0, 1 y 10 (algo se puede actualizar) | [docs/CLI_REFERENCE.md](docs/CLI_REFERENCE.md) |
| GitHub | `GET /users/<propietario>/repos` (en caché con `If-None-Match`) y el manifiesto en bruto de cada candidato; no hace falta token | `github_client.py` |
| El espacio de trabajo | las carpetas junto a la herramienta, `<nombre>.backup-xxxxxxxx` para las instalaciones anteriores y `.eh3d-updater/evidence.jsonl` para el registro de evidencias | `install.py`, `evidence.py` |
| Ajustes | `~/.eh3d_updater_settings.json` (idioma, espacio de trabajo, perfil, copias conservadas, política de firmas) | `settings.py` |

## ⚙️ Configuración

No hay que configurar nada para empezar. Las elecciones que se recuerdan viven en `~/.eh3d_updater_settings.json`, y algunas también se pueden dar como opciones o variables de entorno.

| Ajuste | Por defecto | Rango | Qué hace |
|---|---|---|---|
| `workspace_root` / `--workspace` | la carpeta superior de la herramienta | una carpeta | dónde viven las copias, las copias de seguridad y el registro de evidencias |
| `lang` | el idioma del sistema | en, es, de, fr, it, ja, zh, pt | el idioma de la ventana |
| `profile` / `--profile` | ninguno (todos los proyectos) | un nombre de perfil definido; uno no definido es un error | restringe `status`, `check`, `install` y `update` a los proyectos de un perfil de estación |
| `backups_to_keep` / `clean-backups --keep` | 2 | un número entero de 0 o más | cuántas instalaciones anteriores se conservan por proyecto |
| `require_signed_commits`, `allowed_signers_file` / `EH3D_UPDATER_REQUIRE_SIGNED=1`, `EH3D_UPDATER_ALLOWED_SIGNERS` | desactivado | activado o desactivado | rechazar commits que no firme un firmante permitido |
| `validation_unavailable` / `EH3D_UPDATER_ACCEPT_UNAVAILABLE_VALIDATION=1` | rechazar | rechazar o aceptar | qué hacer cuando la validación de un proyecto no puede ejecutarse porque falta una herramienta |
| `GITHUB_TOKEN` | ninguno | un token de GitHub | solo sube el límite de peticiones del listado; nunca es obligatorio |
| `--no-build` (install, update) | desactivado | activado o desactivado | solo clonar o traer, sin la comprobación de construcción del proyecto (un avance rápido simple) |

Los valores de red son constantes: 10 s por petición, hasta 8 peticiones a la vez, 3 intentos con espera y un `Retry-After` de 60 s como máximo.

## 🚀 Inicio rápido

Necesitas Python 3.10 o posterior; la ventana necesita además PySide6 (`pip install ".[gui]"`).

```bash
./run.sh --cli status          # run.bat --cli status on Windows
./run.sh --cli status --offline --json
./run.sh --cli check           # exit code 10 when something can be updated
./run.sh --cli update EH3D-COMMON --preview
./run.sh --cli install EH3D-CORE-LIBS
```

`run.sh` / `run.bat` sin `--cli` abren la ventana. `install` y `update` piden una confirmación antes de tocar nada, y siempre reciben un nombre de proyecto.

## 🧪 Pruebas

La suite tiene 334 pruebas que pasan (`pytest tests`), y otra que se omite cuando una copia hermana que necesita no está junto a esta. Se ejecutan con un GitHub simulado y repositorios locales, sin red, y cubren el contrato del manifiesto, el descubrimiento, la comparación de versiones y commits, la instalación y la actualización con el clon de preparación y los rechazos (cambios locales, una rama divergente, una versión menor, un manifiesto no válido, una compilación que falla), las copias de seguridad y su restauración, la cadena de evidencias, la política de firmas, los ajustes y perfiles, los mensajes y los ocho idiomas de la ventana, y el puente de Python de la ventana (sin pantalla). Una prueba también comprueba que el árbol de ficheros de cada README lista cada entrada versionada de primer nivel. El CI las ejecuta en Linux y en Windows, más `python tools/ci_validate.py` y una comprobación de sintaxis de cada fichero de Python.

## 🏗️ Compilación y publicación

La versión vive en `pyproject.toml`, en `eh3d.project.json` y en el paquete, y cada versión tiene su entrada en [CHANGELOG.md](CHANGELOG.md). `build.sh` / `build.bat` instalan el paquete y lo comprueban, `build-test.sh` / `build-test.bat` ejecutan además las pruebas y `test.sh` / `test.bat` ejecutan solo las pruebas, cada uno con un panel en vivo; la versión no cambia. Las versiones se publican en GitHub; la herramienta se instala desde este repositorio con pip y no está en PyPI.

## 📂 Estructura del repositorio

<p align="center">
  <img src="images/repository-structure.svg" alt="Estructura del repositorio EH3D-UPDATER" width="100%">
</p>

<details>
<summary>Versión en texto del árbol</summary>

```text
EH3D-UPDATER/
├── src/eh3d_updater/
│   ├── main.py                                  la línea de comandos y el arranque de la ventana
│   ├── github_client.py detect.py               las versiones en GitHub y las copias locales
│   ├── project_manifest.py registry.py          el contrato del manifiesto y su forma en ejecución
│   ├── install.py commits.py                    instalar, actualizar, copias, restaurar; comparar commits
│   ├── evidence.py signature.py                 el registro de evidencias y la política de firmas
│   ├── qt_gui.py qml/                           la ventana Qt Quick y su QML
│   ├── i18n.py messages.py                      los ocho idiomas y los mensajes como códigos
│   └── settings.py profiles.py                  lo que se recuerda y los perfiles de estación
├── tests/                                       sin red: un GitHub simulado y repositorios locales
├── docs/                                        la referencia de la línea de comandos, la guía de la ventana y los datos de las dos imágenes
├── tools/                                       CI, construcción, README, icono e imágenes
├── images/                                      banner y las imágenes de Arquitectura y Estructura del repositorio
├── .github/                                     flujos de CI y de publicación, plantillas de issues y pull requests
├── build.sh build.bat                           instala y comprueba el paquete con un panel en vivo
├── build-test.sh build-test.bat                 lo mismo, y luego las pruebas
├── run.sh run.bat                               abre la ventana, o la línea de comandos con --cli
├── bump*.py                                     los scripts que suben la versión
├── eh3d.project.json                            manifiesto: versión, rol, madurez y comando de compilación
├── run-gui.vbs                                  abre la ventana sin consola en Windows
├── pyproject.toml                               el paquete de Python y sus extras
├── CHANGELOG.md                                 qué cambió en cada versión
├── SECURITY.md SUPPORT.md                       cómo informar de una vulnerabilidad y dónde preguntar
├── CONTRIBUTING.md CODE_OF_CONDUCT.md LICENSE   cómo contribuir, el código de conducta y la licencia
└── LICENSE.md                                   el texto de la licencia en Markdown
```

</details>

## 🗺️ Hoja de ruta y límites conocidos

**Límites conocidos hoy**

* Nunca ha instalado ni actualizado un proyecto desde el GitHub real: todo se prueba con un GitHub simulado y repositorios locales, y solo existen unos pocos repositorios EH3D para instalar.
* El traspaso desde ELECTRO-HOBBY-3D-UPDATER no se ha ejecutado contra una copia real.
* Por defecto no se exige que los commits estén firmados; la política es opcional.
* El script de compilación de un proyecto instalado se ejecuta con tus derechos.
* La herramienta no ha tenido revisión independiente y no está en PyPI.

**Siguiente**

* Instalar y actualizar un proyecto real de extremo a extremo con el GitHub real y anotar lo que salga.
* Ejecutar el traspaso desde ELECTRO-HOBBY-3D-UPDATER en una copia real.
* Decidir si los commits firmados pasan a ser el valor por defecto de la suite.

## 🌍 Idiomas

El README y los textos existen en inglés, español, francés, italiano, alemán, chino, japonés y portugués de Portugal.

## 🔗 Proyectos relacionados

* [EH3D-COMMON](https://github.com/JuanenRac/EH3D-COMMON): el contenedor de proyecto y los tipos de máquina; se puede instalar con esta herramienta
* [EH3D-CORE-LIBS](https://github.com/JuanenRac/EH3D-CORE-LIBS): los lectores de Gerber, Excellon y G-code; se puede instalar con esta herramienta
* [ELECTRO-HOBBY-3D-UPDATER](https://github.com/JuanenRac/ELECTRO-HOBBY-3D-UPDATER): el actualizador por encima de los cuatro ecosistemas, que reparte a este
* [URTC-UPDATER](https://github.com/JuanenRac/URTC-UPDATER): el actualizador de URTC, del que esta herramienta toma su diseño

## 📚 Documentación

* [Referencia de la línea de comandos](docs/CLI_REFERENCE.md): cada comando, opción y código de salida.
* [La ventana de escritorio](docs/QML_DESKTOP_GUI.md): cómo la ventana Qt Quick se apoya en los mismos servicios que la línea de comandos.
* [Registro de cambios](CHANGELOG.md)

## 🤝 Contribuir y comunidad

* Antes de una pull request ejecuta `PYTHONPATH=src python -m pytest tests -q` y `python -I tools/ci_validate.py`: todo debe pasar. Consulta [CONTRIBUTING.md](CONTRIBUTING.md) y el [código de conducta](CODE_OF_CONDUCT.md).
* El README existe en ocho idiomas: un cambio en el texto se hace en los ocho archivos, y las dos imágenes se dibujan a partir de `docs/architecture.json` y `docs/structure.json` con `tools/make_architecture.py` y `tools/make_structure.py`.
* Un cambio en un texto de cara al usuario va a los ocho idiomas de `i18n.py`; una decisión de seguridad se toma en los servicios de Python, nunca en el QML.
* Informa de una vulnerabilidad en privado: [SECURITY.md](SECURITY.md). Preguntas, ideas e informes: electrohobby3d@gmail.com ([SUPPORT.md](SUPPORT.md)).

## 👤 AUTOR

**JuanenRac (Electro Hobby 3D)** · electrohobby3d@gmail.com

## 📜 LICENCIA

Software: GPL-3.0-or-later. Véase [LICENSE](LICENSE). Los diseños de hardware de la suite usan CERN OHL-S.
