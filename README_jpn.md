<p align="center">
  <img src="images/EH3D_UPDATER_BANNER.svg" alt="EH3D-UPDATER banner" width="100%">
</p>

# 🛠️ EH3D-UPDATER

<p align="center"><a href="README.md">🇺🇸 English</a> | <a href="README_spa.md">🇪🇸 Español</a> | <a href="README_fra.md">🇫🇷 Français</a> | <a href="README_ita.md">🇮🇹 Italiano</a> | <a href="README_deu.md">🇩🇪 Deutsch</a> | <a href="README_zho.md">🇨🇳 中文</a> | 🇯🇵 <b>日本語</b> | <a href="README_por.md">🇵🇹 Português</a></p>

### EH3D Fabrication Suite のリポジトリを PC 上で検出、インストール、更新します：勝手には何も起きず、使用中のインストールは代わりのものがビルドされ検証された後にだけ置き換えられます

<p align="center">
  <img src="https://img.shields.io/badge/License-GPL%203.0--or--later-blue.svg" alt="GPL 3.0 or later">
  <img src="https://img.shields.io/badge/Language-Python%203.10%2B-blue.svg" alt="Python">
  <img src="https://img.shields.io/badge/Languages-8-00E5FF.svg" alt="Languages">
  <img src="https://img.shields.io/badge/Version-0.0.1-0f6cbd.svg" alt="Version">
  <img src="https://img.shields.io/badge/Maturity-scaffolding-FFB020.svg" alt="Maturity">
</p>

---

**正直さのチェック - 今日動いているもの：** `eh3d.project.json` マニフェストで EH3D のリポジトリを見つけ、各ローカルコピーを GitHub と比較し、確認のうえで1つずつインストールまたは更新するコマンドラインと Qt Quick ウィンドウです。更新はクローンし、強制せずにマージし、まずステージングコピーでビルドと検証を行い、以前のインストールはバックアップとして残します。これは同じファミリーの他のエコシステムのアップデーターを EH3D の名前にしたもので、偽の GitHub とローカルリポジトリを使うコンピューター上のテストが 317 件あります。まだ実際の作業には使っておらず、インストール対象として存在するのは EH3D-COMMON と EH3D-CORE-LIBS だけです。

---

> **安全性（safety）とセキュリティの現状：** お使いのマシン上のファイルを置き換え、インストールするもののビルド検証を実行するため、明示的な確認の後にだけ行い、ローカルに変更のあるコピーには決して行わず、すべての試行を秘密情報を含まない証跡ログに記録します。コミットの署名は、そのポリシーを選んだ場合にだけ確認します。安全システムではなく、機械を制御することもありません。

## 📋 概要

| | |
|---|---|
| バージョン | `0.0.1` |
| 成熟度 | 足場段階 |
| テスト | 317 |
| 技術スタック | Python 3.10+ / PySide6 / Qt Quick |
| 実機 | 該当なし：使う人の PC 上で動作します |

## 🚦 プロジェクトの状況

各行はこのリポジトリの一部分で、信号は今日どこまで進んでいるかを示します。計画ではなく、リポジトリが示せるもの（テスト、ビルド、実行）に基づいて書かれています。

🟢 完了・検証済み · 🟡 動作する（既知の制限あり） · 🟠 一部のみ、または未検証 · 🔴 未実装または動作しない

| 領域 | 状態 | ここでの意味 |
|---|---|---|
| ソフトウェア | 🟡 | コマンドラインと Qt Quick ウィンドウが、マニフェストから EH3D のリポジトリを見つけ、GitHub と比較し、検証用クローンと以前のインストールのバックアップを使って 1 つずつインストール・更新します。 |
| テスト | 🟢 | 317 件のテストが通ります。模擬の GitHub とローカルのリポジトリを使い、ネットワークは使いません。 |
| 実運用 | 🟠 | まだ実際の作業には使われておらず、本物の GitHub からプロジェクトをインストール・更新したこともありません。インストール対象の EH3D リポジトリも少数です。 |
| インターフェース | 🟡 | ウィンドウは 8 言語で動作し、Python のブリッジはテストされています。コマンドラインは標準ライブラリだけで動きます。 |
| セキュリティ | 🟡 | 確認なしには何も変更されず、ローカルの変更があるチェックアウトにも手を加えません。マージは強制せず、証跡ログで編集や並べ替えが分かります。署名付きコミットのポリシーは任意で、独立したレビューは受けていません。 |
| 連携 | 🟡 | ELECTRO-HOBBY-3D-UPDATER が EH3D のプロジェクトをこのツールに引き渡します。この引き渡しは実際のチェックアウトでは実行されていません。 |
| 実機 | 🟢 | 該当なし：使う人の PC 上で動作します。 |
| ドキュメント | 🟢 | 8 言語の README、コマンドラインのリファレンス、ウィンドウのガイド。 |

## 🎯 概要

* **マニフェストでプロジェクトを見つけます：** エコシステムが `EH3D` の `eh3d.project.json` を持つ公開リポジトリはすべてプロジェクトです。新しいリポジトリはマニフェストを持つだけで現れ、このツールにプロジェクトの一覧はありません。
* **マシンを GitHub と比較します：** 各プロジェクトについてローカルコピーのバージョンと GitHub の既定ブランチのバージョンを読み、インストール済み、最新、古い、新しいコミットあり、のいずれかを示します。
* **確認のうえ、1つずつインストールまたは更新します：** 代わりのものはステージングコピーでビルドと検証を行ってから使用中のインストールに触れ、以前のものはウィンドウから復元できるバックアップとして残ります。
* **まとめての操作も確認されます：** *不足分をすべてインストール* と *古いものをすべて更新* は別々の順次実行で、同じ安全な経路を通ります。バックグラウンドで更新されることはありません。
* **証跡ログと任意の署名付きコミットポリシー：** すべての試行がログに書かれ、後から編集、削除、順序変更された行がないか確認できます。
* **8言語のウィンドウと、標準ライブラリだけで動くコマンドライン**（`--cli`）があり、画面のないマシンでも動作します。

## 🧩 EH3D での役割

EH3D-UPDATER は、スイートを入手して最新に保つための手段です。4つのエコシステムの上にある ELECTRO-HOBBY-3D-UPDATER は、EH3D のプロジェクトをこれに引き渡します。

## 📂 リポジトリ構成

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
│   ├── registry.py         リポジトリ自身のマニフェストの実行時の形
│   ├── version_parse.py    ローカルファイルと GitHub で共通のバージョンの読み取り方
│   ├── commits.py          チェックアウトをリモートとコミット単位で比較し、バージョン変更を伴わない新しいコミットを検出
│   ├── signature.py        コミット署名のポリシー: 既定では警告、要求すれば必須
│   ├── messages.py         コードとパラメーターで表すインストール・更新メッセージ (英語テキスト付き)
│   ├── settings.py         ウィンドウが起動をまたいで記憶する選択
│   ├── profiles.py         名前付きステーションプロファイル: マシンがインストールするプロジェクト
│   ├── notify.py           通知のみの確認で出るデスクトップ通知
│   ├── logs.py             ウィンドウのログファイルのローテーション (フォルダーが無制限に増えないように)
│   ├── gui.py              ウィンドウ形式の GUI
│   ├── assets/             プログラムのアイコン (.ico と .svg)
│   └── i18n.py             the eight languages
├── docs/
│   ├── CLI_REFERENCE.md    every command of the command line
│   └── QML_DESKTOP_GUI.md  the window
├── tests/                  the tests (no network, no board)
├── tools/ci_validate.py, build_test.py, generate_app_icon.py  CI が実行する検査、ビルド確認、ウィンドウアイコンの描画
└── eh3d.project.json       the manifest of the project
```

## 🛠️ ビルドと実行

Python 3.10 以降が必要です。ウィンドウには PySide6 も必要です（`pip install ".[gui]"`）。

```bash
PYTHONPATH=src python -m pytest tests -q
python -I tools/ci_validate.py
./run.sh --cli status        # run.bat --cli status on Windows
```

## 🔗 関連プロジェクト

* [EH3D-COMMON](https://github.com/JuanenRac/EH3D-COMMON): プロジェクトコンテナとマシンの型。このツールでインストールできます
* [EH3D-CORE-LIBS](https://github.com/JuanenRac/EH3D-CORE-LIBS): Gerber、Excellon、G-code のリーダー。このツールでインストールできます
* [ELECTRO-HOBBY-3D-UPDATER](https://github.com/JuanenRac/ELECTRO-HOBBY-3D-UPDATER): 4つのエコシステムの上にあるアップデーターで、これに委任します
* [URTC-UPDATER](https://github.com/JuanenRac/URTC-UPDATER): URTC のアップデーター。このツールの設計の元です

## 📚 ドキュメントとコミュニティ

* [コマンドラインリファレンス](docs/CLI_REFERENCE.md)と[デスクトップウィンドウ](docs/QML_DESKTOP_GUI.md)。
* [コントリビュート](CONTRIBUTING.md)、[セキュリティポリシー](SECURITY.md)、[サポート](SUPPORT.md)、[行動規範](CODE_OF_CONDUCT.md)。

## 👤 作者

**JuanenRac (Electro Hobby 3D)** · electrohobby3d@gmail.com

## 📜 ライセンス

ソフトウェア：GPL-3.0-or-later。[LICENSE](LICENSE) を参照。
