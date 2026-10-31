<p align="center">
  <img src="images/EH3D_UPDATER_BANNER.svg" alt="EH3D-UPDATER banner" width="100%">
</p>

# 🛠️ EH3D-UPDATER

<p align="center"><a href="README.md">🇺🇸 English</a> | <a href="README_spa.md">🇪🇸 Español</a> | <a href="README_fra.md">🇫🇷 Français</a> | <a href="README_ita.md">🇮🇹 Italiano</a> | <a href="README_deu.md">🇩🇪 Deutsch</a> | <a href="README_zho.md">🇨🇳 中文</a> | <a href="README_jpn.md">🇯🇵 日本語</a> | 🇵🇹 <b>Português</b></p>

### Deteta, instala e atualiza no teu PC os repositórios da EH3D Fabrication Suite: nada acontece sozinho, e uma instalação em uso só é substituída depois de a sua substituta ter sido construída e verificada

<p align="center">
  <img src="https://img.shields.io/badge/License-GPL%203.0--or--later-blue.svg" alt="GPL 3.0 or later">
  <img src="https://img.shields.io/badge/Stack-Python%203.10%2B-3776AB.svg" alt="Python">
  <img src="https://img.shields.io/badge/Languages-8-00E5FF.svg" alt="Languages">
  <img src="https://img.shields.io/badge/Version-0.0.2-0f6cbd.svg" alt="Version">
  <img src="https://img.shields.io/badge/Maturity-scaffolding-FFB020.svg" alt="Maturity">
</p>

---

**Verificação de honestidade - o que funciona hoje:** uma linha de comandos e uma janela Qt Quick que encontram os repositórios EH3D pelos seus manifestos `eh3d.project.json`, comparam cada cópia local com o GitHub e instalam ou atualizam um de cada vez após uma confirmação. A atualização é clonada, fundida sem forçar, e construída e verificada primeiro num clone de preparação, e a instalação anterior fica guardada como cópia de segurança. É o atualizador dos outros ecossistemas da família com os nomes do EH3D, com 334 testes que correm num computador com um GitHub simulado e repositórios locais. Ainda não foi usado para trabalho real e nunca instalou nem atualizou um projeto a partir do GitHub real.

---

> **Estado de segurança (safety) e de segurança informática:** substitui ficheiros na tua máquina e executa a verificação de construção do que instala, por isso só o faz após uma confirmação explícita, nunca sobre uma cópia com alterações locais, e regista cada tentativa num registo de evidências que não leva segredos. Só verifica a assinatura de um commit se escolheres essa política; não é um sistema de segurança (safety) e não controla nenhuma máquina.

## 📋 Num relance

| | |
|---|---|
| Versão | `0.0.2` |
| Maturidade | Estrutura inicial |
| Testes | 334 |
| Tecnologias | Python 3.10+ / PySide6 / Qt Quick |
| Em hardware real | Não se aplica: corre no PC da pessoa que o usa |

**Ir para:** [Visão geral](#-visão-geral) · [Arquitetura](#-arquitetura) · [Início rápido](#-início-rápido) · [Testes](#-testes) · [Estrutura](#-estrutura-do-repositório) · [Relacionados](#-projetos-relacionados)

## 🚦 Estado do projeto

Cada linha é uma parte deste repositório e a luz diz até onde chega hoje. É escrita com o que o repositório consegue demonstrar (testes, compilações, execuções), não com o que está previsto.

🟢 Feito e verificado · 🟡 Funciona, com limites conhecidos · 🟠 Feito a meio ou ainda por verificar · 🔴 Por fazer ou a não funcionar

| Área | Estado | O que significa aqui |
|---|---|---|
| Software | 🟡 | Uma linha de comandos e uma janela Qt Quick encontram os repositórios EH3D pelos seus manifestos, comparam-nos com o GitHub e instalam ou atualizam um de cada vez, com um clone de preparação e uma cópia da instalação anterior. |
| Testes | 🟡 | Passam 334 testes (`pytest`), com um GitHub simulado e repositórios locais (sem rede); outro é ignorado quando falta uma cópia vizinha de que precisa. |
| Descoberta | 🟡 | Os repositórios públicos são só candidatos: um projeto entra no ecossistema quando o seu `eh3d.project.json` da raiz valida e diz `EH3D`; testado contra uma listagem simulada, não executado contra o GitHub real. |
| Uso real | 🟠 | Ainda não foi usado para trabalho real e nunca instalou nem atualizou um projeto a partir do GitHub real; só existem poucos repositórios EH3D para instalar. |
| Interface | 🟡 | A janela funciona em oito idiomas e a sua ponte Python está coberta por testes; a linha de comandos só precisa da biblioteca padrão. |
| Segurança | 🟡 | Nada muda sem confirmação nem sobre uma cópia com alterações locais, as fusões nunca forçam e um registo de evidências mostra as linhas editadas ou reordenadas; a política de commits assinados é opcional e não houve revisão independente. |
| Integração | 🟡 | O ELECTRO-HOBBY-3D-UPDATER passa-lhe os projetos EH3D; essa passagem não foi executada contra uma cópia real. |
| Hardware real | 🟡 | Não se aplica: corre no PC da pessoa que o usa. |
| Documentação | 🟡 | README em oito idiomas, a referência da linha de comandos e o guia da janela. |

## 🎯 Visão geral

* **Encontra os projetos pelos seus manifestos:** os repositórios públicos do proprietário no GitHub são só uma lista de candidatos; um é um projeto quando o seu `eh3d.project.json` da raiz valida e declara o ecossistema `EH3D`, por isso um repositório novo aparece por ter um manifesto e nada nesta ferramenta enumera os projetos. Em local, o nome de uma pasta nunca basta para entrar no ecossistema.
* **Compara a máquina com o GitHub:** de cada projeto lê a versão da cópia local e a do ramo por omissão do GitHub, e diz se está instalado, atualizado, desatualizado ou com commits novos (uma versão igual com commits novos é detetada com um `git ls-remote`).
* **Instala e atualiza um projeto de cada vez, após uma confirmação:** a substituta é construída e verificada num clone de preparação antes de tocar na instalação em uso, e a anterior fica guardada como cópia que se pode restaurar a partir da janela ou com `restore-backup`.
* **Os lotes também se confirmam:** *Instalar tudo o que falta* e *Atualizar tudo o que está desatualizado* são ações separadas e sequenciais pelo mesmo caminho de segurança. Nada se atualiza em segundo plano.
* **Um registo de evidências e uma política opcional de commits assinados:** cada tentativa é escrita num registo que depois se pode verificar à procura de linhas editadas, removidas ou reordenadas.
* **Perfis de posto:** um perfil com nome lista os projetos com que uma máquina trabalha, e a janela e os comandos seguem-no.
* **Uma janela em oito idiomas e uma linha de comandos** (`--cli`) que só precisa da biblioteca padrão, por isso também funciona numa máquina sem ecrã.

## 🧩 Papel no EH3D

O EH3D-UPDATER é o modo de obter a suite e mantê-la atualizada. O ELECTRO-HOBBY-3D-UPDATER, a ferramenta acima dos quatro ecossistemas, passa-lhe os projetos EH3D. Um repositório EH3D novo não precisa de nada aqui: aparece assim que é público e leva um manifesto válido.

## 🏛️ Arquitetura

<p align="center">
  <img src="images/architecture.svg" alt="Arquitetura de EH3D-UPDATER: quem o usa, o que contém e de que depende" width="100%">
</p>

Como as partes deste repositório se encaixam: quem o usa, o que contém e de que depende. A imagem é desenhada a partir de `docs/architecture.json` e verificada com o código.

## ✨ Funcionalidades

* **O manifesto decide:** a descoberta, o nome, a versão, o comando de compilação e as notas vêm do próprio `eh3d.project.json` do repositório; um candidato com manifesto inválido, ou com versão inferior à instalada, é recusado antes de tocar em qualquer coisa.
* **Uma cópia saudável nunca é substituída:** uma edição local real ou um ramo divergente fazem a atualização falhar em voz alta, nunca um reinício silencioso (`--ff-only` com `--no-build`).
* **Pré-visualização antes de atualizar:** `update --preview` mostra o commit candidato, o seu autor, o estado da sua assinatura e os ficheiros de compilação e ferramentas que altera, e pára.
* **Só notificar:** `check` lista o que se poderia atualizar, não altera nada e termina com 10 quando há algo (uma notificação de ambiente de trabalho é opcional).
* **Cópias de segurança com limite:** a instalação anterior fica como `<nome>.backup-<8 dígitos hex>`; por omissão guardam-se as 2 mais recentes e `clean-backups` poda o resto.
* **Simpático com a rede:** os pedidos são repetidos com espera, um `Retry-After` curto é esperado, a lista de repositórios é guardada em cache com `If-None-Match` (um `304` não gasta quota) e um GitHub inalcançável recua para o estado local com um aviso.

## 🔒 Segurança e proteção

| Ameaça | Defesa |
|---|---|
| Uma atualização indesejada ou de surpresa | nada corre em segundo plano: `install` e `update` recebem um nome de projeto e uma confirmação, e os botões de lote da janela são separados, sequenciais e confirmados |
| Um candidato estragado a substituir uma instalação que funcionava | o candidato é clonado, fundido sem forçar, construído e verificado num clone de preparação; a pasta em uso só é trocada depois, com duas mudanças de nome, e a anterior fica guardada como cópia restaurável |
| Perder trabalho local | uma cópia com alterações locais ou um ramo divergente nunca é substituída: a atualização falha em voz alta |
| Um repositório que finge fazer parte da suite | um repositório só entra quando o seu manifesto da raiz valida e declara `EH3D`; um candidato com versão inferior à instalada é recusado |
| Um commit de origem desconhecida | política opcional: com `EH3D_UPDATER_REQUIRE_SIGNED=1` (ou a definição) e um ficheiro de signatários permitidos um commit tem de estar assinado; por omissão um não assinado é instalado com um aviso, e `update --preview` mostra antes o estado da assinatura |
| Adulterar o registo do que aconteceu | cada tentativa de instalação ou atualização é uma linha de um registo de evidências que leva o hash da linha anterior; `evidence` verifica a cadeia e termina com 1 quando uma linha foi editada, removida ou reordenada |
| Fuga de segredos | o registo de evidências não leva segredos; o GitHub lê-se sem token (um `GITHUB_TOKEN` opcional só sobe o limite de pedidos); a ferramenta nunca o imprime |
| Um script de validação que não pode correr aqui | uma instalação que não se pode validar porque falta uma ferramenta é recusada a menos que a aceites (a definição `validation_unavailable` ou `EH3D_UPDATER_ACCEPT_UNAVAILABLE_VALIDATION=1`) |
| Duas instâncias ao mesmo tempo | uma instância que encontra outra a trabalhar na área de trabalho recusa limpar ou restaurar cópias de segurança |

**O que não é defendido:** o script de compilação de um projeto instalado é código desse projeto e corre com os teus direitos, por isso instala só o que for de confiança; os commits sem assinatura são aceites por omissão; e a ferramenta não teve revisão independente. Comunica uma vulnerabilidade em privado (ver [SECURITY.md](SECURITY.md)).

## 🔌 Interfaces

| Interface | O que é | Onde |
|---|---|---|
| Janela | uma janela Qt Quick em oito idiomas (a predefinida; precisa do extra opcional `PySide6`) | `qt_gui.py`, `qml/Main.qml`, [docs/QML_DESKTOP_GUI.md](docs/QML_DESKTOP_GUI.md) |
| Linha de comandos | `eh3d-updater --cli` com `status`, `install`, `update`, `check`, `clean-backups`, `restore-backup` e `evidence`; códigos de saída 0, 1 e 10 (algo pode ser atualizado) | [docs/CLI_REFERENCE.md](docs/CLI_REFERENCE.md) |
| GitHub | `GET /users/<proprietário>/repos` (em cache com `If-None-Match`) e o manifesto em bruto de cada candidato; não é preciso token | `github_client.py` |
| A área de trabalho | as pastas junto à ferramenta, `<nome>.backup-xxxxxxxx` para as instalações anteriores e `.eh3d-updater/evidence.jsonl` para o registo de evidências | `install.py`, `evidence.py` |
| Definições | `~/.eh3d_updater_settings.json` (idioma, área de trabalho, perfil, cópias guardadas, política de assinaturas) | `settings.py` |

## ⚙️ Configuração

Não é preciso configurar nada para começar. As escolhas que ficam lembradas vivem em `~/.eh3d_updater_settings.json`, e algumas também se podem dar como opções ou variáveis de ambiente.

| Definição | Por omissão | Gama | O que faz |
|---|---|---|---|
| `workspace_root` / `--workspace` | a pasta-mãe da ferramenta | uma pasta | onde vivem as cópias, as cópias de segurança e o registo de evidências |
| `lang` | o idioma do sistema | en, es, de, fr, it, ja, zh, pt | o idioma da janela |
| `profile` / `--profile` | nenhum (todos os projetos) | um nome de perfil definido; um não definido é um erro | restringe `status`, `check`, `install` e `update` aos projetos de um perfil de posto |
| `backups_to_keep` / `clean-backups --keep` | 2 | um número inteiro de 0 ou mais | quantas instalações anteriores se guardam por projeto |
| `require_signed_commits`, `allowed_signers_file` / `EH3D_UPDATER_REQUIRE_SIGNED=1`, `EH3D_UPDATER_ALLOWED_SIGNERS` | desativado | ativado ou desativado | recusar commits que um signatário permitido não tenha assinado |
| `validation_unavailable` / `EH3D_UPDATER_ACCEPT_UNAVAILABLE_VALIDATION=1` | recusar | recusar ou aceitar | o que fazer quando a validação de um projeto não pode correr porque falta uma ferramenta |
| `GITHUB_TOKEN` | nenhum | um token do GitHub | só sobe o limite de pedidos da listagem; nunca é obrigatório |
| `--no-build` (install, update) | desativado | ativado ou desativado | só clonar ou trazer, sem a verificação de construção do projeto (um simples avanço rápido) |

Os valores de rede são constantes: 10 s por pedido, até 8 pedidos de cada vez, 3 tentativas com espera e um `Retry-After` de 60 s no máximo.

## 🚀 Início rápido

Precisa de Python 3.10 ou mais recente; a janela precisa também do PySide6 (`pip install ".[gui]"`).

```bash
./run.sh --cli status          # run.bat --cli status on Windows
./run.sh --cli status --offline --json
./run.sh --cli check           # exit code 10 when something can be updated
./run.sh --cli update EH3D-COMMON --preview
./run.sh --cli install EH3D-CORE-LIBS
```

`run.sh` / `run.bat` sem `--cli` abrem a janela. `install` e `update` pedem uma confirmação antes de tocar em qualquer coisa, e recebem sempre um nome de projeto.

## 🧪 Testes

A suite tem 334 testes que passam (`pytest tests`), e mais um que é ignorado quando uma cópia vizinha de que precisa não está junto a esta. Correm com um GitHub simulado e repositórios locais, sem rede, e cobrem o contrato do manifesto, a descoberta, a comparação de versões e commits, a instalação e a atualização com o clone de preparação e as recusas (alterações locais, ramo divergente, versão inferior, manifesto inválido, construção que falha), as cópias de segurança e o restauro, a cadeia de evidências, a política de assinaturas, as definições e os perfis, as mensagens e os oito idiomas da janela, e a ponte Python da janela (fora do ecrã). Um teste verifica também que a árvore de ficheiros de cada README lista cada entrada versionada de primeiro nível. A CI executa-os em Linux e Windows, mais `python tools/ci_validate.py` e uma verificação de sintaxe de cada ficheiro Python.

## 🏗️ Compilação e publicação

A versão vive em `pyproject.toml`, em `eh3d.project.json` e no pacote, e cada versão tem a sua entrada em [CHANGELOG.md](CHANGELOG.md). `build.sh` / `build.bat` instalam o pacote e verificam-no, `build-test.sh` / `build-test.bat` executam também os testes e `test.sh` / `test.bat` executam só os testes, cada um num painel em direto; a versão não muda. As versões são publicadas no GitHub; a ferramenta instala-se a partir deste repositório com o pip e não está no PyPI.

## 📂 Estrutura do repositório

<p align="center">
  <img src="images/repository-structure.svg" alt="Estrutura do repositório EH3D-UPDATER" width="100%">
</p>

<details>
<summary>Versão em texto da árvore</summary>

```text
EH3D-UPDATER/
├── src/eh3d_updater/
│   ├── main.py                                  a linha de comandos e o arranque da janela
│   ├── github_client.py detect.py               as versões no GitHub e as cópias locais
│   ├── project_manifest.py registry.py          o contrato do manifesto e a sua forma em execução
│   ├── install.py commits.py                    instalar, atualizar, cópias; comparar commits
│   ├── evidence.py signature.py                 o registo de evidências e a política de assinaturas
│   ├── qt_gui.py qml/                           a janela Qt Quick e o seu QML
│   ├── i18n.py messages.py                      os oito idiomas e as mensagens como códigos
│   └── settings.py profiles.py                  o que se lembra e os perfis de posto
├── tests/                                       sem rede: um GitHub simulado e repositórios locais
├── docs/                                        a referência da linha de comandos, o guia da janela e os dados das duas imagens
├── tools/                                       CI, construção, README, ícone e imagens
├── images/                                      banner e as imagens de Arquitetura e Estrutura do repositório
├── .github/                                     fluxos de CI e de publicação, modelos de issues e pull requests
├── build.sh build.bat                           instala e verifica o pacote num painel em direto
├── build-test.sh build-test.bat                 o mesmo, e depois os testes
├── run.sh run.bat                               abre a janela, ou a linha de comandos com --cli
├── bump*.py                                     os scripts que sobem a versão
├── eh3d.project.json                            manifesto: versão, papel, maturidade e comando de compilação
├── run-gui.vbs                                  abre a janela sem consola no Windows
├── pyproject.toml                               o pacote Python e os seus extras
├── CHANGELOG.md                                 o que mudou em cada versão
├── SECURITY.md SUPPORT.md                       como comunicar uma vulnerabilidade e onde perguntar
├── CONTRIBUTING.md CODE_OF_CONDUCT.md LICENSE   como contribuir, o código de conduta e a licença
└── LICENSE.md                                   o texto da licença em Markdown
```

</details>

## 🗺️ Roteiro e limites conhecidos

**Limites conhecidos hoje**

* Nunca instalou nem atualizou um projeto a partir do GitHub real: tudo é testado com um GitHub simulado e repositórios locais, e só existem poucos repositórios EH3D para instalar.
* A passagem a partir do ELECTRO-HOBBY-3D-UPDATER não foi executada contra uma cópia real.
* Por omissão não se exige que os commits estejam assinados; a política é opcional.
* O script de compilação de um projeto instalado corre com os teus direitos.
* A ferramenta não teve revisão independente e não está no PyPI.

**A seguir**

* Instalar e atualizar um projeto real de ponta a ponta com o GitHub real e registar o que aparecer.
* Executar a passagem a partir do ELECTRO-HOBBY-3D-UPDATER numa cópia real.
* Decidir se os commits assinados passam a ser o valor por omissão da suite.

## 🌍 Idiomas

O README e os textos existem em inglês, espanhol, francês, italiano, alemão, chinês, japonês e português europeu.

## 🔗 Projetos relacionados

* [EH3D-COMMON](https://github.com/JuanenRac/EH3D-COMMON): o contentor de projeto e os tipos de máquina; pode ser instalado com esta ferramenta
* [EH3D-CORE-LIBS](https://github.com/JuanenRac/EH3D-CORE-LIBS): os leitores de Gerber, Excellon e G-code; pode ser instalado com esta ferramenta
* [ELECTRO-HOBBY-3D-UPDATER](https://github.com/JuanenRac/ELECTRO-HOBBY-3D-UPDATER): o atualizador acima dos quatro ecossistemas, que passa a mão a este
* [URTC-UPDATER](https://github.com/JuanenRac/URTC-UPDATER): o atualizador do URTC, de que esta ferramenta toma o desenho

## 📚 Documentação

* [Referência da linha de comandos](docs/CLI_REFERENCE.md): cada comando, opção e código de saída.
* [A janela de ambiente de trabalho](docs/QML_DESKTOP_GUI.md): como a janela Qt Quick assenta nos mesmos serviços que a linha de comandos.
* [Registo de alterações](CHANGELOG.md)

## 🤝 Contribuir e comunidade

* Antes de um pull request execute `PYTHONPATH=src python -m pytest tests -q` e `python -I tools/ci_validate.py`: tudo tem de passar. Consulte [CONTRIBUTING.md](CONTRIBUTING.md) e o [código de conduta](CODE_OF_CONDUCT.md).
* O README existe em oito idiomas: uma alteração ao texto faz-se nos oito ficheiros, e as duas imagens são desenhadas a partir de `docs/architecture.json` e `docs/structure.json` com `tools/make_architecture.py` e `tools/make_structure.py`.
* Uma alteração a um texto visível ao utilizador vai para os oito idiomas de `i18n.py`; uma decisão de segurança toma-se nos serviços Python, nunca no QML.
* Comunique uma vulnerabilidade em privado: [SECURITY.md](SECURITY.md). Perguntas, ideias e relatórios: electrohobby3d@gmail.com ([SUPPORT.md](SUPPORT.md)).

## 👤 AUTOR

**JuanenRac (Electro Hobby 3D)** · electrohobby3d@gmail.com

## 📜 LICENÇA

Software: GPL-3.0-or-later. Ver [LICENSE](LICENSE). Os projetos de hardware da suite usam a CERN OHL-S.
