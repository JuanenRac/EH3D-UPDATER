<p align="center">
  <img src="images/EH3D_UPDATER_BANNER.svg" alt="EH3D-UPDATER banner" width="100%">
</p>

# 🛠️ EH3D-UPDATER

<p align="center"><a href="README.md">🇺🇸 English</a> | <a href="README_spa.md">🇪🇸 Español</a> | <a href="README_fra.md">🇫🇷 Français</a> | <a href="README_ita.md">🇮🇹 Italiano</a> | <a href="README_deu.md">🇩🇪 Deutsch</a> | 🇨🇳 <b>中文</b> | <a href="README_jpn.md">🇯🇵 日本語</a> | <a href="README_por.md">🇵🇹 Português</a></p>

### 在你的电脑上检测、安装和更新 EH3D Fabrication Suite 的仓库：不会自行发生任何事，正在使用的安装只有在替换件构建并检查通过之后才会被替换

<p align="center">
  <img src="https://img.shields.io/badge/License-GPL%203.0--or--later-blue.svg" alt="GPL 3.0 or later">
  <img src="https://img.shields.io/badge/Language-Python%203.10%2B-blue.svg" alt="Python">
  <img src="https://img.shields.io/badge/Languages-8-00E5FF.svg" alt="Languages">
  <img src="https://img.shields.io/badge/Version-0.0.1-0f6cbd.svg" alt="Version">
  <img src="https://img.shields.io/badge/Maturity-scaffolding-FFB020.svg" alt="Maturity">
</p>

---

**诚实性检查 - 今天真正能运行的部分：** 一个命令行和一个 Qt Quick 窗口，通过 `eh3d.project.json` 清单找到 EH3D 仓库，把每个本地副本与 GitHub 比较，并在确认后一次安装或更新一个项目。更新会先克隆、非强制合并，并在预备副本中构建和检查，之前的安装会作为备份保留。它是该系列其他生态系统的更新器换上 EH3D 名称，有 317 个测试，在带有假 GitHub 和本地仓库的电脑上运行。它还没有用于真实工作，目前只有 EH3D-COMMON 和 EH3D-CORE-LIBS 可供安装。

---

> **安全（safety）与信息安全状态：** 它会替换你机器上的文件，并运行所安装内容的构建检查，因此只在明确确认后才这样做，绝不会覆盖带有本地修改的副本，并把每次尝试记录到不含机密的证据日志中。只有你选择该策略时，它才会检查提交的签名；它不是安全系统，也不控制任何机器。

## 📋 概览

| | |
|---|---|
| 版本 | `0.0.1` |
| 成熟度 | 脚手架 |
| 测试 | 317 |
| 技术栈 | Python 3.10+ / PySide6 / Qt Quick |
| 真实硬件 | 不适用：它运行在使用者的电脑上 |

## 🚦 项目状态

每一行是本仓库的一个部分，灯号表示它今天做到了哪一步。内容依据仓库能够展示的证据（测试、构建、运行），而不是计划。

🟢 已完成并验证 · 🟡 可用，有已知限制 · 🟠 部分完成或尚未验证 · 🔴 未完成或不可用

| 领域 | 状态 | 在这里的含义 |
|---|---|---|
| 软件 | 🟡 | 命令行和 Qt Quick 窗口通过清单找到 EH3D 仓库，与 GitHub 对比，并一次一个地安装或更新，先用暂存克隆验证，并保留上一次安装的备份。 |
| 测试 | 🟢 | 317 项测试通过，使用模拟的 GitHub 和本地仓库（不联网）。 |
| 实际使用 | 🟠 | 尚未用于实际工作，也从未从真实的 GitHub 安装或更新过项目；可安装的 EH3D 仓库只有少数几个。 |
| 界面 | 🟡 | 窗口支持八种语言，其 Python 桥接层有测试覆盖；命令行只需要标准库。 |
| 安全性 | 🟡 | 没有确认不会做任何更改，有本地改动的检出也不会被覆盖；合并从不强制，证据日志能发现被编辑或重排的行；签名提交策略是可选的，也没有经过独立审查。 |
| 集成 | 🟡 | ELECTRO-HOBBY-3D-UPDATER 会把 EH3D 项目交给它；这一交接尚未在真实检出上运行过。 |
| 真实硬件 | 🟢 | 不适用：它运行在使用者的电脑上。 |
| 文档 | 🟢 | 八种语言的 README、命令行参考和窗口使用指南。 |

## 🎯 概述

* **通过清单找到项目：** 每个带有生态系统为 `EH3D` 的 `eh3d.project.json` 的公开仓库都是一个项目，因此新仓库只要有清单就会出现，本工具里没有任何项目列表。
* **把本机与 GitHub 比较：** 对每个项目读取本地副本的版本和 GitHub 默认分支的版本，并说明它是已安装、最新、已过时，还是有新提交。
* **确认后一次安装或更新一个项目：** 替换件先在预备副本中构建和检查，然后才会动正在使用的安装，之前的安装作为备份保留，可从窗口恢复。
* **批量操作同样需要确认：** *安装所有缺失项* 和 *更新所有过时项* 是单独的、按顺序执行的操作，走同一条安全路径。不会在后台更新任何东西。
* **证据日志和可选的签名提交策略：** 每次尝试都写入日志，之后可检查其中是否有被编辑、删除或重新排序的行。
* **八种语言的窗口和命令行**（`--cli`），命令行只需要标准库，因此也能在没有屏幕的机器上运行。

## 🧩 在 EH3D 中的角色

EH3D-UPDATER 是获取套件并保持其最新的方式。位于四个生态系统之上的 ELECTRO-HOBBY-3D-UPDATER 会把 EH3D 项目交给它处理。

## 📂 仓库结构

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

## 🛠️ 构建与运行

需要 Python 3.10 或更新版本；窗口还需要 PySide6（`pip install ".[gui]"`）。

```bash
PYTHONPATH=src python -m pytest tests -q
python -I tools/ci_validate.py
./run.sh --cli status        # run.bat --cli status on Windows
```

## 🔗 相关项目

* [EH3D-COMMON](https://github.com/JuanenRac/EH3D-COMMON): 项目容器和机器类型；可用本工具安装
* [EH3D-CORE-LIBS](https://github.com/JuanenRac/EH3D-CORE-LIBS): Gerber、Excellon 和 G-code 的读取库；可用本工具安装
* [ELECTRO-HOBBY-3D-UPDATER](https://github.com/JuanenRac/ELECTRO-HOBBY-3D-UPDATER): 位于四个生态系统之上的更新器，会委托给本工具
* [URTC-UPDATER](https://github.com/JuanenRac/URTC-UPDATER): URTC 的更新器，本工具的设计来自它

## 📚 文档与社区

* [命令行参考](docs/CLI_REFERENCE.md)和[桌面窗口](docs/QML_DESKTOP_GUI.md)。
* [贡献指南](CONTRIBUTING.md)、[安全政策](SECURITY.md)、[支持](SUPPORT.md)和[行为准则](CODE_OF_CONDUCT.md)。

## 👤 作者

**JuanenRac (Electro Hobby 3D)** · electrohobby3d@gmail.com

## 📜 许可证

软件：GPL-3.0-or-later。参见 [LICENSE](LICENSE)。
