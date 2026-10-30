<p align="center">
  <img src="images/EH3D_UPDATER_BANNER.svg" alt="EH3D-UPDATER banner" width="100%">
</p>

# 🛠️ EH3D-UPDATER

<p align="center"><a href="README.md">🇺🇸 English</a> | <a href="README_spa.md">🇪🇸 Español</a> | <a href="README_fra.md">🇫🇷 Français</a> | 🇮🇹 <b>Italiano</b> | <a href="README_deu.md">🇩🇪 Deutsch</a> | <a href="README_zho.md">🇨🇳 中文</a> | <a href="README_jpn.md">🇯🇵 日本語</a> | <a href="README_por.md">🇵🇹 Português</a></p>

### Rileva, installa e aggiorna sul tuo PC i repository della EH3D Fabrication Suite: nulla accade da solo, e un'installazione in uso viene sostituita solo dopo che la sua sostituta è stata costruita e verificata

<p align="center">
  <img src="https://img.shields.io/badge/License-GPL%203.0--or--later-blue.svg" alt="GPL 3.0 or later">
  <img src="https://img.shields.io/badge/Stack-Python%203.10%2B-3776AB.svg" alt="Python">
  <img src="https://img.shields.io/badge/Languages-8-00E5FF.svg" alt="Languages">
  <img src="https://img.shields.io/badge/Version-0.0.2-0f6cbd.svg" alt="Version">
  <img src="https://img.shields.io/badge/Maturity-scaffolding-FFB020.svg" alt="Maturity">
</p>

---

**Verifica di onestà - cosa funziona oggi:** una riga di comando e una finestra Qt Quick che trovano i repository EH3D tramite i loro manifesti `eh3d.project.json`, confrontano ogni copia locale con GitHub e installano o aggiornano un progetto alla volta dopo una conferma. L'aggiornamento viene clonato, unito senza forzare, e costruito e verificato prima in un clone di staging, e l'installazione precedente è conservata come backup. È l'aggiornatore degli altri ecosistemi della famiglia con i nomi di EH3D, con 322 test che girano su un computer con un GitHub finto e repository locali. Non è ancora stato usato per lavoro reale e non ha mai installato né aggiornato un progetto dal vero GitHub.

---

> **Stato di sicurezza funzionale e informatica:** sostituisce file sulla tua macchina ed esegue il controllo di build di ciò che installa, quindi lo fa solo dopo una conferma esplicita, mai sopra una copia con modifiche locali, e registra ogni tentativo in un registro di prove che non contiene segreti. Verifica la firma di un commit solo se scegli quella politica; non è un sistema di sicurezza funzionale e non controlla alcuna macchina.

## 📋 In breve

| | |
|---|---|
| Versione | `0.0.2` |
| Maturità | Impalcatura |
| Test | 322 |
| Stack tecnologico | Python 3.10+ / PySide6 / Qt Quick |
| Su hardware reale | Non applicabile: gira sul PC della persona che lo usa |

**Vai a:** [Panoramica](#-panoramica) · [Architettura](#-architettura) · [Avvio rapido](#-avvio-rapido) · [Test](#-test) · [Struttura](#-struttura-del-repository) · [Correlati](#-progetti-correlati)

## 🚦 Stato del progetto

Ogni riga è una parte di questo repository e il semaforo dice a che punto è oggi. È scritta in base a ciò che il repository può mostrare (test, compilazioni, esecuzioni), non a ciò che è previsto.

🟢 Fatto e verificato · 🟡 Funziona, con limiti noti · 🟠 Fatto a metà o non ancora verificato · 🔴 Non fatto o non funzionante

| Area | Stato | Cosa significa qui |
|---|---|---|
| Software | 🟡 | Una riga di comando e una finestra Qt Quick trovano i repository EH3D tramite i loro manifesti, li confrontano con GitHub e installano o aggiornano un progetto alla volta, con un clone di staging e un backup dell'installazione precedente. |
| Test | 🟡 | Passano 322 test (`pytest`), con un GitHub finto e repository locali (senza rete); un altro viene saltato quando manca una copia vicina di cui ha bisogno. |
| Rilevamento | 🟡 | I repository pubblici sono solo candidati: un progetto entra nell'ecosistema quando il suo `eh3d.project.json` alla radice è valido e dice `EH3D`; provato contro un elenco finto, non eseguito contro il vero GitHub. |
| Uso reale | 🟠 | Non è ancora stato usato per lavoro reale e non ha mai installato né aggiornato un progetto dal vero GitHub; esistono solo pochi repository EH3D da installare. |
| Interfaccia | 🟡 | La finestra funziona in otto lingue e il suo ponte Python è coperto da test; la riga di comando richiede solo la libreria standard. |
| Sicurezza | 🟡 | Nulla cambia senza conferma né sopra una copia con modifiche locali, le unioni non forzano mai e un registro di prove mostra le righe modificate o riordinate; la politica dei commit firmati è facoltativa e non c'è stata una revisione indipendente. |
| Integrazione | 🟡 | ELECTRO-HOBBY-3D-UPDATER gli passa i progetti EH3D; questo passaggio non è stato eseguito su una copia reale. |
| Hardware reale | 🟡 | Non applicabile: gira sul PC della persona che lo usa. |
| Documentazione | 🟡 | README in otto lingue, il riferimento della riga di comando e la guida della finestra. |

## 🎯 Panoramica

* **Trova i progetti tramite i loro manifesti:** i repository pubblici del proprietario su GitHub sono solo un elenco di candidati; uno è un progetto quando il suo `eh3d.project.json` alla radice è valido e dichiara l'ecosistema `EH3D`, quindi un nuovo repository compare avendo un manifesto e nulla in questo strumento elenca i progetti. In locale, il nome di una cartella non basta mai per entrare nell'ecosistema.
* **Confronta la macchina con GitHub:** per ogni progetto legge la versione della copia locale e quella del ramo predefinito di GitHub, e dice se è installato, aggiornato, obsoleto o ha nuovi commit (una versione uguale con nuovi commit viene notata con un `git ls-remote`).
* **Installa e aggiorna un progetto alla volta, dopo una conferma:** la sostituta viene costruita e verificata in un clone di staging prima di toccare l'installazione in uso, e la precedente è conservata come backup ripristinabile dalla finestra o con `restore-backup`.
* **Anche i lotti sono confermati:** *Installa tutto ciò che manca* e *Aggiorna tutto ciò che è obsoleto* sono azioni separate e sequenziali attraverso lo stesso percorso di sicurezza. Nulla si aggiorna in background.
* **Un registro di prove e una politica facoltativa di commit firmati:** ogni tentativo viene scritto in un registro che si può verificare poi per righe modificate, rimosse o riordinate.
* **Profili di postazione:** un profilo con nome elenca i progetti con cui lavora una macchina, e la finestra e i comandi lo seguono.
* **Una finestra in otto lingue e una riga di comando** (`--cli`) che richiede solo la libreria standard, quindi funziona anche su una macchina senza schermo.

## 🧩 Ruolo in EH3D

EH3D-UPDATER è il modo per ottenere la suite e tenerla aggiornata. ELECTRO-HOBBY-3D-UPDATER, lo strumento sopra i quattro ecosistemi, gli passa i progetti EH3D. Un nuovo repository EH3D non richiede nulla qui: compare appena è pubblico e porta un manifesto valido.

## 🏛️ Architettura

<p align="center">
  <img src="images/architecture.svg" alt="Architettura di EH3D-UPDATER: chi lo usa, che cosa contiene e da che cosa dipende" width="100%">
</p>

Come si incastrano le parti di questo repository: chi lo usa, che cosa contiene e da che cosa dipende. L'immagine è disegnata da `docs/architecture.json` e verificata rispetto al codice.

## ✨ Funzionalità

* **Decide il manifesto:** il rilevamento, il nome, la versione, il comando di build e le note vengono dal `eh3d.project.json` del repository stesso; un candidato con manifesto non valido, o con una versione inferiore a quella installata, viene rifiutato prima di toccare qualsiasi cosa.
* **Una copia sana non viene mai sostituita:** una vera modifica locale o un ramo divergente fanno fallire l'aggiornamento rumorosamente, mai un reset silenzioso (`--ff-only` con `--no-build`).
* **Anteprima prima dell'aggiornamento:** `update --preview` mostra il commit candidato, il suo autore, lo stato della sua firma e i file di build e strumenti che cambia, poi si ferma.
* **Solo notifica:** `check` elenca ciò che si potrebbe aggiornare, non cambia nulla ed esce con 10 quando c'è qualcosa (una notifica desktop è facoltativa).
* **Backup con limite:** l'installazione precedente è conservata come `<nome>.backup-<8 cifre esadecimali>`; per impostazione predefinita si tengono le 2 più recenti e `clean-backups` pota il resto.
* **Gentile con la rete:** le richieste vengono ritentate con attesa, un `Retry-After` breve viene atteso, l'elenco dei repository è messo in cache con `If-None-Match` (un `304` non costa quota) e un GitHub irraggiungibile ripiega sullo stato locale con un avviso.

## 🔒 Sicurezza e protezione

| Minaccia | Difesa |
|---|---|
| Un aggiornamento indesiderato o a sorpresa | nulla gira in background: `install` e `update` prendono un nome di progetto e una conferma, e i pulsanti di gruppo della finestra sono separati, sequenziali e confermati |
| Un candidato rotto che sostituisce un'installazione funzionante | il candidato viene clonato, unito senza forzare, costruito e verificato in un clone di staging; la cartella in uso viene scambiata con due rinomine solo dopo, e la precedente è conservata come backup ripristinabile |
| Perdere lavoro locale | una copia con modifiche locali o un ramo divergente non viene mai sostituita: l'aggiornamento fallisce rumorosamente |
| Un repository che finge di far parte della suite | un repository entra solo quando il suo manifesto alla radice è valido e dichiara `EH3D`; un candidato con versione inferiore a quella installata viene rifiutato |
| Un commit di origine ignota | politica facoltativa: con `EH3D_UPDATER_REQUIRE_SIGNED=1` (o l'impostazione) e un file di firmatari consentiti un commit deve essere firmato; per impostazione predefinita uno non firmato viene installato con un avviso, e `update --preview` mostra prima lo stato della firma |
| Manomettere il registro di ciò che è accaduto | ogni tentativo di installazione o aggiornamento è una riga di un registro di prove che porta l'hash della riga precedente; `evidence` verifica la catena ed esce con 1 quando una riga è stata modificata, rimossa o riordinata |
| Fuga di segreti | il registro di prove non contiene segreti; GitHub si legge senza token (un `GITHUB_TOKEN` facoltativo alza solo il limite di richieste); lo strumento non lo stampa mai |
| Uno script di validazione che non può girare qui | un'installazione che non si può validare perché manca uno strumento viene rifiutata a meno che tu la accetti (l'impostazione `validation_unavailable` o `EH3D_UPDATER_ACCEPT_UNAVAILABLE_VALIDATION=1`) |
| Due istanze insieme | un'istanza che ne trova un'altra al lavoro sull'area di lavoro rifiuta di pulire o ripristinare i backup |

**Ciò che non è difeso:** lo script di build di un progetto installato è il codice di quel progetto e gira con i tuoi diritti, quindi installa solo ciò di cui ti fidi; i commit non firmati sono accettati per impostazione predefinita; e lo strumento non ha avuto una revisione indipendente. Segnala una vulnerabilità in privato (vedi [SECURITY.md](SECURITY.md)).

## 🔌 Interfacce

| Interfaccia | Che cos'è | Dove |
|---|---|---|
| Finestra | una finestra Qt Quick in otto lingue (il predefinito; richiede l'extra facoltativo `PySide6`) | `qt_gui.py`, `qml/Main.qml`, [docs/QML_DESKTOP_GUI.md](docs/QML_DESKTOP_GUI.md) |
| Riga di comando | `eh3d-updater --cli` con `status`, `install`, `update`, `check`, `clean-backups`, `restore-backup` ed `evidence`; codici di uscita 0, 1 e 10 (qualcosa si può aggiornare) | [docs/CLI_REFERENCE.md](docs/CLI_REFERENCE.md) |
| GitHub | `GET /users/<proprietario>/repos` (in cache con `If-None-Match`) e il manifesto grezzo di ogni candidato; nessun token necessario | `github_client.py` |
| L'area di lavoro | le cartelle accanto allo strumento, `<nome>.backup-xxxxxxxx` per le installazioni precedenti e `.eh3d-updater/evidence.jsonl` per il registro di prove | `install.py`, `evidence.py` |
| Impostazioni | `~/.eh3d_updater_settings.json` (lingua, area di lavoro, profilo, backup conservati, politica delle firme) | `settings.py` |

## ⚙️ Configurazione

Non c'è nulla da configurare per iniziare. Le scelte ricordate stanno in `~/.eh3d_updater_settings.json`, e alcune si possono dare anche come opzioni o variabili d'ambiente.

| Impostazione | Predefinito | Intervallo | Cosa fa |
|---|---|---|---|
| `workspace_root` / `--workspace` | la cartella madre dello strumento | una cartella | dove vivono le copie, i backup e il registro di prove |
| `lang` | la lingua del sistema | en, es, de, fr, it, ja, zh, pt | la lingua della finestra |
| `profile` / `--profile` | nessuno (tutti i progetti) | un nome di profilo definito; uno non definito è un errore | limita `status`, `check`, `install` e `update` ai progetti di un profilo di postazione |
| `backups_to_keep` / `clean-backups --keep` | 2 | un numero intero da 0 in su | quante installazioni precedenti si conservano per progetto |
| `require_signed_commits`, `allowed_signers_file` / `EH3D_UPDATER_REQUIRE_SIGNED=1`, `EH3D_UPDATER_ALLOWED_SIGNERS` | disattivato | attivato o disattivato | rifiutare i commit non firmati da un firmatario consentito |
| `validation_unavailable` / `EH3D_UPDATER_ACCEPT_UNAVAILABLE_VALIDATION=1` | rifiutare | rifiutare o accettare | cosa fare quando la validazione di un progetto non può girare perché manca uno strumento |
| `GITHUB_TOKEN` | nessuno | un token GitHub | alza solo il limite di richieste dell'elenco; mai obbligatorio |
| `--no-build` (install, update) | disattivato | attivato o disattivato | solo clonare o scaricare, senza il controllo di build del progetto (un semplice fast-forward) |

I valori di rete sono costanti: 10 s per richiesta, fino a 8 richieste alla volta, 3 tentativi con attesa e un `Retry-After` di al massimo 60 s.

## 🚀 Avvio rapido

Serve Python 3.10 o successivo; la finestra richiede anche PySide6 (`pip install ".[gui]"`).

```bash
./run.sh --cli status          # run.bat --cli status on Windows
./run.sh --cli status --offline --json
./run.sh --cli check           # exit code 10 when something can be updated
./run.sh --cli update EH3D-COMMON --preview
./run.sh --cli install EH3D-CORE-LIBS
```

`run.sh` / `run.bat` senza `--cli` aprono la finestra. `install` e `update` chiedono una conferma prima di toccare qualsiasi cosa, e prendono sempre un nome di progetto.

## 🧪 Test

La suite ha 322 test che passano (`pytest tests`), e uno che viene saltato quando una copia vicina di cui ha bisogno non è accanto a questa. Girano con un GitHub finto e repository locali, senza rete, e coprono il contratto del manifesto, il rilevamento, il confronto di versioni e commit, l'installazione e l'aggiornamento con il clone di staging e i rifiuti (modifiche locali, ramo divergente, versione inferiore, manifesto non valido, build che fallisce), i backup e il ripristino, la catena di prove, la politica delle firme, le impostazioni e i profili, i messaggi e le otto lingue della finestra, e il ponte Python della finestra (offscreen). Un test verifica anche che l'albero dei file di ogni README elenchi ogni voce versionata di primo livello. La CI li esegue su Linux e Windows, più `python tools/ci_validate.py` e un controllo di sintassi di ogni file Python.

## 🏗️ Compilazione e rilascio

La versione sta in `pyproject.toml`, in `eh3d.project.json` e nel pacchetto, e ogni versione ha la sua voce in [CHANGELOG.md](CHANGELOG.md). `build.sh` / `build.bat` installano il pacchetto e lo verificano, `build-test.sh` / `build-test.bat` eseguono anche i test e `test.sh` / `test.bat` eseguono solo i test, ciascuno in un pannello dal vivo; la versione non cambia. Le versioni vengono pubblicate su GitHub; lo strumento si installa da questo repository con pip e non è su PyPI.

## 📂 Struttura del repository

<p align="center">
  <img src="images/repository-structure.svg" alt="Struttura del repository EH3D-UPDATER" width="100%">
</p>

<details>
<summary>Versione testuale dell'albero</summary>

```text
EH3D-UPDATER/
├── src/eh3d_updater/
│   ├── main.py                                  la riga di comando e l'avvio della finestra
│   ├── github_client.py detect.py               le versioni su GitHub e le copie locali
│   ├── project_manifest.py registry.py          il contratto del manifesto e la sua forma a runtime
│   ├── install.py commits.py                    installare, aggiornare, backup; confronto commit
│   ├── evidence.py signature.py                 il registro di prove e la politica delle firme
│   ├── qt_gui.py qml/                           la finestra Qt Quick e il suo QML
│   ├── i18n.py messages.py                      le otto lingue e i messaggi come codici
│   └── settings.py profiles.py                  ciò che si ricorda e i profili di postazione
├── tests/                                       senza rete: un GitHub finto e repository locali
├── docs/                                        il riferimento della riga di comando, la guida della finestra e i dati delle due immagini
├── tools/                                       CI, build, README, icona e immagini
├── images/                                      banner e le immagini di Architettura e Struttura del repository
├── .github/                                     workflow di CI e di rilascio, modelli di issue e pull request
├── build.sh build.bat                           installa e verifica il pacchetto in un pannello dal vivo
├── build-test.sh build-test.bat                 lo stesso, poi i test
├── run.sh run.bat                               apre la finestra, o la riga di comando con --cli
├── bump*.py                                     gli script che alzano la versione
├── eh3d.project.json                            manifesto: versione, ruolo, maturità e comando di compilazione
├── run-gui.vbs                                  apre la finestra senza console su Windows
├── pyproject.toml                               il pacchetto Python e i suoi extra
├── CHANGELOG.md                                 cosa è cambiato in ogni versione
├── SECURITY.md SUPPORT.md                       come segnalare una vulnerabilità e dove chiedere
├── CONTRIBUTING.md CODE_OF_CONDUCT.md LICENSE   come contribuire, codice di condotta e licenza
└── LICENSE.md                                   il testo della licenza in Markdown
```

</details>

## 🗺️ Roadmap e limiti noti

**Limiti noti oggi**

* Non ha mai installato né aggiornato un progetto dal vero GitHub: tutto è provato con un GitHub finto e repository locali, ed esistono solo pochi repository EH3D da installare.
* Il passaggio da ELECTRO-HOBBY-3D-UPDATER non è stato eseguito su una copia reale.
* Per impostazione predefinita non si richiede che i commit siano firmati; la politica è facoltativa.
* Lo script di build di un progetto installato gira con i tuoi diritti.
* Lo strumento non ha avuto una revisione indipendente e non è su PyPI.

**Prossimi passi**

* Installare e aggiornare un progetto reale da cima a fondo con il vero GitHub e annotare ciò che emerge.
* Eseguire il passaggio da ELECTRO-HOBBY-3D-UPDATER su una copia reale.
* Decidere se i commit firmati diventano il valore predefinito della suite.

## 🌍 Lingue

Il README e i testi esistono in inglese, spagnolo, francese, italiano, tedesco, cinese, giapponese e portoghese europeo.

## 🔗 Progetti correlati

* [EH3D-COMMON](https://github.com/JuanenRac/EH3D-COMMON): il contenitore di progetto e i tipi di macchina; si può installare con questo strumento
* [EH3D-CORE-LIBS](https://github.com/JuanenRac/EH3D-CORE-LIBS): i lettori di Gerber, Excellon e G-code; si può installare con questo strumento
* [ELECTRO-HOBBY-3D-UPDATER](https://github.com/JuanenRac/ELECTRO-HOBBY-3D-UPDATER): l'aggiornatore sopra i quattro ecosistemi, che passa la mano a questo
* [URTC-UPDATER](https://github.com/JuanenRac/URTC-UPDATER): l'aggiornatore di URTC, da cui questo strumento prende il progetto

## 📚 Documentazione

* [Riferimento della riga di comando](docs/CLI_REFERENCE.md): ogni comando, opzione e codice di uscita.
* [La finestra desktop](docs/QML_DESKTOP_GUI.md): come la finestra Qt Quick poggia sugli stessi servizi della riga di comando.
* [Registro delle modifiche](CHANGELOG.md)

## 🤝 Contribuire e comunità

* Prima di una pull request esegui `PYTHONPATH=src python -m pytest tests -q` e `python -I tools/ci_validate.py`: tutto deve passare. Vedi [CONTRIBUTING.md](CONTRIBUTING.md) e il [codice di condotta](CODE_OF_CONDUCT.md).
* Il README esiste in otto lingue: una modifica al testo si fa in tutti e otto i file, e le due immagini sono disegnate da `docs/architecture.json` e `docs/structure.json` con `tools/make_architecture.py` e `tools/make_structure.py`.
* Una modifica a un testo visibile all'utente va nelle otto lingue di `i18n.py`; una decisione di sicurezza si prende nei servizi Python, mai nel QML.
* Segnala una vulnerabilità in privato: [SECURITY.md](SECURITY.md). Domande, idee e segnalazioni: electrohobby3d@gmail.com ([SUPPORT.md](SUPPORT.md)).

## 👤 AUTORE

**JuanenRac (Electro Hobby 3D)** · electrohobby3d@gmail.com

## 📜 LICENZA

Software: GPL-3.0-or-later. Vedi [LICENSE](LICENSE). I progetti hardware della suite usano la CERN OHL-S.
