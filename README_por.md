<p align="center">
  <img src="images/EH3D_UPDATER_BANNER.svg" alt="EH3D-UPDATER banner" width="100%">
</p>

# 🛠️ EH3D-UPDATER

<p align="center"><a href="README.md">🇺🇸 English</a> | <a href="README_spa.md">🇪🇸 Español</a> | <a href="README_fra.md">🇫🇷 Français</a> | <a href="README_ita.md">🇮🇹 Italiano</a> | <a href="README_deu.md">🇩🇪 Deutsch</a> | <a href="README_zho.md">🇨🇳 中文</a> | <a href="README_jpn.md">🇯🇵 日本語</a> | 🇵🇹 <b>Português</b></p>

### Deteta, instala e atualiza no seu PC os repositórios da EH3D Fabrication Suite: nada acontece sozinho, e uma instalação em uso só é substituída depois de a sua substituta ter sido construída e verificada

<p align="center">
  <img src="https://img.shields.io/badge/License-GPL%203.0--or--later-blue.svg" alt="GPL 3.0 or later">
  <img src="https://img.shields.io/badge/Language-Python%203.10%2B-blue.svg" alt="Python">
  <img src="https://img.shields.io/badge/Languages-8-00E5FF.svg" alt="Languages">
  <img src="https://img.shields.io/badge/Version-0.0.1-0f6cbd.svg" alt="Version">
  <img src="https://img.shields.io/badge/Maturity-scaffolding-FFB020.svg" alt="Maturity">
</p>

---

**Verificação de honestidade - o que funciona hoje:** uma linha de comandos e uma janela Qt Quick que encontram os repositórios EH3D pelos seus manifestos `eh3d.project.json`, comparam cada cópia local com o GitHub e instalam ou atualizam um projeto de cada vez depois de uma confirmação. A atualização é clonada, fundida sem forçar e construída e verificada primeiro numa cópia de preparação, e a instalação anterior é guardada como cópia de segurança. É o atualizador dos outros ecossistemas da família com os nomes do EH3D, com 317 testes que correm num computador com um GitHub falso e repositórios locais. Ainda não foi usado para trabalho real, e só existem para instalar o EH3D-COMMON e o EH3D-CORE-LIBS.

---

> **Estado de segurança (safety) e de segurança informática:** substitui ficheiros da sua máquina e executa a verificação de construção do que instala, por isso só o faz depois de uma confirmação explícita, nunca sobre uma cópia com alterações locais, e regista cada tentativa num registo de evidências sem segredos. Só verifica a assinatura de um commit se escolher essa política; não é um sistema de segurança funcional e não controla nenhuma máquina.

## 📋 Num relance

| | |
|---|---|
| Versão | `0.0.1` |
| Maturidade | Andaime |
| Testes | 317 |
| Pilha tecnológica | Python 3.10+ / PySide6 / Qt Quick |
| Em hardware real | Não aplicável: corre no PC de quem o usa |

## 🎯 Visão geral

* **Encontra os projetos pelos seus manifestos:** todo o repositório público com um `eh3d.project.json` do ecossistema `EH3D` é um projeto, por isso um repositório novo aparece por ter um manifesto e nada nesta ferramenta enumera os projetos.
* **Compara a máquina com o GitHub:** de cada projeto lê a versão da cópia local e a do ramo predefinido do GitHub, e diz se está instalado, atualizado, desatualizado ou com commits novos.
* **Instala e atualiza um projeto de cada vez, depois de uma confirmação:** a substituta é construída e verificada numa cópia de preparação antes de tocar na instalação em uso, e a anterior é guardada como cópia de segurança que se pode restaurar a partir da janela.
* **Os lotes também são confirmados:** *Instalar tudo o que falta* e *Atualizar tudo o que está desatualizado* são ações separadas e sequenciais pelo mesmo caminho de segurança. Nada se atualiza em segundo plano.
* **Um registo de evidências e uma política opcional de commits assinados:** cada tentativa fica escrita num registo que se pode verificar depois quanto a linhas editadas, removidas ou reordenadas.
* **Uma janela em oito idiomas e uma linha de comandos** (`--cli`) que só precisa da biblioteca padrão, por isso também funciona numa máquina sem ecrã.

## 🧩 Papel no EH3D

O EH3D-UPDATER é a forma de obter a suite e de a manter atualizada. O ELECTRO-HOBBY-3D-UPDATER, a ferramenta acima dos quatro ecossistemas, entrega-lhe os projetos EH3D.

## 📂 Estrutura do repositório

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

## 🛠️ COMPILAR E EXECUTAR

Precisa de Python 3.10 ou mais recente; a janela precisa também de PySide6 (`pip install ".[gui]"`).

```bash
PYTHONPATH=src python -m pytest tests -q
python -I tools/ci_validate.py
./run.sh --cli status        # run.bat --cli status on Windows
```

## 🔗 Projetos relacionados

* [EH3D-COMMON](https://github.com/JuanenRac/EH3D-COMMON): o contentor de projeto e os tipos de máquina; instala-se com esta ferramenta
* [EH3D-CORE-LIBS](https://github.com/JuanenRac/EH3D-CORE-LIBS): os leitores de Gerber, Excellon e G-code; instala-se com esta ferramenta
* [ELECTRO-HOBBY-3D-UPDATER](https://github.com/JuanenRac/ELECTRO-HOBBY-3D-UPDATER): o atualizador acima dos quatro ecossistemas, que delega neste
* [URTC-UPDATER](https://github.com/JuanenRac/URTC-UPDATER): o atualizador do URTC, de que esta ferramenta toma o desenho

## 📚 Documentação e comunidade

* [Referência da linha de comandos](docs/CLI_REFERENCE.md) e [a janela de ambiente de trabalho](docs/QML_DESKTOP_GUI.md).
* [Como contribuir](CONTRIBUTING.md), [política de segurança](SECURITY.md), [suporte](SUPPORT.md) e [código de conduta](CODE_OF_CONDUCT.md).

## 👤 AUTOR

**JuanenRac (Electro Hobby 3D)** · electrohobby3d@gmail.com

## 📜 LICENÇA

Software: GPL-3.0-or-later. Consulte [LICENSE](LICENSE).
