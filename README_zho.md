<p align="center">
  <img src="images/EH3D_UPDATER_BANNER.svg" alt="EH3D-UPDATER banner" width="100%">
</p>

# 🛠️ EH3D-UPDATER

<p align="center"><a href="README.md">🇺🇸 English</a> | <a href="README_spa.md">🇪🇸 Español</a> | <a href="README_fra.md">🇫🇷 Français</a> | <a href="README_ita.md">🇮🇹 Italiano</a> | <a href="README_deu.md">🇩🇪 Deutsch</a> | 🇨🇳 <b>中文</b> | <a href="README_jpn.md">🇯🇵 日本語</a> | <a href="README_por.md">🇵🇹 Português</a></p>

### 在你的电脑上检测、安装和更新 EH3D Fabrication Suite 的仓库：不会自行发生任何事，正在使用的安装只有在其替代版本构建并检查通过之后才会被替换

<p align="center">
  <img src="https://img.shields.io/badge/License-GPL%203.0--or--later-blue.svg" alt="GPL 3.0 or later">
  <img src="https://img.shields.io/badge/Stack-Python%203.10%2B-3776AB.svg" alt="Python">
  <img src="https://img.shields.io/badge/Languages-8-00E5FF.svg" alt="Languages">
  <img src="https://img.shields.io/badge/Version-0.0.2-0f6cbd.svg" alt="Version">
  <img src="https://img.shields.io/badge/Maturity-scaffolding-FFB020.svg" alt="Maturity">
</p>

---

**诚实性核对 - 今天真正能运行的内容：** 一个命令行和一个 Qt Quick 窗口，通过 `eh3d.project.json` 清单找到 EH3D 仓库，把每个本地检出与 GitHub 比较，并在确认后一次安装或更新一个。更新先在暂存克隆中克隆、不强制合并、构建并检查，之前的安装作为备份保留。它是家族其他生态系统的更新器换上 EH3D 名称的版本，有 334 个测试在计算机上用假的 GitHub 和本地仓库运行。它尚未用于真实工作，也从未从真正的 GitHub 安装或更新过项目。

---

> **安全（safety）与信息安全现状：** 它会替换你机器上的文件并运行所安装内容的构建检查，所以只在明确确认之后才这样做，绝不会覆盖有本地修改的检出，并把每次尝试记录在不含机密的证据日志中。只有当你选择该策略时才会检查提交的签名；它不是安全系统（safety），也不控制任何机床。

## 📋 速览

| | |
|---|---|
| 版本 | `0.0.2` |
| 成熟度 | 脚手架 |
| 测试 | 334 |
| 技术栈 | Python 3.10+ / PySide6 / Qt Quick |
| 真实硬件 | 不适用：它运行在使用者的电脑上 |

**跳转到：** [概述](#-概述) · [架构](#-架构) · [快速开始](#-快速开始) · [测试](#-测试) · [结构](#-仓库结构) · [相关项目](#-相关项目)

## 🚦 项目状态

每一行是本仓库的一个部分，灯号表示它今天做到了哪一步。内容依据仓库能够展示的证据（测试、构建、运行），而不是计划。

🟢 已完成并验证 · 🟡 可用，有已知限制 · 🟠 部分完成或尚未验证 · 🔴 未完成或不可用

| 领域 | 状态 | 在这里的含义 |
|---|---|---|
| 软件 | 🟡 | 命令行和 Qt Quick 窗口通过清单找到 EH3D 仓库，与 GitHub 比较，并用暂存克隆和之前安装的备份一次安装或更新一个。 |
| 测试 | 🟡 | 334 个测试通过（`pytest`），使用假的 GitHub 和本地仓库（不联网）；当缺少它所需的相邻检出时，另有一个测试被跳过。 |
| 发现 | 🟡 | 公开仓库只是候选：根目录的 `eh3d.project.json` 通过校验并声明 `EH3D` 的项目才会加入生态系统；已针对假的列表测试，未针对真实 GitHub 运行。 |
| 真实使用 | 🟠 | 尚未用于真实工作，也从未从真正的 GitHub 安装或更新过项目；目前可安装的 EH3D 仓库只有少数几个。 |
| 界面 | 🟡 | 窗口支持八种语言，其 Python 桥接有测试覆盖；命令行只需要标准库。 |
| 安全 | 🟡 | 没有确认不会更改任何东西，也不会覆盖有本地修改的检出，合并从不强制，证据日志会显示被编辑或重排的行；签名提交策略是可选的，也未经独立审查。 |
| 集成 | 🟡 | ELECTRO-HOBBY-3D-UPDATER 把 EH3D 项目交给它；这一交接尚未在真实检出上运行过。 |
| 真实硬件 | 🟡 | 不适用：它运行在使用者的电脑上。 |
| 文档 | 🟡 | 八种语言的 README、命令行参考和窗口指南。 |

## 🎯 概述

* **通过清单找到项目：** 所有者在 GitHub 上的公开仓库只是候选列表；根目录的 `eh3d.project.json` 通过校验并声明生态系统 `EH3D` 的才是项目，所以新仓库只要有清单就会出现，这个工具里没有任何项目列表。在本地，光有文件夹名永远不足以加入生态系统。
* **把机器与 GitHub 比较：** 对每个项目读取本地检出的版本和 GitHub 默认分支上的版本，并说明它是已安装、最新、过期还是有新提交（版本相同但有新提交，用一次 `git ls-remote` 就能发现）。
* **确认后一次安装或更新一个项目：** 替代版本先在暂存克隆中构建并检查，然后才动正在使用的安装，之前的安装作为备份保留，可从窗口或用 `restore-backup` 恢复。
* **批量操作同样要确认：** “安装所有缺失项”和“更新所有过期项”是独立的、依次执行的操作，走同一条安全路径。后台不会更新任何东西。
* **证据日志和可选的签名提交策略：** 每次尝试都写入日志，之后可检查其中是否有被编辑、删除或重排的行。
* **工位配置：** 命名的配置列出一台机器所处理的项目，窗口和命令都遵循它。
* **八种语言的窗口和只需标准库的命令行**（`--cli`），因此在没有屏幕的机器上也能工作。

## 🧩 在 EH3D 中的角色

EH3D-UPDATER 是获取套件并保持最新的途径。位于四个生态系统之上的 ELECTRO-HOBBY-3D-UPDATER 把 EH3D 项目交给它。新的 EH3D 仓库在这里不需要任何改动：只要公开并带有有效的清单，它就会出现。

## 🏛️ 架构

<p align="center">
  <img src="images/architecture.svg" alt="EH3D-UPDATER 的架构：谁在使用、包含什么、依赖什么" width="100%">
</p>

本仓库各部分如何协作：谁在使用它、它包含什么、它依赖什么。图片由 `docs/architecture.json` 绘制，并与代码核对。

## ✨ 功能

* **清单说了算：** 发现、名称、版本、构建命令和说明都来自仓库自己的 `eh3d.project.json`；清单无效或版本低于已安装版本的候选，会在动任何东西之前被拒绝。
* **健康的检出从不被替换：** 真实的本地修改或分叉的分支会让更新明确失败，绝不会悄悄重置（`--no-build` 时使用 `--ff-only`）。
* **更新前预览：** `update --preview` 显示候选提交、其作者、签名状态以及它更改的构建和工具文件，然后停止。
* **仅通知：** `check` 列出可以更新的内容，不更改任何东西，有可更新项时以 10 退出（桌面通知是可选的）。
* **有上限的备份：** 之前的安装保留为 `<名称>.backup-<8 位十六进制>`；默认保留最新的 2 个，`clean-backups` 清理其余的。
* **对网络友好：** 请求带退避重试，较短的 `Retry-After` 会等待，仓库列表用 `If-None-Match` 缓存（`304` 不消耗配额），GitHub 无法访问时会带警告退回到本地状态。

## 🔒 安全与防护

| 威胁 | 防御 |
|---|---|
| 不想要的或突然的更新 | 后台不运行任何东西：`install` 和 `update` 需要一个项目名称和一次确认，窗口的批量按钮是分开的、依次执行并需确认 |
| 损坏的候选替换了正常工作的安装 | 候选先在暂存克隆中克隆、不强制合并、构建并检查；之后才用两次重命名替换正在使用的文件夹，之前的安装作为可恢复的备份保留 |
| 丢失本地工作 | 有本地修改的检出或分叉的分支绝不会被替换：更新会明确失败 |
| 冒充套件一部分的仓库 | 只有根目录清单通过校验并声明 `EH3D` 的仓库才会加入；版本低于已安装版本的候选会被拒绝 |
| 来源不明的提交 | 可选策略：设置 `EH3D_UPDATER_REQUIRE_SIGNED=1`（或相应设置）并提供允许签名者文件后，提交必须已签名；默认情况下未签名的提交会带警告安装，`update --preview` 会先显示签名状态 |
| 篡改发生过什么的记录 | 每次安装或更新尝试都是证据日志的一行，带有前一行的哈希；`evidence` 会验证这条链，当有行被编辑、删除或重排时以 1 退出 |
| 泄露机密 | 证据日志不含机密；读取 GitHub 不需要令牌（可选的 `GITHUB_TOKEN` 只会提高速率限制），工具从不打印它 |
| 在这里无法运行的验证脚本 | 因缺少工具而无法验证的安装会被拒绝，除非你接受（设置 `validation_unavailable` 或 `EH3D_UPDATER_ACCEPT_UNAVAILABLE_VALIDATION=1`） |
| 同时有两个实例 | 发现另一个实例正在工作区中运行的实例，会拒绝清理或恢复备份 |

**没有防御的内容：** 已安装项目的构建脚本是该项目自己的代码，以你的权限运行，所以只安装你信任的东西；默认接受未签名的提交；该工具也未经独立审查。请私下报告漏洞（见 [SECURITY.md](SECURITY.md)）。

## 🔌 接口

| 接口 | 内容 | 位置 |
|---|---|---|
| 窗口 | 八种语言的 Qt Quick 窗口（默认；需要可选的 `PySide6` 附加项） | `qt_gui.py`、`qml/Main.qml`、[docs/QML_DESKTOP_GUI.md](docs/QML_DESKTOP_GUI.md) |
| 命令行 | `eh3d-updater --cli`，含 `status`、`install`、`update`、`check`、`clean-backups`、`restore-backup` 和 `evidence`；退出码 0、1 和 10（有可更新项） | [docs/CLI_REFERENCE.md](docs/CLI_REFERENCE.md) |
| GitHub | `GET /users/<所有者>/repos`（用 `If-None-Match` 缓存）和每个候选的原始清单；不需要令牌 | `github_client.py` |
| 工作区 | 工具旁边的文件夹、用于之前安装的 `<名称>.backup-xxxxxxxx`，以及用于证据日志的 `.eh3d-updater/evidence.jsonl` | `install.py`、`evidence.py` |
| 设置 | `~/.eh3d_updater_settings.json`（语言、工作区、配置、保留的备份、签名策略） | `settings.py` |

## ⚙️ 配置

开始使用不需要配置任何东西。被记住的选择保存在 `~/.eh3d_updater_settings.json` 中，其中一些也可以用选项或环境变量给出。

| 设置 | 默认值 | 范围 | 作用 |
|---|---|---|---|
| `workspace_root` / `--workspace` | 工具所在的上级文件夹 | 一个文件夹 | 检出、备份和证据日志所在的位置 |
| `lang` | 系统语言 | en、es、de、fr、it、ja、zh、pt | 窗口的语言 |
| `profile` / `--profile` | 无（所有项目） | 已定义的配置名称；未定义的名称是错误 | 把 `status`、`check`、`install` 和 `update` 限制在某个工位配置的项目内 |
| `backups_to_keep` / `clean-backups --keep` | 2 | 0 或更大的整数 | 每个项目保留多少个之前的安装 |
| `require_signed_commits`、`allowed_signers_file` / `EH3D_UPDATER_REQUIRE_SIGNED=1`、`EH3D_UPDATER_ALLOWED_SIGNERS` | 关 | 开或关 | 拒绝未由允许的签名者签名的提交 |
| `validation_unavailable` / `EH3D_UPDATER_ACCEPT_UNAVAILABLE_VALIDATION=1` | 拒绝 | 拒绝或接受 | 项目的验证因缺少工具而无法运行时怎么办 |
| `GITHUB_TOKEN` | 无 | GitHub 令牌 | 只会提高列表的速率限制；从不是必需的 |
| `--no-build`（install、update） | 关 | 开或关 | 只克隆或拉取，不运行项目自己的构建检查（简单的快进） |

网络数值是常量：每个请求 10 秒，同时最多 8 个请求，带退避重试 3 次，`Retry-After` 最多 60 秒。

## 🚀 快速开始

需要 Python 3.10 或更高版本；窗口还需要 PySide6（`pip install ".[gui]"`）。

```bash
./run.sh --cli status          # run.bat --cli status on Windows
./run.sh --cli status --offline --json
./run.sh --cli check           # exit code 10 when something can be updated
./run.sh --cli update EH3D-COMMON --preview
./run.sh --cli install EH3D-CORE-LIBS
```

不带 `--cli` 的 `run.sh` / `run.bat` 会打开窗口。`install` 和 `update` 在动任何东西之前都会要求确认，并且始终只接受一个项目名称。

## 🧪 测试

测试共 334 个通过（`pytest tests`），另有 1 个在所需的相邻检出不在本仓库旁边时被跳过。它们使用假的 GitHub 和本地仓库、不联网运行，覆盖清单约定、发现、版本和提交比较、带暂存克隆的安装与更新及各种拒绝情形（本地修改、分叉的分支、较低的版本、无效清单、构建失败）、备份与恢复、证据链、签名策略、设置与配置、消息和窗口的八种语言，以及窗口的 Python 桥接（离屏）。还有一个测试检查每个 README 的文件树是否列出了每一项受版本控制的第一层条目。CI 在 Linux 和 Windows 上运行它们，另外运行 `python tools/ci_validate.py` 和对每个 Python 文件的语法检查。

## 🏗️ 构建与发布

版本号位于 `pyproject.toml`、`eh3d.project.json` 和包中，每个版本在 [CHANGELOG.md](CHANGELOG.md) 中都有条目。`build.sh` / `build.bat` 安装并检查包，`build-test.sh` / `build-test.bat` 还会运行测试，`test.sh` / `test.bat` 只运行测试，都在实时面板中进行；版本不会改变。版本发布在 GitHub 上；该工具通过 pip 从本仓库安装，不在 PyPI 上。

## 📂 仓库结构

<p align="center">
  <img src="images/repository-structure.svg" alt="EH3D-UPDATER 的仓库结构" width="100%">
</p>

<details>
<summary>目录树的文本版</summary>

```text
EH3D-UPDATER/
├── src/eh3d_updater/
│   ├── main.py                                  命令行和窗口的启动
│   ├── github_client.py detect.py               GitHub 上的版本和本地检出
│   ├── project_manifest.py registry.py          清单约定及其运行时形式
│   ├── install.py commits.py                    安装、更新、备份、提交比较
│   ├── evidence.py signature.py                 证据日志和签名策略
│   ├── qt_gui.py qml/                           Qt Quick 窗口及其 QML
│   ├── i18n.py messages.py                      八种语言和代码化的消息
│   └── settings.py profiles.py                  被记住的内容和工位配置
├── tests/                                       不联网：假的 GitHub 和本地仓库
├── docs/                                        命令行参考、窗口指南和两张图的数据
├── tools/                                       CI、构建、README 检查、图标和绘图
├── images/                                      横幅图以及架构和仓库结构图片
├── .github/                                     CI 与发布工作流、Issue 和 PR 模板
├── build.sh build.bat                           在实时面板中安装并检查包
├── build-test.sh build-test.bat                 同样的步骤，然后运行测试
├── run.sh run.bat                               启动窗口，加 --cli 则为命令行
├── bump*.py                                     提升版本的脚本
├── eh3d.project.json                            清单：版本、角色、成熟度和构建命令
├── run-gui.vbs                                  在 Windows 上不带控制台启动窗口
├── pyproject.toml                               Python 包及其附加项
├── CHANGELOG.md                                 每个版本的变更
├── SECURITY.md SUPPORT.md                       如何报告漏洞及在哪里提问
├── CONTRIBUTING.md CODE_OF_CONDUCT.md LICENSE   参与贡献、行为准则和许可证
└── LICENSE.md                                   Markdown 格式的许可证文本
```

</details>

## 🗺️ 路线图与已知限制

**目前已知的限制**

* 它从未从真正的 GitHub 安装或更新过项目：一切都用假的 GitHub 和本地仓库测试，目前可安装的 EH3D 仓库只有少数几个。
* 从 ELECTRO-HOBBY-3D-UPDATER 的交接尚未在真实检出上运行过。
* 默认不要求提交必须签名；该策略是可选的。
* 已安装项目的构建脚本以你的权限运行。
* 该工具未经独立审查，也不在 PyPI 上。

**下一步**

* 用真正的 GitHub 把一个真实项目从头到尾安装并更新一遍，记录出现的问题。
* 在真实检出上运行来自 ELECTRO-HOBBY-3D-UPDATER 的交接。
* 决定签名提交是否成为套件的默认要求。

## 🌍 语言

README 和文本提供英语、西班牙语、法语、意大利语、德语、汉语、日语和欧洲葡萄牙语版本。

## 🔗 相关项目

* [EH3D-COMMON](https://github.com/JuanenRac/EH3D-COMMON)：项目容器和机床类型；可用本工具安装
* [EH3D-CORE-LIBS](https://github.com/JuanenRac/EH3D-CORE-LIBS)：Gerber、Excellon 和 G 代码的读取库；可用本工具安装
* [ELECTRO-HOBBY-3D-UPDATER](https://github.com/JuanenRac/ELECTRO-HOBBY-3D-UPDATER)：位于四个生态系统之上的更新器，会把工作分派给本工具
* [URTC-UPDATER](https://github.com/JuanenRac/URTC-UPDATER)：URTC 的更新器，本工具的设计取自它

## 📚 文档

* [命令行参考](docs/CLI_REFERENCE.md)：每个命令、选项和退出码。
* [桌面窗口](docs/QML_DESKTOP_GUI.md)：Qt Quick 窗口如何建立在与命令行相同的服务之上。
* [变更日志](CHANGELOG.md)

## 🤝 参与贡献与社区

* 提交 pull request 之前请运行 `PYTHONPATH=src python -m pytest tests -q` 和 `python -I tools/ci_validate.py`，全部通过。参见 [CONTRIBUTING.md](CONTRIBUTING.md) 和[行为准则](CODE_OF_CONDUCT.md)。
* README 有八种语言：修改文字时要同步修改全部八个文件，两张图片由 `tools/make_architecture.py` 和 `tools/make_structure.py` 根据 `docs/architecture.json` 和 `docs/structure.json` 绘制。
* 面向用户的文本改动要写进 `i18n.py` 的八种语言；安全决策在 Python 服务中做出，绝不在 QML 中。
* 请私下报告漏洞：[SECURITY.md](SECURITY.md)。问题、想法和报告：electrohobby3d@gmail.com（[SUPPORT.md](SUPPORT.md)）。

## 👤 作者

**JuanenRac (Electro Hobby 3D)** · electrohobby3d@gmail.com

## 📜 许可证

软件：GPL-3.0-or-later。见 [LICENSE](LICENSE)。套件的硬件设计使用 CERN OHL-S。
